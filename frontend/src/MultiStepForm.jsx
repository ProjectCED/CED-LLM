import React, { useState } from 'react';
import FileDownload from './FileDownload'; // Step 1 component
import ClassificationSelection from './ClassificationSelection'; // Step 2 component
import AISelection from './AISelection'; // Step 3 component
import ProjectSelection from './ProjectSelection'; // Step 4 component
import './MultiStepForm.css';

// EditButton Component
const EditButton = ({ onEditClick, step }) => {
  return (
    <button className="edit-button" onClick={() => onEditClick(step)}>
      Edit
    </button>
  );
};

// SaveButton Component
const SaveButton = ({ onSaveClick }) => {
  return (
    <button className="multiform-save-button" onClick={onSaveClick}>
      Save
    </button>
  );
};

// NextButton Component
const NextButton = ({ onNextClick }) => {
  return (
    <button className="next-button" onClick={onNextClick}>
      Next
    </button>
  );
};

const MultiStepForm = ({ projects, setProjects, setExpanded, setSelectedResult, setBlueprint, setOverlayActive}) => {
  // State variables to track the current step and selections
  const [currentStep, setCurrentStep] = useState(1); 
  const [isEditing, setIsEditing] = useState(false);
  const [stepCompleted, setStepCompleted] = useState(0); 

  // Persistent state
  const [selectedFiles, setSelectedFiles] = useState([]); 
  const [copiedText, setCopiedText] = useState(''); 
  const [selectedClassification, setSelectedClassification] = useState(null); 
  const [selectedAI, setSelectedAI] = useState(null); 
  const [selectedBlueprint, setSelectedBlueprint] = useState(null);
  const [selectedProjectOption, setSelectedProjectOption] = useState(null); 
  const [selectedExistingProject, setSelectedExistingProject] = useState(null);
  const [customClassificationText, setCustomClassificationText] = useState('');
  const [newProjectName, setNewProjectName] = useState('');

  // Temporary state for current step changes
  const [tempFiles, setTempFiles] = useState([]);
  const [tempText, setTempText] = useState('');
  const [tempClassification, setTempClassification] = useState(null);
  const [tempBlueprint, setTempBlueprint] = useState(null);
  const [tempCustomText, setTempCustomText] = useState('');
  const [tempAI, setTempAI] = useState(null);
  const [tempProjectOption, setTempProjectOption] = useState(null);
  const [tempExistingProject, setTempExistingProject] = useState(null);
  const [tempNewProjectName, setTempNewProjectName] = useState('');


  // Function to reset form state
  const resetFormState = () => {

    // Function to reset persistent states
    setCurrentStep(1); 
    setSelectedFiles([]);
    setCopiedText('');
    setSelectedClassification(null);
    setSelectedAI(null);
    setSelectedBlueprint(null);
    setSelectedProjectOption(null);
    setSelectedExistingProject(null);
    setStepCompleted(0); 
    setIsEditing(false);
    setCustomClassificationText('');
    setNewProjectName('');

    // Reset temporay states
    setTempFiles([]);
    setTempText('');
    setTempClassification(null);
    setTempBlueprint(null);
    setTempCustomText('');
    setTempAI(null);
    setTempProjectOption(null);
    setTempExistingProject(null);
    setTempNewProjectName('');
  };

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

   // Update selected temporary files state
   const handleTempFileUpload = (files) => {
    if (files.length > 0) {
      setTempFiles(files);
      setTempText('');
    } else {
      setTempFiles([]);
    }
  };

  // Update temporary copied text state
  const handleTempTextChange = (text) => {
    if (text.trim() !== '') {
      setTempText(text);
      setTempFiles([]);
    } else {
      setTempText('');
    }
  };

  // Handle analyze button click, navigate to the projects page
  const handleAnalyze = async () => {
  //const formdata = new FormData();
  //formdata.append('file', selectedFiles[0]);
  //const response = await fetch('http://127.0.0.1:5000/upload_file', {
    //method: 'POST',
    //body: formdata,
  //});
  //const data = await response.json();
  //navigate('/app/projects', { state : data});

  // Create new result 
  const today = new Date();
  const formattedDate = `${String(today.getDate()).padStart(2, '0')}${String(today.getMonth() + 1).padStart(2, '0')}${today.getFullYear()}`;
  console.log("Formatted date (DDMMYYYY):", formattedDate);
  
  console.log('Selected Classification:', selectedClassification);
  console.log('Selected Blueprint:', selectedBlueprint);
  console.log('Custom Classification Text:', customClassificationText);
  console.log('Selected project:', selectedProjectOption);
  console.log('Selected Existing Project:', selectedExistingProject);
  console.log('Projects:', projects);

  // If the user selected "New Project"
  if (selectedProjectOption === 'New Project') {
    if (!newProjectName.trim()) {
      alert('Please enter a new project name.');
      return;
    }

    // Create a new project object
    const newProject = {
      name: newProjectName,
      results: [formattedDate],
      open: true
    };

    // Add the new project to the projects list
    setProjects((prevProjects) => [...prevProjects, newProject]);

    // Set the new project as the selected one and open the Sidebar
    setSelectedResult({
      projectIndex: projects.length,
      result: formattedDate,
    });

    // Expand the sidebar and set overlay so other content is unclickable
    setExpanded(true);
    setOverlayActive(true);

    // If the user selected "Existing Project"
  } else if (selectedProjectOption === 'Existing Project') {
    // Check if chosen project can be found
    const existingProjectIndex = projects.findIndex(
      (project) => project.name === selectedExistingProject
    );

    if (existingProjectIndex === -1) {
      console.error('Selected project not found in the list.');
      alert('The selected project could not be found.');
      return;
    }

    // Create a new result and update the project
    let newResultName = generateUniqueResultName(projects[existingProjectIndex]?.results || [], formattedDate);
    setProjects((prevProjects) => {
      const updatedProjects = prevProjects.map((project, index) => {
        if (index === existingProjectIndex) {
          return { ...project, results: [...project.results, newResultName], open: true };
        }
        return project;
      });
      return updatedProjects;
    });

    // Open the Sidebar and set the created result as selected
    if (newResultName) {
      setSelectedResult({
        projectIndex: existingProjectIndex,
        result: newResultName,
      });

      // Expand the sidebar and set overlay so other content is unclickable
      setExpanded(true); 
      setOverlayActive(true);
    }
      
  }

    // Reset the form state
    resetFormState();

    alert("Analysis completed! The result has been added to the selected project.");
  };

  // Function to generate a unique result name if duplicates exist
  const generateUniqueResultName = (results, baseName) => {
    let name = baseName;
    let counter = 1;
    while (results.includes(name)) {
      name = `${baseName} (${counter++})`;
    }
    console.log('Generated unique result name:', name);
    return name;
  };

  const allStepsCompleted = stepCompleted > 4;

  // Combined validation and saving function
  const validateAndSaveStep = (step) => {
    switch (step) {
      case 1:
        if (tempFiles.length === 0 && tempText.trim() === '') {
          alert('Please upload one file or enter some text.');
          return false;
        }
        handleFileUpload(tempFiles);
        handleTextChange(tempText);
        break;

      case 2:
        if (!tempClassification) {
          alert('Please select a classification option.');
          return false;
        }
        if (tempClassification === 'Saved Blueprint' && !tempBlueprint) {
          alert('Please select a saved blueprint.');
          return false;
        }
        if (tempClassification === 'Created Blueprint' && tempCustomText.trim() === '') {
          alert('Please enter a blueprint for "Created Blueprint".');
          return false;
        }
        handleClassificationSelection(tempClassification);
        if (tempClassification === 'Saved Blueprint') {
          handleBlueprintSelection(tempBlueprint);
        } else if (tempClassification === 'Created Blueprint') {
          handleCustomTextChange(tempCustomText);
        } else {
          setBlueprint(null);
        }
        break;

      case 3:
        if (!tempAI) {
          alert('Please select an AI option.');
          return false;
        }
        handleAISelection(tempAI);
        break;

      case 4:
        if (!tempProjectOption) {
          alert('Please choose a project option.');
          return false;
        }
        if (tempProjectOption === 'New Project' && !tempNewProjectName.trim()) {
          alert('Please enter a new project name.');
          return false;
        }
        if (tempProjectOption === 'Existing Project' && !tempExistingProject) {
          alert('Please select an existing project to continue.');
          return false;
        }
        if (tempProjectOption === 'Existing Project' && tempExistingProject) {
          handleExistingProjectSelection(tempExistingProject);
        }
        handleProjectOptionSelection(tempProjectOption);
        setNewProjectName(tempNewProjectName);
        break;

      default:
        console.error('Invalid step');
        return false;
    }
    return true;
  };

  // Function to go to the next step with validation and save selections
  const nextStep = () => {
    if (!validateAndSaveStep(currentStep)) {
      return; 
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
    setBlueprint(blueprint);
    
  };

  // Function to custom blueprint text
  const handleCustomTextChange = (text) => {
    setCustomClassificationText(text);
    setBlueprint(text)
  };

  // Function to update selected project option (New or Existing)
  const handleProjectOptionSelection = (option) => {
    setSelectedProjectOption(option);
    if (option === 'New Project') {
      setNewProjectName(''); 
    }
    if (option !== 'Existing Project') {
      setSelectedExistingProject(null); 
    }
  };

  
  // Function to update selected existing project
  const handleExistingProjectSelection = (project) => {
    setSelectedExistingProject(project);
    setSelectedProjectOption('Existing Project'); 
  };

  // Function to handle clicking the "Edit" button for a specific step
  const handleEditClick = (step) => {
    // Prevent editing another step if currently in editing mode
    if (isEditing) {
      alert('Please save or cancel the current editing step before editing another step.');
      return;
    }
    setCurrentStep(step);
    setIsEditing(true);
  };

  // Function to handle the "Save" button click
  const handleSaveClick = () => {
    if (!validateAndSaveStep(currentStep)) {
      return; 
    }
    setIsEditing(false); 
    setCurrentStep(5); 
  };

  return (
    <div className="multi-step-form">
      <p className="classification-heading">
        CED-LLM offers a streamlined process for classifying text data using AI technology. The interface provides four key steps to guide you through the classification process.
      </p>
      {/* Step 1: File upload or copy-paste text */}
      <div className="step">
        <div className="step-header">
          <h2 className={`step-title ${currentStep === 1 ? 'active' : ''}`}>
            1. File Upload or Copy Paste Text
          </h2>
          {allStepsCompleted && currentStep !== 1 && (
            <EditButton onEditClick={handleEditClick} step={1} />
          )}
        </div>
        {currentStep === 1 && (
          <div className="step-content">
            <FileDownload 
              onFileUpload={handleTempFileUpload}
              onTextChange={handleTempTextChange}
              isEditing={isEditing} 
            />
            {isEditing ? (
              <SaveButton onSaveClick={handleSaveClick} />
            ) : (
              <NextButton onNextClick={nextStep} />
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
            <EditButton onEditClick={handleEditClick} step={2} />
          )}
        </div>
        {currentStep === 2 && (
          <div className="step-content">
            <ClassificationSelection
              selectedClassification={tempClassification}
              onSelectClassification={setTempClassification} 
              onSelectBlueprint={setTempBlueprint}
              isLocked={isEditing} 
              onCustomTextChange={setTempCustomText}
            />
            {isEditing ? (
              <SaveButton onSaveClick={handleSaveClick} />
            ) : (
              <NextButton onNextClick={nextStep} />
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
            <EditButton onEditClick={handleEditClick} step={3} />
          )}
        </div>
        {currentStep === 3 && (
          <div className="step-content">
            <AISelection selectedAI={tempAI} onSelectAI={setTempAI} isLocked={isEditing} />
            {isEditing ? (
              <SaveButton onSaveClick={handleSaveClick} />
            ) : (
              <NextButton onNextClick={nextStep} />
            )}
          </div>
        )}
        {stepCompleted >= 3 && (
          <div className="step-summary">
            <p>{selectedAI}</p>
          </div>
        )}
      </div>

      {/* Step 4: Project Selection */}
      <div className="step">
        <div className="step-header">
          <h2 className={`step-title ${currentStep === 4 ? 'active' : ''}`}>
            4. Choose a Project for Displaying Results
          </h2>
          {allStepsCompleted && currentStep !== 4 && (
            <EditButton onEditClick={handleEditClick} step={4} />
          )}
        </div>
        {currentStep === 4 && (
          <div className="step-content">
            <ProjectSelection
              existingProjects={projects?.map((project) => project.name) || []}
              selectedProjectOption={tempProjectOption}
              onSelectProjectOption={setTempProjectOption}
              onSelectExistingProject={setTempExistingProject}
              isLocked={isEditing}
              uploadedFileName={tempFiles.length > 0 ? tempFiles[0].name : ''}
              copiedText={tempText}
              newProjectName={tempNewProjectName}
              onNewProjectNameChange={setTempNewProjectName}
            />
            {isEditing ? (
              <SaveButton onSaveClick={handleSaveClick} />
            ) : (
              <NextButton onNextClick={nextStep} />
            )}
          </div>
        )}
        {stepCompleted >= 4 && (
          <div className="step-summary">
            <p>{selectedProjectOption}</p>
            {selectedProjectOption === 'Existing Project' && selectedExistingProject && (
              <p>{selectedExistingProject}</p>
            )}
            {selectedProjectOption === 'New Project' && newProjectName && (
              <p>The given name: {newProjectName}</p>
            )}
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