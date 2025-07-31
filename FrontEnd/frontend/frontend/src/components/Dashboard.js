import React, { useEffect, useState } from 'react';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);
  const [expandedSessions, setExpandedSessions] = useState(new Set());

  useEffect(() => {
    const fetchStats = () => {
      fetch('http://localhost:5000/api/ratings/stats')
        .then(res => {
          if (res.headers.get('content-type')?.includes('application/json')) {
            return res.json();
          } else {
            throw new Error('Received non-JSON response');
          }
        })
        .then(data => setStats(data))
        .catch(err => {
          console.error('Fetch error:', err);
          setError(err.message);
        });
    };
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const toggleSession = (sessionId) => {
    const newExpanded = new Set(expandedSessions);
    if (newExpanded.has(sessionId)) {
      newExpanded.delete(sessionId);
    } else {
      newExpanded.add(sessionId);
    }
    setExpandedSessions(newExpanded);
  };

  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;
  if (!stats) return <div>Loading...</div>;

  return (
    <div className="dashboard-container">
      <h1>Admin Dashboard</h1>
      
      {/* Overall Statistics */}
      <div className="stats-section">
        <h2>Overall Statistics</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Sessions</h3>
            <p className="stat-number">{stats.overall_statistics.total_sessions}</p>
          </div>
          <div className="stat-card">
            <h3>Total Ratings</h3>
            <p className="stat-number">{stats.overall_statistics.total_ratings}</p>
          </div>
          <div className="stat-card">
            <h3>Average Rating</h3>
            <p className="stat-number">{stats.overall_statistics.average_rating.toFixed(2)}</p>
          </div>
          <div className="stat-card">
            <h3>Rating Range</h3>
            <p className="stat-number">{stats.overall_statistics.min_rating} - {stats.overall_statistics.max_rating}</p>
          </div>
        </div>
      </div>

      {/* Statistics by Summary */}
      <div className="summary-stats-section">
        <h2>Statistics by Summary</h2>
        <table className="data-table">
          <thead>
            <tr>
              <th>Summary ID</th>
              <th>Total Ratings</th>
              <th>Average Rating</th>
              <th>Min Rating</th>
              <th>Max Rating</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(stats.summary_statistics).map(([summaryId, summaryStats]) => (
              <tr key={summaryId}>
                <td>Summary {summaryId}</td>
                <td>{summaryStats.total_ratings}</td>
                <td>{summaryStats.average_rating.toFixed(2)}</td>
                <td>{summaryStats.min_rating}</td>
                <td>{summaryStats.max_rating}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Rating Distribution */}
      <div className="distribution-section">
        <h2>Overall Rating Distribution</h2>
        <table className="data-table">
          <thead>
            <tr>
              <th>Rating</th>
              <th>Count</th>
              <th>Percentage</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(stats.distribution).map(([rating, count]) => (
              <tr key={rating}>
                <td>{rating}</td>
                <td>{count}</td>
                <td>{((count / stats.overall_statistics.total_ratings) * 100).toFixed(1)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Individual Submissions */}
      <div className="submissions-section">
        <h2>Individual Form Submissions</h2>
        <div className="submissions-container">
          {stats.individual_submissions.map((submission, index) => (
            <div key={submission.session_id} className="submission-card">
              <div 
                className="submission-header" 
                onClick={() => toggleSession(submission.session_id)}
                style={{ cursor: 'pointer', backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '5px', marginBottom: '10px' }}
              >
                <h3>
                  Submission #{index + 1} 
                  <span style={{ fontSize: '14px', color: '#666', marginLeft: '10px' }}>
                    (Session Average: {submission.session_average.toFixed(2)})
                  </span>
                </h3>
                <p style={{ margin: '5px 0', fontSize: '14px', color: '#888' }}>
                  Submitted: {new Date(submission.submitted_at).toLocaleString()}
                </p>
                <p style={{ margin: '0', fontSize: '12px', color: '#aaa' }}>
                  Session ID: {submission.session_id}
                </p>
                <span style={{ float: 'right', fontSize: '18px' }}>
                  {expandedSessions.has(submission.session_id) ? '▼' : '▶'}
                </span>
              </div>
              
              {expandedSessions.has(submission.session_id) && (
                <div className="submission-details">
                  <table className="data-table" style={{ width: '100%' }}>
                    <thead>
                      <tr>
                        <th>Summary</th>
                        <th>Original Text</th>
                        <th>AI Summary</th>
                        <th>Rating</th>
                      </tr>
                    </thead>
                    <tbody>
                      {submission.ratings.map((rating) => (
                        <tr key={rating.rating_id}>
                          <td>Summary {rating.summary_id}</td>
                          <td className="text-cell" style={{ maxWidth: '300px', wordWrap: 'break-word' }}>
                            {rating.prompt_text.substring(0, 200)}
                            {rating.prompt_text.length > 200 && '...'}
                          </td>
                          <td className="text-cell" style={{ maxWidth: '300px', wordWrap: 'break-word' }}>
                            {rating.ai_summary}
                          </td>
                          <td>
                            <span className={`rating-badge rating-${rating.rating_value}`}>
                              {rating.rating_value}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
