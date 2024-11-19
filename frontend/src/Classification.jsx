import React from 'react';
import MultiStepForm from './MultiStepForm';
import './Classification.css';


const Classification = ({ projects, setProjects}) => {
  return (
    <div className="Classification">
      <p className="classification-heading">
        CED-LLM offers a streamlined process for classifying text data using AI technology. The interface provides four key steps to guide you through the classification process.
      </p>
      <MultiStepForm projects={projects} setProjects={setProjects}/>
    </div>
  );
};

export default Classification;