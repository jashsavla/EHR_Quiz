import React, { useState } from 'react';
import axios from 'axios';
import { summaries } from '../data/summaries';

const SummaryRatingForm = () => {
  const [ratings, setRatings] = useState({});
  const [message, setMessage] = useState({ type: '', text: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleRating = (id, value) => {
    setRatings(prev => ({
      ...prev,
      [id]: value
    }));
    // Clear any error messages when user makes a new rating
    setMessage({ type: '', text: '' });
  };

  const handleSubmit = async () => {
    // Validate that all summaries have been rated
    if (Object.keys(ratings).length !== summaries.length) {
      setMessage({
        type: 'error',
        text: 'Please rate all summaries before submitting.'
      });
      return;
    }

    setIsSubmitting(true);
    try {
      const submitData = summaries.map(summary => ({
        prompt_text: summary.originalText,
        ai_summary: summary.aiSummary,
        rating: ratings[summary.id]
      }));

      const response = await axios.post('http://localhost:5000/api/ratings', submitData);
      
      if (response.status === 201) {
        setMessage({
          type: 'success',
          text: 'Ratings submitted successfully! Thank you for your feedback.'
        });
        // Reset ratings after successful submission
        setRatings({});
      } else {
        throw new Error('Submission failed');
      }
    } catch (error) {
      console.error('Error submitting ratings:', error);
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to submit ratings. Please try again.'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="summary-form">
      <h2>EHR Summary Rating System</h2>
      <p className="instructions">
        Please rate how well each AI-generated summary captures the essential information from the original EHR summary.
        Rate from 1 (poor) to 5 (excellent).
      </p>

      {summaries.map(summary => (
        <div key={summary.id} className="summary-entry">
          <h3>Original EHR Summary</h3>
          <div className="summary-text">
            {summary.originalText.split('\n').map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>
          
          <h3>AI-Generated Summary</h3>
          <div className="ai-summary">
            <p>{summary.aiSummary}</p>
          </div>

          <div className="rating-container">
            <p>Rate this summary:</p>
            {[1, 2, 3, 4, 5].map(value => (
              <div
                key={value}
                className={`rating-circle ${ratings[summary.id] === value ? 'active' : ''}`}
                onClick={() => !isSubmitting && handleRating(summary.id, value)}
                style={{ cursor: isSubmitting ? 'not-allowed' : 'pointer' }}
              >
                {value}
              </div>
            ))}
          </div>
        </div>
      ))}

      {message.text && (
        <div className={`message ${message.type}-message`}>
          {message.text}
        </div>
      )}

      <button
        className="submit-button"
        onClick={handleSubmit}
        disabled={isSubmitting || Object.keys(ratings).length !== summaries.length}
      >
        {isSubmitting ? 'Submitting...' : 'Submit Ratings'}
      </button>
    </div>
  );
};

export default SummaryRatingForm; 