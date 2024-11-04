import React, { useEffect, useState } from 'react';
import './Projects.css';
import { useLocation } from 'react-router-dom';

const Projects = () => {
  const { state } = useLocation();
  const [ result, setResult ] = useState(null);
  const [ loading, setLoading ] = useState(true);

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

    let data = await response.json();
    data = JSON.stringify(data, null, 0).replace(/\\n/g, '<br />')

    setResult(data);
    setLoading(false);
  }

  useEffect(() => {
    analyzeFile();
  }, []);

  return (
    <div className="projects-container">
      <h2>Analysis Results</h2>
      {loading ? (
        <p>Analyzing...</p>
      ) : (
        <div
          style={{ whiteSpace: 'pre-wrap', textAlign: 'justify'}}
          dangerouslySetInnerHTML={{ __html: result }}/>
      )}
    </div>
  );
};

export default Projects;