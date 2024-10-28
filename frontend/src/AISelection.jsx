import React, { useState, useEffect } from 'react';
import './AISelection.css';  

const AISelection = ({ selectedAI, onSelectAI }) => {
  const [localSelectedAI, setLocalSelectedAI] = useState(selectedAI || '');

  useEffect(() => {
    setLocalSelectedAI(selectedAI);
  }, [selectedAI]);

  const handleAISelection = (ai) => {
    setLocalSelectedAI(ai);
    onSelectAI(ai);
  };

  return (
    <div className="ai-selection-container">
      <h2>Choose AI for analysis</h2>
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
