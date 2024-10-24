import React from 'react';
import './Projects.css';

const Projects = () => {
  return (
    <div className="projects-container">
      <h1>Hello World from Projects!</h1>
      <div className="results-box">
        Results from analysis here
      </div>

      <div className="button-container-projects">
        <button className="download-button">Download result as pdf</button>
        <button className="blueprint-button">Save as blueprint</button>
      </div>
    </div>
  );
};

export default Projects;