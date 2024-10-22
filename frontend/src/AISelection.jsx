import React, { useState } from 'react';
import './AISelection.css';  

const AISelection = ({ onSelectAI }) => {
     // State to track which AI option is selected, initially no option is selected
  const [selectedAI, setSelectedAI] = useState('');  

  // Function to handle AI selection
  const handleAISelection = (ai) => {
    setSelectedAI(ai);
    onSelectAI(ai); // Pass the selected AI back to MultiStepForm
  };

   // Function to handle when the "Analyze" button is clicked
  const handleAnalyze = () => {
    if (selectedAI) {
      console.log(`Analyzing with ${selectedAI}`);
      
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
      
    </div>
  );
};

export default AISelection;