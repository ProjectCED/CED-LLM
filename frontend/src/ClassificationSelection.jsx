import React from 'react';
import { useNavigate } from 'react-router-dom';
import './ClassificationSelection.css';

const ClassificationSelection = () => {

  const navigate = useNavigate();

  // Function to handle navigation to the default classification route
  const handleDefaultClassification = () => {
    navigate('/app/classification/default-classification');
  };

  return (
    <div className="classification-selection">
      <h2>Classification selection</h2>
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
        <button className="selection-button"
        onClick={handleDefaultClassification}
        >
          Default classification
        </button>
        <button className="selection-button">Saved model classification</button>
        <button className="selection-button">Create classification</button>
      </div>
    </div>
  );
};

export default ClassificationSelection;