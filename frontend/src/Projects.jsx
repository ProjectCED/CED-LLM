import React from 'react';
import './Projects.css';
import { useLocation } from 'react-router-dom';

const Projects = () => {
  const { state } = useLocation();

  const analyzeFile = async () => {
    if (state === undefined || state === null) {
      return;
    }
    else if (!state.hasOwnProperty('filename')) {
      return;
    }

    const filename = state['filename'];

    const response = await fetch('http://127.0.0.1:5000/test_analyze', {
      method: 'POST',
      body: filename,
    });

    const data = await response.json();

    return data;
  }

  analyzeFile();
  return (
    <div className="projects-container">
      <h1>Hello World from Projects!</h1>
    </div>
  );
};

export default Projects;