import React, { useState } from 'react';
import FileDownload from './FileDownload'; // Step 1 component
import ClassificationSelection from './ClassificationSelection'; // Step 2 component
import AISelection from './AISelection'; // Step 3 component
import ProjectSelection from './ProjectSelection'; // Step 4 component
import './MultiStepForm.css';
import { uploadFile, analyzeUploadedFile, analyzeText, saveProject, saveResult } from './utils';

/**
 * EditButton component renders a button to enable editing a specific step.
 *
 * @param {Object} props - The props object.
 * @param {function} props.onEditClick - Callback to handle edit action for a step.
 * @param {number} props.step - The step number to edit.
 * @returns {JSX.Element} The EditButton component.
 */
const EditButton = ({ onEditClick, step }) => {
  return (
    <button className="edit-button" onClick={() => onEditClick(step)}>
      Edit
    </button>
  );
};

/**
 * SaveButton component renders a button to save changes made in a step.
 *
 * @param {Object} props - The props object.
 * @param {function} props.onSaveClick - Callback to handle save action.
 * @returns {JSX.Element} The SaveButton component.
 */
const SaveButton = ({ onSaveClick }) => {
  return (
    <button className="multiform-save-button" onClick={onSaveClick}>
      Save
    </button>
  );
};

/**
 * NextButton component renders a button to proceed to the next step.
 *
 * @param {Object} props - The props object.
 * @param {function} props.onNextClick - Callback to handle proceeding to the next step.
 * @returns {JSX.Element} The NextButton component.
 */
const NextButton = ({ onNextClick }) => {
  return (
    <button className="next-button" onClick={onNextClick}>
      Next
    </button>
  );
};

/**
 * MultiStepForm component guides users through a multi-step process for 
 * classifying text data with AI, uploading files, selecting blueprints, 
 * and associating results with a project.
 *
 * @component
 * @param {Object} props - The props object.
 * @param {Array} props.projects - List of existing projects.
 * @param {function} props.setProjects - Callback to update projects.
 * @param {function} props.setExpanded - Callback to expand the project sidebar.
 * @param {function} props.setSelectedResult - Callback to set the selected result.
 * @param {function} props.setOverlayActive - Callback to toggle the overlay state.
 * @returns {JSX.Element} The MultiStepForm component.
 */
const MultiStepForm = ({ projects, setProjects, setExpanded, setSelectedResult, setOverlayActive}) => {
  // State variables to track the current step and selections
  
  /**
   * @type {number}
   * @description The current step in the multi-step form.
   */
  const [currentStep, setCurrentStep] = useState(1); 

  /**
   * @type {boolean}
   * @description Tracks whether the form is in editing mode.
   */
  const [isEditing, setIsEditing] = useState(false);

  /**
   * @type {number}
   * @description Tracks the number of completed steps.
   */
  const [stepCompleted, setStepCompleted] = useState(0);

  // Persistent states for current step changes
   /**
   * @type {Array<File>}
   * @description List of selected files for upload.
   */
   const [selectedFiles, setSelectedFiles] = useState([]);

   /**
    * @type {string}
    * @description Stores text that the user has copied for classification.
    */
   const [copiedText, setCopiedText] = useState('');
 
   /**
    * @type {?Object}
    * @description Stores the selected classification for the current step.
    */
   const [selectedClassification, setSelectedClassification] = useState(null);
 
   /**
    * @type {?Object}
    * @description Stores the selected AI model for the current step.
    */
   const [selectedAI, setSelectedAI] = useState(null);
 
   /**
    * @type {?Object}
    * @description Stores the selected blueprint for the current step.
    */
   const [selectedBlueprint, setSelectedBlueprint] = useState(null);
 
   /**
    * @type {?string}
    * @description Stores the selected project option (either new or existing).
    */
   const [selectedProjectOption, setSelectedProjectOption] = useState(null);
 
   /**
    * @type {?Object}
    * @description Stores the selected existing project, if any.
    */
   const [selectedExistingProject, setSelectedExistingProject] = useState(null);
 
   /**
    * @type {string}
    * @description Stores custom classification text provided by the user.
    */
   const [customClassificationText, setCustomClassificationText] = useState('');
 
   /**
    * @type {string}
    * @description Stores the name of a new project if the user chooses to create one.
    */
   const [newProjectName, setNewProjectName] = useState('');
 

  // Temporary states for current step changes
  /**
   * @type {Array<File>}
   * @description Temporarily stores files during the current step.
   */
  const [tempFiles, setTempFiles] = useState([]);

  /**
   * @type {string}
   * @description Temporarily stores text input during the current step.
   */
  const [tempText, setTempText] = useState('');

  /**
   * @type {?Object}
   * @description Temporarily stores classification selection during the current step.
   */
  const [tempClassification, setTempClassification] = useState(null);

  /**
   * @type {?Object}
   * @description Temporarily stores blueprint selection during the current step.
   */
  const [tempBlueprint, setTempBlueprint] = useState(null);

  /**
   * @type {string}
   * @description Temporarily stores custom classification text input during the current step.
   */
  const [tempCustomText, setTempCustomText] = useState('');

  /**
   * @type {?Object}
   * @description Temporarily stores AI selection during the current step.
   */
  const [tempAI, setTempAI] = useState(null);

  /**
   * @type {?string}
   * @description Temporarily stores the selected project option during the current step.
   */
  const [tempProjectOption, setTempProjectOption] = useState(null);

  /**
   * @type {?Object}
   * @description Temporarily stores the selected existing project during the current step.
   */
  const [tempExistingProject, setTempExistingProject] = useState(null);

  /**
   * @type {string}
   * @description Temporarily stores the new project name during the current step.
   */
  const [tempNewProjectName, setTempNewProjectName] = useState('');

  /**
   * Resets the form state to its initial values.
   */
  const resetFormState = () => {

    // Reset persistent states
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

  /**
   * Handles file upload and updates the selected files state.
   *
   * @param {FileList} files - The uploaded files.
   */
  const handleFileUpload = (files) => {
    if (files.length > 0) {
      setSelectedFiles(files);
      setCopiedText('');
    } else {
      setSelectedFiles([]);
    }
  };

  /**
   * Handles changes in the copied text input field.
   *
   * @param {string} text - The entered text.
   */
  const handleTextChange = (text) => {
    if (text.trim() !== '') {
      setCopiedText(text);
      setSelectedFiles([]);
    } else {
      setCopiedText('');
    }
  };

   /**
   * Handles temporary file uploads during editing.
   * @param {File[]} files - Array of temporary files uploaded.
   */
   const handleTempFileUpload = (files) => {
    if (files.length > 0) {
      setTempFiles(files);
      setTempText('');
    } else {
      setTempFiles([]);
    }
  };

   /**
   * Handles changes in the temporary copied text input during editing.
   * @param {string} text - The temporary text input.
   */
  const handleTempTextChange = (text) => {
    if (text.trim() !== '') {
      setTempText(text);
      setTempFiles([]);
    } else {
      setTempText('');
    }
  };

  /**
   * Handles the "Analyze" button click, processing the final step 
   * and associating results with a project.
   */
  const handleAnalyze = async () => {
  let analysisResult = null;
  let filename = null;
  if (selectedAI === 'Mistral') {
    
  if (selectedFiles.length > 0) {
    filename = await uploadFile(selectedFiles[0]);
    analysisResult = await analyzeUploadedFile(filename, selectedBlueprint);
  } else {
    analysisResult = await analyzeText(copiedText, selectedBlueprint);
  }

  console.log("Analysis result:", analysisResult);
  console.log("Filename:", filename);

  // Create new result 
  const today = new Date();
  const formattedDate = `${String(today.getDate()).padStart(2, '0')}${String(today.getMonth() + 1).padStart(2, '0')}${today.getFullYear()}`;

  // If the user selected "New Project"
  if (selectedProjectOption === 'New Project') {
    if (!newProjectName.trim()) {
      alert('Please enter a new project name.');
      return;
    }

    // Create a new project object
    const newProject = {
      id: null,
      name: newProjectName,
      results: [],
      open: true
    };
    const projectId = await saveProject(newProjectName);
    newProject.id = projectId;

    // TODO: Avoid duplicate code (result is already present in the other if branch)
    const newResult = {
      id: null,
      name: formattedDate,
      filename: filename,
      blueprint: selectedBlueprint,
      result: analysisResult,
      projectId: projectId
    };
    const resultId = await saveResult(newResult);
    newResult.id = resultId;
    newProject.results.push(newResult);

    // Add the new project to the projects list
    setProjects((prevProjects) => [...prevProjects, newProject]);

    // Set the new project as the selected one and open the Sidebar
    setSelectedResult({
      projectIndex: projects.length,
      result: newResult
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

    const existingProjectId = projects[existingProjectIndex].id;
    // TODO: Avoid duplicate code (result is already present in the other if branch)
    const newResult = {
      id: null,
      name: formattedDate,
      filename: filename,
      blueprint: selectedBlueprint,
      result: analysisResult,
      projectId: existingProjectId
    };
    const resultId = await saveResult(newResult);
    newResult.id = resultId;

    setProjects((prevProjects) => {
      const updatedProjects = prevProjects.map((project, index) => {
        if (index === existingProjectIndex) {
          return { ...project, results: [...project.results, newResult], open: true };
        }
        return project;
      });
      return updatedProjects;
    });

    // Open the Sidebar and set the created result as selected
    if (newResultName) {
      setSelectedResult({
        projectIndex: existingProjectIndex,
        result: newResult,
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

  /**
   * Generates a unique result name if duplicates exist.
   * @param {string[]} results - List of existing result names.
   * @param {string} baseName - The base name for the result.
   * @returns {string} - A unique result name.
   */
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

  /**
   * Validates and saves the current step's data.
   * @param {number} step - The step to validate and save.
   * @returns {boolean} - True if the step data is valid, false otherwise.
   */
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
          //setBlueprint(null);
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

  /**
   * Navigates to the next step after validation and saving.
   */
  const nextStep = () => {
    if (!validateAndSaveStep(currentStep)) {
      return; 
    }
    const newStep = currentStep + 1;
    setCurrentStep(newStep);
    setStepCompleted(Math.max(stepCompleted, newStep));
  };

  /**
   * Updates the selected classification in Step 2.
   * @param {string} classification - The selected classification option.
   */
  const handleClassificationSelection = (classification) => {
    setSelectedClassification(classification);
  };

  /**
   * Updates the selected AI in Step 3.
   * @param {string} ai - The selected AI option.
   */
  const handleAISelection = (ai) => {
    setSelectedAI(ai);
  };

  /**
   * Updates the selected blueprint in Step 2.
   * @param {string} blueprint - The selected blueprint option.
   */
  const handleBlueprintSelection = (blueprint) => {
    setSelectedBlueprint(blueprint);
    //setBlueprint(blueprint);
    
  };

  /**
   * Updates the custom classification text for the blueprint.
   * @param {string} text - The custom text input for classification.
   */
  const handleCustomTextChange = (text) => {
    setCustomClassificationText(text);
    //setBlueprint(text)
  };

  /**
   * Updates the selected project option (New or Existing).
   * @param {string} option - The selected project option ('New Project' or 'Existing Project').
   */
  const handleProjectOptionSelection = (option) => {
    setSelectedProjectOption(option);
    if (option === 'New Project') {
      setNewProjectName(''); 
    }
    if (option !== 'Existing Project') {
      setSelectedExistingProject(null); 
    }
  };

  
  /**
   * Updates the selected existing project.
   * @param {Object} project - The selected existing project.
   */
  const handleExistingProjectSelection = (project) => {
    setSelectedExistingProject(project);
    setSelectedProjectOption('Existing Project'); 
  };

  /**
   * Handles clicking the "Edit" button for a specific step.
   * @param {number} step - The step number to edit.
   */
  const handleEditClick = (step) => {
    // Prevent editing another step if currently in editing mode
    if (isEditing) {
      alert('Please save or cancel the current editing step before editing another step.');
      return;
    }
    setCurrentStep(step);
    setIsEditing(true);
  };

  /**
   * Saves the current step's data and exits editing mode.
   */
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
            {selectedBlueprint && <p>{selectedBlueprint.name}</p>}
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