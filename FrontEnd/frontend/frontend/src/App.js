import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import SummaryRatingForm from './components/SummaryRatingForm';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>EHR Summary Rating System</h1>
          <nav className="nav-links">
            <Link to="/" className="nav-link">Rating Form</Link>
            <Link to="/dashboard" className="nav-link">Admin Dashboard</Link>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<SummaryRatingForm />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;