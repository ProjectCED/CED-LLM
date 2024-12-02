import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './DefaultClassification.css';  

/**
 * AISelection component allows the user to select an AI option (Mistral or OpenAI) 
 * for analysis. Once the AI is selected, the user can click the "Analyze" button 
 * to navigate to the projects page.
 * 
 * @component
 * @returns {JSX.Element} The rendered AISelection component with AI options buttons 
 * and an "Analyze" button that navigates to the next page.
 */
const AISelection = () => {
  /**
   * State to track which AI option is selected. 
   * Initially, no option is selected.
   * @type {string}
   */
  const [selectedAI, setSelectedAI] = useState('');

  /**
   * `useNavigate` hook from React Router to handle navigation to another page.
   * @type {Function}
   */
  const navigate = useNavigate();  

  /**
   * Handles the selection of an AI option (Mistral or OpenAI).
   * Updates the state `selectedAI` to the chosen option.
   * 
   * @param {string} ai - The selected AI option, either 'Mistral' or 'OpenAI'.
   */
  const handleAISelection = (ai) => {
    setSelectedAI(ai);
  };

  /**
   * Handles the click event for the "Analyze" button. 
   * If an AI is selected, navigates to the '/app/projects' route.
   * Otherwise, shows an alert prompting the user to select an AI option.
   */
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