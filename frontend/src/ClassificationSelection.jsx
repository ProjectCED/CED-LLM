import React, { useState } from 'react'; 
import './ClassificationSelection.css';

const ClassificationSelection = ({ onSelectClassification }) => {
  const [selectedClassification, setSelectedClassification] = useState(null); // Track which button is selected

  // Function to handle the button click and update the selected classification
  const handleButtonClick = (classification)=> {
    setSelectedClassification(classification);
    onSelectClassification(classification); // Pass the selected classification back to MultiStepForm
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
          className={`selection-button ${selectedClassification === 'default' ? 'selected' : ''}`}
          onClick={() => handleButtonClick('default')}
        >
          Default classification
        </button>
        <button
          className={`selection-button ${selectedClassification === 'saved' ? 'selected' : ''}`}
          onClick={() => handleButtonClick('saved')}
        >
          Saved model classification
        </button>
        <button
          className={`selection-button ${selectedClassification === 'create' ? 'selected' : ''}`}
          onClick={() => handleButtonClick('create')}
        >
          Create classification
        </button>
      </div>
    </div>
  );
};

export default ClassificationSelection;