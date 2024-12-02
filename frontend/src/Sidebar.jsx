import React, { useState } from 'react';
import { TbLayoutSidebarLeftCollapse, TbLayoutSidebarLeftExpand } from "react-icons/tb";
import { FaTrash } from "react-icons/fa";
import { AiOutlineClose } from "react-icons/ai";
import jsPDF from "jspdf"; 
import './Sidebar.css';
import { saveProject } from './utils';

function Sidebar({ 
  setOverlayActive, 
  projects, 
  setProjects, 
  expanded, 
  setExpanded, 
  selectedResult, 
  setSelectedResult,
  blueprint  
  }) {

  // State to manage sidebar expansion
  const [newProjectName, setNewProjectName] = useState('');
  const [hoveredProject, setHoveredProject] = useState(null);
  const [hoveredResult, setHoveredResult] = useState({ projectIndex: null, resultIndex: null });

  // Toggle sidebar between expanded and collapsed states
  const toggleSidebar = () => {
    setExpanded(!expanded);
    if (!expanded) {
      setSelectedResult(null); // Collapse closes result details
    }
  };

  // Toggles a project's open/closed state
  const toggleProject = (index) => {
    setProjects(prevProjects =>
      prevProjects.map((project, i) =>
        i === index ? { ...project, open: !project.open } : project
      )
    );
  };

  // Adds a new project to the project list
  const addProject = () => {
    if (newProjectName.trim()) {
      const newProject = {
        id: null,
        name: newProjectName,
        open: false,
        results: []
      };
      const id = saveProject(newProjectName);
      newProject.id = id;
      
      setProjects([...projects, newProject]);
      setNewProjectName('');
    } else {
      alert("Project name cannot be empty");
    }
  };

  // Deletes a project from the list
  const deleteProject = (index) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete the project and lose all its results?"
    );
    if (confirmDelete) {
      setProjects(prevProjects => prevProjects.filter((_, i) => i !== index));
    }
  };

  // Deletes a specific result from a project
  const deleteResult = (projectIndex, resultIndex) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this result?"
    );
    if (confirmDelete) {
      setProjects(prevProjects =>
        prevProjects.map((project, i) =>
          i === projectIndex
            ? { ...project, results: project.results.filter((_, j) => j !== resultIndex) }
            : project
        )
      );
    }
  };

  // Opens detailed view for a specific result
  const openResultDetails = (projectIndex, result) => {
    setSelectedResult({ projectIndex, result });
    setOverlayActive(true);
  };

  // Closes the detailed view
  const closeResultDetails = () => {
    setSelectedResult(null);
    setOverlayActive(false);
  };

  const downloadPDF = () => {
    if (!selectedResult) return;

    const doc = new jsPDF();
    const projectName = projects[selectedResult.projectIndex]?.name;
    const resultName = selectedResult.result;

    // Add content to the PDF
    doc.setFont("helvetica", "bold");
    doc.setFontSize(20);
    doc.text("Analyze Result", 20, 20);
    doc.setFontSize(12);
    doc.setFont("helvetica", "normal");
    doc.text(`Project: ${projectName}`, 20, 40);
    doc.text(`Result: ${resultName}`, 20, 50);
    doc.text("Details for the result:", 20, 70);
    doc.text(`Blueprint: ${blueprint || "Automatic blueprint"}`, 20, 60);

    // Add example content
    const exampleText = `
      Result details here. This could include any relevant data about the result.`;
    doc.text(exampleText, 20, 90, { maxWidth: 170 });

    // Save the PDF
    doc.save(`${resultName}.pdf`);
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
            {projects.map((project, projectIndex) => (
              <div
                key={projectIndex}
                className="project-item"
                onMouseEnter={() => setHoveredProject(projectIndex)}
                onMouseLeave={() => setHoveredProject(null)}
              >
                <div className="project-header" onClick={() => toggleProject(projectIndex)}>
                  <span className="project-name">
                    {project.open ? '▴' : '▾'} {project.name}
                  </span>
                  {hoveredProject === projectIndex && (
                    <FaTrash
                      className="delete-icon"
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteProject(projectIndex);
                      }}
                    />
                  )}
                </div>
                {project.open && (
                  <div className="project-results">
                    {project.results.map((result, resultIndex) => (
                      <div
                        key={resultIndex}
                        className={`project-result ${
                          selectedResult?.projectIndex === projectIndex && selectedResult?.result === result ? 'selected' : ''
                        }`}
                        onMouseEnter={() => setHoveredResult({ projectIndex, resultIndex })}
                        onMouseLeave={() => setHoveredResult({ projectIndex: null, resultIndex: null })}
                        onClick={() => openResultDetails(projectIndex, result)}
                      >
                        {result}
                        {hoveredResult.projectIndex === projectIndex && hoveredResult.resultIndex === resultIndex && (
                          <FaTrash
                            className="delete-icon"
                            onClick={(e) => {
                              e.stopPropagation();
                              deleteResult(projectIndex, resultIndex);
                            }}
                          />
                        )}
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

          {selectedResult && <div className="overlay" onClick={closeResultDetails}></div>}
          {selectedResult && (
            <div className={`result-details ${selectedResult ? 'show' : ''}`}>
              <AiOutlineClose className="close-icon" onClick={closeResultDetails} />
              <h2>Details for result: {selectedResult.result}</h2>

              <div className="result-details-content">

              <div className="result-data">
                <p>Project: {projects[selectedResult.projectIndex]?.name}</p>
                <p>Blueprint: {blueprint || 'Automatic blueprint'}</p>
              </div>
                
                <p>
                Text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text.
                </p>

                <p>
                Text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text.
                </p>

                <p>
                Text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text.
                </p>

                <p>
                Text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text.
                </p>

                <p>
                Text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text.
                </p>

              </div>

              {/* Download button */}
              <button className="download-pdf-button" onClick={downloadPDF}>
                Download to PDF
              </button>

            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Sidebar;