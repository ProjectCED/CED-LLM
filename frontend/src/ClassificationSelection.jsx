import React, { useState, useEffect } from 'react';
import './ClassificationSelection.css';
import BlueprintDropdown from './BlueprintDropdown';
import { getBlueprints } from './utils';

const ClassificationSelection = ({ selectedClassification, onSelectClassification, onSelectBlueprint, onCustomTextChange }) => {
  // Local state to keep track of the currently selected classification,
  // selected blueprint and custom input text
  const [localSelectedClassification, setLocalSelectedClassification] = useState(selectedClassification || '');
  const [selectedBlueprint, setSelectedBlueprint] = useState(null);
  const [blueprints, setBlueprints] = useState([]);
  const [customText, setCustomText] = useState('');

  // Update localSelectedClassification if selectedClassification prop changes
  useEffect(() => {
    setLocalSelectedClassification(selectedClassification);
    getBlueprints().then((bps) => {
      setBlueprints(bps);
    });
  }, [selectedClassification]);

  // Handles classification button click
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

  // Handles blueprint selection in the BlueprintDropdown component
  const handleBlueprintSelect = (blueprintIndex) => {
    const blueprint = blueprints[blueprintIndex];
    setSelectedBlueprint(blueprint);
    onSelectBlueprint(blueprint);
  };

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
