import React, { useState, useEffect } from 'react';
import './ProjectSelection.css';

/**
 * ProjectSelection allows users to select an existing project or create a new one. 
 * It provides a UI for choosing between existing projects from a list or entering a new project name.
 *
 * @component
 * @param {Object} props - The props passed to the component.
 * @param {string[]} props.existingProjects - Array of existing project names available for selection.
 * @param {string} [props.selectedProjectOption] - The currently selected option, either 'Existing Project' or 'New Project'.
 * @param {Function} props.onSelectProjectOption - Callback function triggered when the project option changes.
 *        Receives the selected option as an argument.
 * @param {Function} props.onSelectExistingProject - Callback function triggered when an existing project is selected.
 *        Receives the name of the selected existing project as an argument.
 * @param {string} [props.uploadedFileName] - Name of an uploaded file, used to suggest a default name for a new project.
 * @param {string} [props.copiedText] - Text copied by the user, used to generate a suggested name for a new project.
 * @param {string} [props.newProjectName] - The name of the new project currently entered by the user.
 * @param {Function} props.onNewProjectNameChange - Callback function triggered when the new project name changes.
 *        Receives the updated project name as an argument.
 * @returns {JSX.Element} A UI for project selection, including buttons, dropdowns, and input fields.
 */

const ProjectSelection = ({
  existingProjects = [],
  selectedProjectOption,
  onSelectProjectOption,
  onSelectExistingProject,
  uploadedFileName,
  copiedText,
  newProjectName,
  onNewProjectNameChange,
}) => {

  /**
   * @type {string}
   * @description Tracks the locally selected project option ('Existing Project' or 'New Project').
   */
  const [localSelectedOption, setLocalSelectedOption] = useState(selectedProjectOption || '');

  /**
   * @type {string}
   * @description Tracks the name of the selected existing project from the dropdown.
   */
  const [selectedExistingProject, setSelectedExistingProject] = useState('');

  /**
   * @type {string}
   * @description Tracks the name of the new project entered by the user.
   */
  const [localNewProjectName, setLocalNewProjectName] = useState(newProjectName || '');

  /**
   * Synchronize the local selected option with the `selectedProjectOption` prop whenever it changes.
   */
  useEffect(() => {
    if (selectedProjectOption !== localSelectedOption) {
      setLocalSelectedOption(selectedProjectOption);
    }
  }, [selectedProjectOption]);

  /**
   * Automatically set a suggested name for a new project based on the uploaded file name or copied text.
   */
  useEffect(() => {
    if (localSelectedOption === 'New Project') {
      if (uploadedFileName) {
        setLocalNewProjectName(uploadedFileName);
      } else if (copiedText) {
        setLocalNewProjectName(copiedText.split(' ').slice(0, 3).join(' '));
      }
    }
  }, [localSelectedOption, uploadedFileName, copiedText]);

  /**
   * Update the parent component whenever the new project name changes.
   */
  useEffect(() => {
    if (localNewProjectName !== newProjectName) {
      onNewProjectNameChange(localNewProjectName);
    }
  }, [localNewProjectName, newProjectName, onNewProjectNameChange]);

  /**
   * Handle selection of a project option ('Existing Project' or 'New Project').
   *
   * @param {string} option - The selected option.
   */
  const handleOptionSelect = (option) => {
    setLocalSelectedOption(option);
    onSelectProjectOption(option);

    if (option === 'Existing Project') {
      setSelectedExistingProject('');
      onSelectExistingProject('');
    }
  };

  /**
   * Handle selection of an existing project from the dropdown.
   *
   * @param {string} project - The name of the selected existing project.
   */
  const handleExistingProjectSelect = (project) => {
    setSelectedExistingProject(project);
    onSelectExistingProject(project);
    onSelectProjectOption('Existing Project');
  };

  /**
   * Handle changes to the new project name input field.
   *
   * @param {Object} event - The input change event.
   */
  const handleNewProjectNameChange = (event) => {
    const value = event.target.value;
    setLocalNewProjectName(value); 
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
            placeholder="Enter a New Project Name"
            value={localNewProjectName}
            onChange={handleNewProjectNameChange}
          />
        </div>
      )}
    </div>
  );
};

export default ProjectSelection;
