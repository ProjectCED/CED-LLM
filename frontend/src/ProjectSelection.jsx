import React, { useState, useEffect } from 'react';
import './ProjectSelection.css';

// ProjectSelection component that handles the selection of a project type (existing, new, or no project)
const ProjectSelection = ({ existingProjects, selectedProjectOption, onSelectProjectOption, onSelectExistingProject }) => {
  // Local state to manage the selected option (existing, new, or no project)
  const [localSelectedOption, setLocalSelectedOption] = useState(selectedProjectOption || '');
  
  // Local state to manage the selected existing project
  const [selectedExistingProject, setSelectedExistingProject] = useState('');

  // Effect hook to update the local selected option when the prop 'selectedProjectOption' changes
  useEffect(() => {
    setLocalSelectedOption(selectedProjectOption);
  }, [selectedProjectOption]);

  // Handler for when an option (existing, new, or no project) is selected
  const handleOptionSelect = (option) => {
    setLocalSelectedOption(option); 
    onSelectProjectOption(option); 

    // If the selected option is not "Existing Project", reset the existing project selection
    if (option !== 'Existing Project') {
      setSelectedExistingProject('');
      onSelectExistingProject(''); 
    }
  };

  // Handler for when a specific existing project is selected from the dropdown
  const handleExistingProjectSelect = (project) => {
    setSelectedExistingProject(project); 
    onSelectExistingProject(project); 
  };

  return (
    <div className="project-selection">
      {/* Text instructing the user to select a project option */}
      <p>Select an existing project or create a new one to display results.</p>
      
      <div className="project-button-container">
        {/* Button to select "Existing Project", highlighted if it's the selected option */}
        <button
          className={`selection-button ${localSelectedOption === 'Existing Project' ? 'selected' : ''}`}
          onClick={() => handleOptionSelect('Existing Project')}
        >
          Existing Project
        </button>
        {/* Button to select "New Project", highlighted if it's the selected option */}
        <button
          className={`selection-button ${localSelectedOption === 'New Project' ? 'selected' : ''}`}
          onClick={() => handleOptionSelect('New Project')}
        >
          Create a New Project
        </button>
      </div>

      {/* Show the dropdown for selecting an existing project when the option is "Existing Project" */}
      {localSelectedOption === 'Existing Project' && (
        <div className="dropdown-container">
          <select
            id="existing-projects"
            value={selectedExistingProject} 
            onChange={(e) => handleExistingProjectSelect(e.target.value)} 
          >
            <option value="">-- Choose a Project --</option>
            {existingProjects.map((project, index) => (
              // Map through the existing projects and create an option for each
              <option key={index} value={project}>
                {project}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Show the input field to create a new project when the option is "New Project" */}
      {localSelectedOption === 'New Project' && (
        <div className="new-project-container">
          <p>Enter New Project Name:</p>
          <input
            id="new-project-name"
            type="text"
            placeholder="New project name"
          />
        </div>
      )}
    </div>
  );
};

export default ProjectSelection;