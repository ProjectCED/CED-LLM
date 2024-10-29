import React, { useState, useEffect } from 'react';
import './ClassificationSelection.css';
import BlueprintDropdown from './BlueprintDropdown';

const ClassificationSelection = ({ selectedClassification, onSelectClassification, onSelectBlueprint }) => {
  // Local state to keep track of the currently selected classification 
  // and selected blueprint 
  const [localSelectedClassification, setLocalSelectedClassification] = useState(selectedClassification || '');
  const [selectedBlueprint, setSelectedBlueprint] = useState('');

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
  };

  // Handles blueprint selection in the BlueprintDropdown component
  const handleBlueprintSelect = (blueprint) => {
    setSelectedBlueprint(blueprint);
    onSelectBlueprint(blueprint);
  };

  return (
    <div className="classification-selection">
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
    </div>
  );
};

export default ClassificationSelection;
