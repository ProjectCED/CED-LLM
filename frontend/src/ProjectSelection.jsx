import React, { useState, useEffect } from 'react';
import './ProjectSelection.css';

// ProjectSelection component that handles the selection of a project type (existing, new, or no project)
const ProjectSelection = ({
  existingProjects,
  selectedProjectOption,
  onSelectProjectOption,
  onSelectExistingProject,
  uploadedFileName,
  copiedText,
  newProjectName,
  onNewProjectNameChange,
}) => {
  const [localSelectedOption, setLocalSelectedOption] = useState(selectedProjectOption || '');
  const [selectedExistingProject, setSelectedExistingProject] = useState('');

  // Sync the local selected option with the selectedProjectOption prop whenever it changes
  useEffect(() => {
    if (selectedProjectOption !== localSelectedOption) {
      setLocalSelectedOption(selectedProjectOption);
    }
  }, [selectedProjectOption]);

  // Effect hook to handle project name change when selecting a new project
  useEffect(() => {
    if (localSelectedOption === 'New Project') {
      if (uploadedFileName) {
        onNewProjectNameChange(uploadedFileName);
      } else if (copiedText) {
        onNewProjectNameChange(copiedText.split(' ').slice(0, 3).join(' '));
      }
    }
  }, [localSelectedOption, uploadedFileName, copiedText, onNewProjectNameChange]);

  // Handler for when an option (existing, new, or none) is selected
  const handleOptionSelect = (option) => {
    setLocalSelectedOption(option);
    onSelectProjectOption(option);

    if (option === 'Existing Project') {
      setSelectedExistingProject(''); 
      onSelectExistingProject(''); 
    }
  };

  // Handler for when a specific existing project is selected from the dropdown
  const handleExistingProjectSelect = (project) => {
    setSelectedExistingProject(project);
    onSelectExistingProject(project);
    onSelectProjectOption('Existing Project');
  };

  return (
    <div className="project-selection">
      <p>Select an existing project or create a new one:</p>

      <div className="project-button-container">
        <button
          className={`selection-button ${localSelectedOption === 'Existing Project' ? 'selected' : ''}`}
          onClick={() => handleOptionSelect('Existing Project')}
        >
          Existing Project
        </button>
        <button
          className={`selection-button ${localSelectedOption === 'New Project' ? 'selected' : ''}`}
          onClick={() => handleOptionSelect('New Project')}
        >
          Create a New Project
        </button>
      </div>

      {localSelectedOption === 'Existing Project' && (
        <div className="dropdown-container">
          <select
            value={selectedExistingProject}
            onChange={(e) => handleExistingProjectSelect(e.target.value)}
          >
            <option value="">-- Choose a Project --</option>
            {existingProjects.map((project, index) => (
              <option key={index} value={project}>
                {project}
              </option>
            ))}
          </select>
        </div>
      )}

      {localSelectedOption === 'New Project' && (
        <div className="new-project-container">
          <p>Enter a new project name or use the default name:</p>
          <input
            type="text"
            placeholder="New project name"
            value={newProjectName}
            onChange={(e) => onNewProjectNameChange(e.target.value)}
          />
        </div>
      )}
    </div>
  );
};

export default ProjectSelection;
