import React, { useEffect, useState } from 'react';
import './Projects.css';
import { useLocation } from 'react-router-dom';
import { analyzeUploadedFile } from './utils';

const Projects = () => {
  const { state } = useLocation();
  const [ result, setResult ] = useState(null);
  const [ loading, setLoading ] = useState(true);

  const loadAnalysisResults = async () => {
    // If state isn't set, try loading from local storage
    if (state === undefined || state === null) {
      /*
        Even if no file has been picked for analysis,
        we can still display the results from the last analysis
        from local storage.
      */
      const storedResult = localStorage.getItem('result');
      if (storedResult !== null) {
        setResult(storedResult);
        setLoading(false);
      }
      /* 
        At this point, either there is a file to analyze or
        it has been loaded from local storage, either way,
        we can't analyze files at this point.
      */
      return;
    }

    // If state IS set, then we have a new file to analyze
    const filename = state['filename'];

    const data = await analyzeUploadedFile(filename);

    localStorage.setItem('result', data);
    setResult(data);
    setLoading(false);
  }

  useEffect(() => {
    loadAnalysisResults();
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