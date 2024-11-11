import React from 'react';
import MultiStepForm from './MultiStepForm';
import './Classification.css';


const Classification = () => {
  return (
    <div className="Classification">
      <p className="classification-heading">
        CED-LLM offers a streamlined process for classifying text data using AI technology. The interface provides three key steps to guide you through the classification process.
      </p>
      <MultiStepForm />
    </div>
  );
};

export default Classification;