import React, { useState } from 'react';
import { TbLayoutSidebarLeftCollapse, TbLayoutSidebarLeftExpand } from "react-icons/tb";
import './Sidebar.css';

function Sidebar() {
    // State hooks for managing the sidebar's expanded state, list of projects, and the new project name
  const [expanded, setExpanded] = useState(false);
  const [projects, setProjects] = useState([
    { name: 'Project 1', open: false, results: ['Result 1', 'Result 2'] },
    { name: 'Project 2', open: false, results: ['Result 1'] },
    { name: 'Project 3', open: false, results: ['Result 1', 'Result 2', 'Result 3'] }
  ]);
  const [newProjectName, setNewProjectName] = useState('');

  // Toggles the expanded/collapsed state of the sidebar
  const toggleSidebar = () => {
    setExpanded(!expanded);
  };

  // Toggles the state (open/closed) of a specific project based on its index
  const toggleProject = (index) => {
    setProjects(prevProjects =>
      prevProjects.map((project, i) =>
        i === index ? { ...project, open: !project.open } : project
      )
    );
  };

  // Adds a new project to the list if the project name is valid (not empty)
  const addProject = () => {
    if (newProjectName.trim()) {
      const newProject = {
        name: newProjectName,
        open: false,
        results: [] 
      };
      setProjects([...projects, newProject]); // Adds the new project to the list
      setNewProjectName(''); // Clears the input field after project creation
    } else {
      alert("Project name cannot be empty");  // Alerts if the project name is empty
    }
  };

  return (
    <div className={`sidebar ${expanded ? 'expanded' : 'collapsed'}`}>
      {/* Sidebar toggle button with conditional icons */}
      <button className="sidebar-toggle" onClick={toggleSidebar}>
        {expanded ? <TbLayoutSidebarLeftCollapse size={24} /> : <TbLayoutSidebarLeftExpand size={24} />}
      </button>
      
      {/* Only show the content if the sidebar is expanded */}
      {expanded && (
        <div className="project-list">
             <h2 className="projects-title">Projects</h2>
          {/* Map through the projects and display them */}  
          {projects.map((project, index) => (
            <div key={index}>
              <div className="project-header" onClick={() => toggleProject(index)}>
                {/* Arrow icon that toggles between open/closed states of each project */}
                {project.open ? '▴' : '▾'} {project.name}
              </div>
              {/* Display the results if the project is open */}
              {project.open && (
                <div className="project-results">
                  {project.results.map((result, i) => (
                    <div key={i} className="project-result">
                      {result}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}

        <div className="input-container">
            {/* Input field for entering a new project name */}
            <input
                type="text"
                value={newProjectName}
                onChange={(e) => setNewProjectName(e.target.value)}
                placeholder="Enter project name"
                className="project-name-input"
            />
            {/* Button to save the new project */}
            <button onClick={addProject} className="create-project-button">
                Save
            </button>
        </div>
    </div>
    )}
    </div>
  );
}

export default Sidebar;