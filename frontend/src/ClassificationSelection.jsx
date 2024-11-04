import React, { useState, useEffect } from 'react';
import './ClassificationSelection.css';
import BlueprintDropdown from './BlueprintDropdown';

const ClassificationSelection = ({ selectedClassification, onSelectClassification, onSelectBlueprint, onCustomTextChange }) => {
  // Local state to keep track of the currently selected classification,
  // selected blueprint and custom input text
  const [localSelectedClassification, setLocalSelectedClassification] = useState(selectedClassification || '');
  const [selectedBlueprint, setSelectedBlueprint] = useState('');
  const [customText, setCustomText] = useState('');

  // Update localSelectedClassification if selectedClassification prop changes
  useEffect(() => {
    setLocalSelectedClassification(selectedClassification);
  }, [selectedClassification]);

  // Array of blueprint options available for selection
  const blueprints = ['Blueprint 1', 'Blueprint 2', 'Blueprint 3'];

  // Handles classification button click
  const handleButtonClick = (classification) => {
    setLocalSelectedClassification(classification);
    onSelectClassification(classification);
  
    // If classification is not 'Saved Classification', clears selected blueprint
  if (classification !== 'Saved Classification') {
    setSelectedBlueprint('');
    onSelectBlueprint(''); 
  }

  if (classification !== 'Created Classification') {
    setCustomText('');
    onCustomTextChange(''); 
  }

  };

  // Handles blueprint selection in the BlueprintDropdown component
  const handleBlueprintSelect = (blueprint) => {
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
        this type of data for the first time, it's recommended to try the default
        classification. If you're satisfied with the results, you can save the classification as a
        blueprint and use it next time, for example, on a larger dataset of the same topic.
      </h2>
      <h2>
        Alternatively, you can now use previously saved blueprints or define directly how you want the data to be classified.
      </h2>
      <div className="button-container">
        <button
          className={`selection-button ${localSelectedClassification === 'Default Classification' ? 'selected' : ''}`}
          onClick={() => handleButtonClick('Default Classification')}
        >
          Default classification
        </button>
        <button
          className={`selection-button ${localSelectedClassification === 'Saved Classification' ? 'selected' : ''}`}
          onClick={() => handleButtonClick('Saved Classification')}
        >
          Saved model classification
        </button>
        <button
          className={`selection-button ${localSelectedClassification === 'Created Classification' ? 'selected' : ''}`}
          onClick={() => handleButtonClick('Created Classification')}
        >
          Create classification
        </button>
      </div>

      {localSelectedClassification === 'Saved Classification' && (
        <BlueprintDropdown
          key={localSelectedClassification} 
          blueprints={blueprints}
          selectedBlueprint={selectedBlueprint}
          onSelectBlueprint={handleBlueprintSelect}
        />
      )}

      {localSelectedClassification === 'Created Classification' && (
        <div className="custom-text-input">
          <input
            type="text"
            placeholder="Enter custom classification"
            value={customText}
            onChange={handleCustomTextChange}
          />
        </div>
      )}
    </div>
  );
};

export default ClassificationSelection;
