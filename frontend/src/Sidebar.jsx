// Sidebar.jsx
import React, { useState } from 'react';
import { TbLayoutSidebarLeftCollapse, TbLayoutSidebarLeftExpand } from "react-icons/tb";
import { FaTrash } from "react-icons/fa";  
import { AiOutlineClose } from "react-icons/ai";  
import './Sidebar.css';

function Sidebar({ setOverlayActive }) {
  const [expanded, setExpanded] = useState(false);
  const [projects, setProjects] = useState([
    { name: 'Customer Feedback', open: false, results: ['12062024', '27092024'] },
    { name: 'Dog show data', open: false, results: ['28042023'] },
    { name: 'Market Research', open: false, results: ['17052024', '18052024', '22052024'] }
  ]);
  const [newProjectName, setNewProjectName] = useState('');
  const [hoveredProject, setHoveredProject] = useState(null);
  const [selectedResult, setSelectedResult] = useState(null);

  const toggleSidebar = () => {
    setExpanded(!expanded);
  };

  const toggleProject = (index) => {
    setProjects(prevProjects =>
      prevProjects.map((project, i) =>
        i === index ? { ...project, open: !project.open } : project
      )
    );
  };

  const addProject = () => {
    if (newProjectName.trim()) {
      const newProject = {
        name: newProjectName,
        open: false,
        results: []
      };
      setProjects([...projects, newProject]);
      setNewProjectName('');
    } else {
      alert("Project name cannot be empty");
    }
  };

  const deleteProject = (index) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete the project and lose all its results?"
    );
    if (confirmDelete) {
      setProjects(prevProjects => prevProjects.filter((_, i) => i !== index));
    }
  };

  const openResultDetails = (projectIndex, result) => {
    setSelectedResult({ projectIndex, result });
    setOverlayActive(true); // Aktivoi overlayn
  };

  const closeResultDetails = () => {
    setSelectedResult(null);
    setOverlayActive(false); // Poistaa overlayn
  };

  return (
    <div className={`sidebar ${expanded ? 'expanded' : 'collapsed'}`}>
      <button className="sidebar-toggle" onClick={toggleSidebar}>
        {expanded ? <TbLayoutSidebarLeftCollapse size={24} /> : <TbLayoutSidebarLeftExpand size={24} />}
      </button>
      
      {expanded && (
        <>
          <h2 className="projects-title">Projects</h2>
          <div className="project-list">
            {projects.map((project, index) => (
              <div key={index}
                className="project-item"
                onMouseEnter={() => setHoveredProject(index)}
                onMouseLeave={() => setHoveredProject(null)}
              >
                <div className="project-header" onClick={() => toggleProject(index)}>
                  <span className="project-name">
                    {project.open ? '▴' : '▾'} {project.name}
                  </span>
                  {hoveredProject === index && (
                    <FaTrash
                      className="delete-icon"
                      onClick={(e) => {
                        e.stopPropagation();  // Estää klikkausta avaamasta projektia
                        deleteProject(index);
                      }}
                    />
                  )}
                </div>
                {project.open && (
                  <div className="project-results">
                    {project.results.map((result, i) => (
                      <div
                        key={i}
                        className={`project-result ${selectedResult?.result === result ? 'selected' : ''}`}
                        onClick={() => openResultDetails(index, result)}
                      >
                        {result}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
          <div className="input-container">
            <p className="add-project-title">Add new project</p>
            <input
              type="text"
              value={newProjectName}
              onChange={(e) => setNewProjectName(e.target.value)}
              placeholder="Enter project name"
              className="project-name-input"
            />
            <button onClick={addProject} className="create-project-button">Save</button>
          </div>

          {/* Overlay ja result-details ikkuna */}
          {selectedResult && <div className="overlay" onClick={closeResultDetails}></div>}
          {selectedResult && (
            <div className={`result-details ${selectedResult ? 'show' : ''}`}>
              <AiOutlineClose className="close-icon" onClick={closeResultDetails} />
              <h2>Analyze result</h2>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Sidebar;

