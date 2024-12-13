import React, { useState, useEffect } from 'react';
import './AISelection.css'; 
import { testMistral } from './utils'; 

/**
 * AISelection component allows users to select an AI model from a set of predefined options.
 * Displays buttons for available AI models and highlights the selected option.
 *
 * @component
 * @param {Object} props - The props passed to the component.
 * @param {string} props.selectedAI - The AI model initially selected. Can be "Mistral", "OpenAI", or an empty string.
 * @param {Function} props.onSelectAI - Callback function triggered when an AI model is selected.
 *        Receives the name of the selected AI model as an argument.
 */
const AISelection = ({ selectedAI, onSelectAI }) => {

  /**
   * Local state to track the currently selected AI model.
   * Initialized with `selectedAI` prop or an empty string if not provided.
   * @type {string}
   */
  const [localSelectedAI, setLocalSelectedAI] = useState(selectedAI || '');

  /**
   * Updates the local state (`localSelectedAI`) whenever the `selectedAI` prop changes.
   */
  useEffect(() => {
    setLocalSelectedAI(selectedAI);
  }, [selectedAI]);

  /**
   * Handles the selection of an AI model.
   * Updates the local state and calls the `onSelectAI` prop function.
   *
   * @param {string} ai - The name of the AI model selected.
   */
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
