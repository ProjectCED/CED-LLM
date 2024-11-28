import React, { useState, useEffect } from 'react';
import './AISelection.css';  

const AISelection = ({ selectedAI, onSelectAI }) => {
  // Local state to keep track of the currently selected AI model
  const [localSelectedAI, setLocalSelectedAI] = useState(selectedAI || '');

  // useEffect to update localSelectedAI if the selectedAI prop changes
  useEffect(() => {
    setLocalSelectedAI(selectedAI);
  }, [selectedAI]);

  // Handles the selection of an AI model
  // Sets the local state and calls the onSelectAI function from props
  const handleAISelection = (ai) => {
    setLocalSelectedAI(ai);
    onSelectAI(ai);
  };

  return (
    <div className="ai-selection-container">
      <h2>Choose the appropriate AI solution to carry out the analysis.</h2>
      <div className="ai-options">
        <button
          className={`ai-option ${localSelectedAI === 'Mistral' ? 'selected' : ''}`}
          onClick={() => handleAISelection('Mistral')}
        >
          Mistral
        </button>
        <button
          className={`ai-option ${localSelectedAI === 'OpenAI' ? 'selected' : ''}`}
          onClick={() => handleAISelection('OpenAI')}
        >
          OpenAI
        </button>
      </div>
    </div>
  );
};

export default AISelection;
