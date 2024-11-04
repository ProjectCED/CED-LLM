import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import FileDownload from './FileDownload'; // Step 1 component
import ClassificationSelection from './ClassificationSelection'; // Step 2 component
import AISelection from './AISelection'; // Step 3 component
import './MultiStepForm.css';


const MultiStepForm = () => {
  // State variables to track the current step and selections
  const [currentStep, setCurrentStep] = useState(1); 
  const [selectedFiles, setSelectedFiles] = useState([]); 
  const [copiedText, setCopiedText] = useState(''); 
  const [selectedClassification, setSelectedClassification] = useState(null); 
  const [selectedAI, setSelectedAI] = useState(null); 
  const [selectedBlueprint, setSelectedBlueprint] = useState(null);
  const [stepCompleted, setStepCompleted] = useState(0); 
  const [isEditing, setIsEditing] = useState(false);
  const [customClassificationText, setCustomClassificationText] = useState('');
  
  const navigate = useNavigate(); // Hook for navigation

  // Update selected files state
  const handleFileUpload = (files) => {
    if (files.length > 0) {
      setSelectedFiles(files);
      setCopiedText('');
    } else {
      setSelectedFiles([]);
    }
  };

  // Update copied text state
  const handleTextChange = (text) => {
    if (text.trim() !== '') {
      setCopiedText(text);
      setSelectedFiles([]);
    } else {
      setCopiedText('');
    }
  };

  // Handle analyze button click, navigate to the projects page
  const handleAnalyze = () => {
    navigate('/app/projects');
  };

  const allStepsCompleted = stepCompleted > 3;
  
  // Function to go to the next step with validation
  const nextStep = () => {
    // Validation for step 1: Check if files or text are provided
    if (currentStep === 1) {
      if (selectedFiles.length === 0 && copiedText.trim() === '') {
        alert('Please upload one file or enter some text.');
        return;
      }
    }

    // Validation for step 2: Ensure a classification option is selected
    if (currentStep === 2) {
      if (!selectedClassification) {
        alert('Please select a classification option.');
        return;
      }
      // Check if "Saved Blueprint" requires a blueprint selection
      if (selectedClassification === 'Saved Blueprint' && !selectedBlueprint) {
        alert('Please select a saved blueprint.');
        return;
      }

      // Check if "Created Blueprint" requires custom blueprint text input
      if (selectedClassification === 'Created Blueprint' && customClassificationText.trim() === '') {
        alert('Please enter a blueprint for "Created Blueprint".');
        return;
      }
    }

    // Validation for step 3: Ensure an AI option is selected
    if (currentStep === 3) {
      if (!selectedAI) {
        alert('Please select an AI option.');
        return;
      }
    }

    const newStep = currentStep + 1;
    setCurrentStep(newStep);
    setStepCompleted(Math.max(stepCompleted, newStep));
  };

  // Function to update selected classification in step 2
  const handleClassificationSelection = (classification) => {
    setSelectedClassification(classification);
  };

  // Function to update selected AI in step 3
  const handleAISelection = (ai) => {
    setSelectedAI(ai);
  };

  // Function to update selected blueprint in step 2
  const handleBlueprintSelection = (blueprint) => {
    setSelectedBlueprint(blueprint);
  };

  const handleCustomTextChange = (text) => {
    setCustomClassificationText(text);
  };

  const handleEditClick = (step) => {
    // Prevent editing another step if currently in editing mode
    if (isEditing) {
      alert('Please save or cancel the current editing step before editing another step.');
      return;
    }

    setCurrentStep(step);
    setIsEditing(true);
  };

  const handleSaveClick = () => {
    // Validation for step 2: Ensure a classification option is selected
    if (currentStep === 2) {
      if (!selectedClassification) {
        alert('Please select a classification option.');
        return;
      }
      // Check if "Saved Blueprint" requires a blueprint selection
      if (selectedClassification === 'Saved Blueprint' && !selectedBlueprint) {
        alert('Please select a a saved blueprint.');
        return;
      }
      // Check if "Created Blueprint" requires custom blueprint text input
      if (selectedClassification === 'Created Blueprint' && customClassificationText.trim() === '') {
        alert('Please enter a blueprint for "Created Blueprint".');
        return;
      }
    }

    setIsEditing(false); // Close the edit mode
    setCurrentStep(4);
  };

  const resetSelections = () => {
    setSelectedFiles([]); 
    setCopiedText(''); 
    setSelectedClassification(null);
    setSelectedAI(null);
    setSelectedBlueprint(null);
  };

  return (
    <div className="multi-step-form">
      {/* Step 1: File upload or copy-paste text */}
      <div className="step">
        <div className="step-header">
          <h2 className={`step-title ${currentStep === 1 ? 'active' : ''}`}>
            1. File Upload or Copy Paste Text
          </h2>
          {allStepsCompleted && currentStep !== 1 && (
            <button className="edit-button" onClick={() => handleEditClick(1)}>
              Edit
            </button>
          )}
        </div>
        {currentStep === 1 && (
          <div className="step-content">
            <FileDownload 
              onFileUpload={handleFileUpload}
              onTextChange={handleTextChange}
              isEditing={isEditing} // Pass isEditing prop to FileDownload
            />
            {isEditing ? (
              <button className="multiform-save-button" onClick={handleSaveClick}>Save</button>
            ) : (
              <button className="next-button" onClick={nextStep}>Next</button>
            )}
          </div>
        )}
        {stepCompleted >= 1 && selectedFiles.length > 0 && (
          <div className="step-summary">
            <p>Selected Files:</p>
            <div className="file-list">
              {selectedFiles.map((file, index) => (
                <div key={index} className="file-item">
                  {file.name}
                </div>
              ))}
            </div>
          </div>
        )}
        {stepCompleted >= 1 && copiedText.trim() !== '' && (
          <div className="step-summary">
            <p>Text has been copied</p>
          </div>
        )}
      </div>

      {/* Step 2: Blueprint Selection */}
      <div className="step">
        <div className="step-header">
          <h2 className={`step-title ${currentStep === 2 ? 'active' : ''}`}>
            2. Blueprint Selection
          </h2>
          {allStepsCompleted && currentStep !== 2 && (
            <button className="edit-button" onClick={() => handleEditClick(2)}>
              Edit
            </button>
          )}
        </div>
        {currentStep === 2 && (
          <div className="step-content">
            <ClassificationSelection
              selectedClassification={selectedClassification}
              onSelectClassification={handleClassificationSelection} 
              onSelectBlueprint={handleBlueprintSelection}
              isLocked={isEditing} // Pass isLocked prop to ClassificationSelection
              onCustomTextChange={handleCustomTextChange}
            />
            {isEditing ? (
              <button className="multiform-save-button" onClick={handleSaveClick}>Save</button>
            ) : (
              <button className="next-button" onClick={nextStep}>Next</button>
            )}
          </div>
        )}
        {stepCompleted >= 2 && (
          <div className="step-summary">
            <p>{selectedClassification}</p>
            {selectedBlueprint && <p>{selectedBlueprint}</p>}
            {customClassificationText && <p>{customClassificationText}</p>}
          </div>
        )}
      </div>

      {/* Step 3: AI selection */}
      <div className="step">
        <div className="step-header">
          <h2 className={`step-title ${currentStep === 3 ? 'active' : ''}`}>
            3. AI Selection
          </h2>
          {allStepsCompleted && currentStep !== 3 && (
            <button className="edit-button" onClick={() => handleEditClick(3)}>
              Edit
            </button>
          )}
        </div>
        {currentStep === 3 && (
          <div className="step-content">
            <AISelection selectedAI={selectedAI} onSelectAI={handleAISelection} isLocked={isEditing} />
            {isEditing ? (
              <button className="multiform-save-button" onClick={handleSaveClick}>Save</button>
            ) : (
              <button className="next-button" onClick={nextStep}>Next</button>
            )}
          </div>
        )}
        {stepCompleted >= 3 && (
          <div className="step-summary">
            <p>{selectedAI}</p>
          </div>
        )}
      </div>

      {/* Show Analyze button disabled until all steps are completed */}
      <div className="analyze-section">
        <button 
          className="analyze-button" 
          onClick={handleAnalyze} 
          disabled={!allStepsCompleted}
        >
          Analyze
        </button>
      </div>
    </div>
  );
};

export default MultiStepForm;