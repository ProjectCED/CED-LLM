import React, { useState } from 'react'; 
import './ClassificationSelection.css';
import BlueprintDropdown from './BlueprintDropdown';

const ClassificationSelection = ({ onSelectClassification, onSelectBlueprint }) => {
  const [selectedClassification, setSelectedClassification] = useState(null); // Track which button is selected
  const [selectedBlueprint, setSelectedBlueprint] = useState('');

   // Sample blueprints array to populate the dropdown
  const blueprints = [
    'Blueprint 1',
    'Blueprint 2',
    'Blueprint 3', 
  ];

  // Function to handle the button click and update the selected classification
  const handleButtonClick = (classification)=> {
    setSelectedClassification(classification);
    onSelectClassification(classification); // Pass the selected classification back to MultiStepForm
  };

  // Function to handle selection of a blueprint from the dropdown
  const handleBlueprintSelect = (blueprint) => {
    setSelectedBlueprint(blueprint);
    onSelectBlueprint(blueprint);
  };

  
  return (
    <div className="classification-selection">
      <p>
        Next, choose how you would like your dataset to be classified. If you're analyzing
        this type of data for the first time, it's recommended to try the default
        classification. If you're satisfied with the results, you can save the classification as a
        blueprint and use it next time, for example, on a larger dataset of the same topic.
      </p>
      <p>
        Alternatively, you can now use previously saved blueprints or define directly how you want the data to be classified.
      </p>

      <div className="button-container">
        <button
          className={`selection-button ${selectedClassification === 'Default Classification' ? 'selected' : ''}`}
          onClick={() => handleButtonClick('Default Classification')}
        >
          Default classification
        </button>
        <button
          className={`selection-button ${selectedClassification === 'Saved Classification' ? 'selected' : ''}`}
          onClick={() => handleButtonClick('Saved Classification')}
        >
          Saved model classification
        </button>
        <button
          className={`selection-button ${selectedClassification === 'Created Classification' ? 'selected' : ''}`}
          onClick={() => handleButtonClick('Created Classification')}
        >
          Create classification
        </button>
      </div>

       {/* Conditionally render the BlueprintDropdown if Saved Classification is selected */}
      {selectedClassification === 'Saved Classification' && (
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