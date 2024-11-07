import React, { useEffect, useState } from 'react';
import './Projects.css';
import { useLocation } from 'react-router-dom';

const Projects = () => {
  const { state } = useLocation();
  const [ result, setResult ] = useState(null);
  const [ loading, setLoading ] = useState(true);

  const analyzeFile = async () => {
    if (state === undefined || state === null) {
      const storedResult = localStorage.getItem('result');
      if (storedResult !== null) {
        setResult(storedResult);
        setLoading(false);
      }
      return;
    }
    const filename = state['filename'];

    // Replace 'test_analyze' with 'analyze_file' for actual analysis using OpenAI API
    const response = await fetch('http://127.0.0.1:5000/test_analyze', {
      method: 'POST',
      body: filename,
    });

    let data = await response.json();
    data = data.replace(/\\n/g, '<br />')
    localStorage.setItem('result', data);
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