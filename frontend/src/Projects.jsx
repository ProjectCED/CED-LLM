import React, {useState} from 'react';
import './Projects.css';

const Projects = () => {
  const [result, setResult] = useState('Results from analysis here'); //tämä näkyy

  const handleAnalyze = async () => { //tämä ei toimi
    try {
      const formData = new FormData();
      formData.append('ced-testi', new File(["ced-testi"], "ced-testi"));

      const response = await fetch('http://localhost:5000/test_analyze', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setResult(data.result); // Set result
    } catch (error) {
      setResult('Error: ' + error.message);
    }
  };

  return (
    <div className="projects-container">
      <h1>Hello World from Projects!</h1>
      <div className="results-box">
        {result}
      </div>

      <div className="button-container-projects">
        <button className="download-button">Download result as pdf</button>
        <button className="blueprint-button">Save as blueprint</button>
      </div>
    </div>
  );
};

export default Projects;