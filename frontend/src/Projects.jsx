import React from 'react';
import './Projects.css';

const Projects = () => {
  return (
    <div className="projects-container">
      <h1>Hello World from Projects!</h1>
      <div className="results-box">
      <h2>Dog Show Success Analysis Report</h2>
        <p><strong>Date:</strong> March 12–13</p>

        <h3>Top Recommended Shows</h3>
        <ul>
          <li>
            <strong>National Canine Championship – Munich</strong><br />
            <strong>Date:</strong> March 12–13<br />
            <strong>Judge Preference Match:</strong> 85%<br />
            <em>Remarks:</em> Consistently high placements for German Shepherds, judge favors working breeds.
          </li>
          <li>
            <strong>Regional Dog Show – Hamburg</strong><br />
            <strong>Date:</strong> April 22<br />
            <strong>Judge Preference Match:</strong> 78%<br />
            <em>Remarks:</em> Smaller show, ideal for first-time participants with breed-friendly judges.
          </li>
        </ul>

        <h3>Judge Highlights</h3>
        <ul>
          <li><strong>Judge A. Müller:</strong> 9.2 avg rating for German Shepherds, prefers structure and obedience.</li>
          <li><strong>Judge K. Weber:</strong> 8.9 avg rating, favors large, well-trained breeds.</li>
        </ul>

        <h3>Key Takeaways</h3>
        <ul>
          <li>Focus on shows with high judge preference matches.</li>
          <li>Start with a moderate-sized show for better odds and visibility.</li>
        </ul>
      </div>

      <div className="button-container-projects">
        <button className="download-button">Download result as pdf</button>
        <button className="blueprint-button">Save as blueprint</button>
      </div>
    </div>
  );
};

export default Projects;