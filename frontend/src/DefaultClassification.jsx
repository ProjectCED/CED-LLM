import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './DefaultClassification.css';  

const AISelection = () => {
     // State to track which AI option is selected, initially no option is selected
  const [selectedAI, setSelectedAI] = useState('');
  const navigate = useNavigate();  

  // Function to handle AI selection (Mistral or OpenAI)
  const handleAISelection = (ai) => {
    setSelectedAI(ai);
  };

   // Function to handle when the "Analyze" button is clicked
  const handleAnalyze = () => {
    if (selectedAI) {
      console.log(`Analyzing with ${selectedAI}`);
      navigate('/app/projects');
    } else {
      alert('Please select an AI option!');
    }
  };

  return (
    <div className="ai-selection-container">
      <h2>Choose AI for analysis</h2>
      <div className="ai-options">
        <button
          className={`ai-option ${selectedAI === 'Mistral' ? 'selected' : ''}`}
          onClick={() => handleAISelection('Mistral')}
        >
          Mistral
        </button>
        <button
          className={`ai-option ${selectedAI === 'OpenAI' ? 'selected' : ''}`}
          onClick={() => handleAISelection('OpenAI')}
        >
          OpenAI
        </button>
      </div>
      <button className="analyze-button" onClick={handleAnalyze}>
        Analyze &rarr;
      </button>
    </div>
  );
};

export default AISelection;