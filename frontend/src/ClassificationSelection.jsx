import React, { useState, useEffect } from 'react';
import './ClassificationSelection.css';
import BlueprintDropdown from './BlueprintDropdown';
import { getBlueprints } from './utils';

/**
 * ClassificationSelection component is responsible for displaying the classification options for selecting 
 * an automatic blueprint, a saved blueprint, or creating a custom blueprint. It includes handling user input 
 * and managing the local state related to classifications, blueprints, and custom text.
 * 
 * @component
 * @param {Object} props - The component's props.
 * @param {string} props.selectedClassification - The currently selected classification (e.g., "Automatic Blueprint", "Saved Blueprint", "Created Blueprint").
 * @param {Function} props.onSelectClassification - Callback function to handle the selection of a classification.
 * @param {Function} props.onSelectBlueprint - Callback function to handle the selection of a blueprint.
 * @param {Function} props.onCustomTextChange - Callback function to handle changes in custom text input.
 * @returns {JSX.Element} The rendered ClassificationSelection component with buttons for classification selection, 
 * blueprint dropdown, and custom text input fields.
 */
const ClassificationSelection = ({ selectedClassification, onSelectClassification, onSelectBlueprint, onCustomTextChange }) => {
  /**
   * Local state to keep track of the currently selected classification.
   * @type {string}
   */
  const [localSelectedClassification, setLocalSelectedClassification] = useState(selectedClassification || '');

   /**
   * Local state to keep track of the selected blueprint.
   * @type {Object|null}
   */
  const [selectedBlueprint, setSelectedBlueprint] = useState(null);

  /**
   * Local state to keep track of the available blueprints.
   * @type {Array<Object>}
   */
  const [blueprints, setBlueprints] = useState([]);

  /**
   * Local state to store the custom text entered for creating a new blueprint.
   * @type {string}
   */
  const [customText, setCustomText] = useState('');

  /**
   * Effect hook that runs when the `selectedClassification` prop changes. 
   * It updates the local classification state and fetches available blueprints.
   */
  useEffect(() => {
    setLocalSelectedClassification(selectedClassification);
    getBlueprints().then((bps) => {
      setBlueprints(bps);
    });
  }, [selectedClassification]);

  /**
   * Handles button click to select a classification.
   * 
   * @param {string} classification - The classification selected by the user (e.g., 'Automatic Blueprint', 'Saved Blueprint', 'Created Blueprint').
   */
  const handleButtonClick = (classification) => {
    setLocalSelectedClassification(classification);
    onSelectClassification(classification);
  
    // If classification is not 'Saved Classification', clears selected blueprint
  if (classification !== 'Saved Blueprint') {
    setSelectedBlueprint(null);
    onSelectBlueprint(null); 
  }

  if (classification !== 'Created Blueprint') {
    setCustomText('');
    onCustomTextChange(''); 
  }

  };

  /**
   * Handles blueprint selection in the BlueprintDropdown component.
   * 
   * @param {number} blueprintIndex - The index of the selected blueprint in the `blueprints` array.
   */
  const handleBlueprintSelect = (blueprintIndex) => {
    const blueprint = blueprints[blueprintIndex];
    setSelectedBlueprint(blueprint);
    onSelectBlueprint(blueprint);
  };

  /**
   * Handles changes in the custom text input field for creating a new blueprint.
   * 
   * @param {React.ChangeEvent<HTMLInputElement>} event - The change event triggered by the input field.
   */
  const handleCustomTextChange = (event) => {
    const text = event.target.value;
    setCustomText(text);
    onCustomTextChange(text); // Pass the text back to the parent component
  };

  return (
    <div className="classification-selection">
      <h2>
        Next, choose how you would like your dataset to be classified. If you're analyzing
        this type of data for the first time, it's recommended to try the Automatic blueprint. 
      </h2>
      <h2>
        Alternatively, you can now use previously saved blueprints or define directly how you want the data to be classified.
      </h2>
      <div className="button-container">
        <button
          className={`selection-button ${localSelectedClassification === 'Automatic Blueprint' ? 'selected' : ''}`}
          onClick={() => handleButtonClick('Automatic Blueprint')}
        >
          Automatic Blueprint
        </button>
        <button
          className={`selection-button ${localSelectedClassification === 'Saved Blueprint' ? 'selected' : ''}`}
          onClick={() => handleButtonClick('Saved Blueprint')}
        >
          Saved Blueprint
        </button>
        <button
          className={`selection-button ${localSelectedClassification === 'Created Blueprint' ? 'selected' : ''}`}
          onClick={() => handleButtonClick('Created Blueprint')}
        >
          Create Blueprint
        </button>
      </div>

      {localSelectedClassification === 'Saved Blueprint' && (
        <BlueprintDropdown
          key={localSelectedClassification} 
          blueprints={blueprints}
          selectedBlueprint={selectedBlueprint}
          onSelectBlueprint={handleBlueprintSelect}
        />
      )}

      {localSelectedClassification === 'Created Blueprint' && (
        <div className="custom-text-input">
          <input
            type="text"
            placeholder="Enter custom blueprint"
            value={customText}
            onChange={handleCustomTextChange}
          />
        </div>
      )}
    </div>
  );
};

export default ClassificationSelection;
