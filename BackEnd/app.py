from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import sys
import logging
import os
import uuid
from sqlalchemy import func

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Database configuration
try:
    # Use environment variable if available, otherwise fallback to local
    database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:Limelemon1%40@localhost/research_db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    logger.info("Database connection established successfully")
except Exception as e:
    logger.error(f"Database connection error: {e}")
    sys.exit(1)

# Database Models
class Rating(db.Model):
    __tablename__ = 'ratings'
    
    rating_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), nullable=False)  # UUID for grouping submissions
    summary_id = db.Column(db.Integer, nullable=False)  # ID of the summary (1-5)
    prompt_text = db.Column(db.Text, nullable=False)
    ai_summary = db.Column(db.Text, nullable=False)
    rating_value = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'rating_id': self.rating_id,
            'session_id': self.session_id,
            'summary_id': self.summary_id,
            'prompt_text': self.prompt_text,
            'ai_summary': self.ai_summary,
            'rating_value': self.rating_value,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Create tables
def init_db():
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            sys.exit(1)

init_db()

# Development only - endpoint to reset ratings
@app.route('/api/reset_ratings', methods=['POST'])
def reset_ratings():
    try:
        # Delete all entries from the ratings table
        Rating.query.delete()
        db.session.commit()
        logger.info("All ratings have been cleared")
        return jsonify({"message": "All ratings have been cleared successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error clearing ratings: {e}")
        return jsonify({"error": "Failed to clear ratings"}), 500

# API Routes
@app.route('/api/ratings', methods=['POST'])
def add_ratings():
    try:
        data = request.json
        if not data or not isinstance(data, list):
            return jsonify({"error": "Invalid data format. Expected a list of ratings."}), 400

        # Generate a unique session ID for this submission
        session_id = str(uuid.uuid4())

        for i, entry in enumerate(data):
            if not all(key in entry for key in ['prompt_text', 'ai_summary', 'rating']):
                return jsonify({"error": "Missing required fields in rating entry"}), 400
            
            if not isinstance(entry['rating'], int) or not 1 <= entry['rating'] <= 5:
                return jsonify({"error": "Rating must be an integer between 1 and 5"}), 400

            new_rating = Rating(
                session_id=session_id,
                summary_id=i + 1,  # Summary IDs 1-5
                prompt_text=entry['prompt_text'],
                ai_summary=entry['ai_summary'],
                rating_value=entry['rating']
            )
            db.session.add(new_rating)
        
        db.session.commit()
        logger.info(f"Ratings added successfully for session {session_id}")
        return jsonify({"message": "Ratings added successfully", "session_id": session_id}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding ratings: {e}")
        return jsonify({"error": "Failed to save ratings"}), 500

@app.route('/api/ratings', methods=['GET'])
def get_ratings():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        pagination = Rating.query.order_by(Rating.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'ratings': [rating.to_dict() for rating in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving ratings: {e}")
        return jsonify({"error": "Failed to retrieve ratings"}), 500

@app.route('/api/ratings/stats', methods=['GET'])
def get_rating_stats():
    try:
        # Get basic statistics
        stats = db.session.query(
            func.count(Rating.rating_id).label('total_ratings'),
            func.avg(Rating.rating_value).label('average_rating'),
            func.min(Rating.rating_value).label('min_rating'),
            func.max(Rating.rating_value).label('max_rating')
        ).first()

        # Get rating distribution
        distribution = db.session.query(
            Rating.rating_value,
            func.count(Rating.rating_id).label('count')
        ).group_by(Rating.rating_value).all()

        # Get statistics by summary ID
        summary_stats = db.session.query(
            Rating.summary_id,
            func.count(Rating.rating_id).label('total_ratings'),
            func.avg(Rating.rating_value).label('average_rating'),
            func.min(Rating.rating_value).label('min_rating'),
            func.max(Rating.rating_value).label('max_rating')
        ).group_by(Rating.summary_id).all()

        # Get all individual submissions grouped by session
        sessions = db.session.query(Rating.session_id).distinct().all()
        individual_submissions = []
        
        for session in sessions:
            session_ratings = Rating.query.filter_by(session_id=session.session_id).order_by(Rating.summary_id).all()
            if session_ratings:  # Only include complete sessions
                individual_submissions.append({
                    'session_id': session.session_id,
                    'submitted_at': session_ratings[0].created_at.isoformat(),
                    'ratings': [rating.to_dict() for rating in session_ratings],
                    'session_average': sum(r.rating_value for r in session_ratings) / len(session_ratings)
                })

        # Sort by submission time (most recent first)
        individual_submissions.sort(key=lambda x: x['submitted_at'], reverse=True)

        return jsonify({
            'overall_statistics': {
                'total_ratings': int(stats.total_ratings) if stats.total_ratings else 0,
                'total_sessions': len(individual_submissions),
                'average_rating': float(stats.average_rating) if stats.average_rating else 0,
                'min_rating': int(stats.min_rating) if stats.min_rating else 0,
                'max_rating': int(stats.max_rating) if stats.max_rating else 0
            },
            'distribution': {
                str(rating): count for rating, count in distribution
            },
            'summary_statistics': {
                str(stat.summary_id): {
                    'total_ratings': int(stat.total_ratings),
                    'average_rating': float(stat.average_rating),
                    'min_rating': int(stat.min_rating),
                    'max_rating': int(stat.max_rating)
                } for stat in summary_stats
            },
            'individual_submissions': individual_submissions[:20]  # Latest 20 submissions
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving rating statistics: {e}")
        return jsonify({"error": "Failed to retrieve rating statistics"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')