import React, { useEffect, useState } from 'react';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = () => {
      fetch('/api/ratings/stats')
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

  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;
  if (!stats) return <div>Loading...</div>;

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Survey Dashboard</h1>
      <h2>Statistics</h2>
      <p>Total Ratings: {stats.statistics.total_ratings}</p>
      <p>Average Rating: {stats.statistics.average_rating.toFixed(2)}</p>
      <p>Min Rating: {stats.statistics.min_rating}</p>
      <p>Max Rating: {stats.statistics.max_rating}</p>

      <h2>Distribution</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Rating</th>
            <th>Count</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(stats.distribution).map(([rating, count]) => (
            <tr key={rating}>
              <td>{rating}</td>
              <td>{count}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Recent Submissions</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Prompt</th>
            <th>AI Summary</th>
            <th>Rating</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          {stats.recent_submissions.map(item => (
            <tr key={item.rating_id}>
              <td>{item.prompt_text}</td>
              <td>{item.ai_summary}</td>
              <td>{item.rating_value}</td>
              <td>{item.created_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}