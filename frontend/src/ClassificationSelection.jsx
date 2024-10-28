import React, { useState, useEffect } from 'react';
import './ClassificationSelection.css';
import BlueprintDropdown from './BlueprintDropdown';

const ClassificationSelection = ({ selectedClassification, onSelectClassification, onSelectBlueprint }) => {
  const [localSelectedClassification, setLocalSelectedClassification] = useState(selectedClassification || '');
  const [selectedBlueprint, setSelectedBlueprint] = useState('');

  useEffect(() => {
    setLocalSelectedClassification(selectedClassification);
  }, [selectedClassification]);

  const blueprints = ['Blueprint 1', 'Blueprint 2', 'Blueprint 3'];

  const handleButtonClick = (classification) => {
    setLocalSelectedClassification(classification);
    onSelectClassification(classification);
  };

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
          blueprints={blueprints}
          selectedBlueprint={selectedBlueprint}
          onSelectBlueprint={handleBlueprintSelect}
        />
      )}
    </div>
  );
};

export default ClassificationSelection;
