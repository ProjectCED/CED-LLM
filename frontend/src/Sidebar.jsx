import React, { useState } from 'react';
import { TbLayoutSidebarLeftCollapse, TbLayoutSidebarLeftExpand } from "react-icons/tb";
import { FaTrash } from "react-icons/fa";
import { AiOutlineClose } from "react-icons/ai";
import jsPDF from "jspdf"; 
import './Sidebar.css';
import { saveProject, deleteProject, deleteResult } from './utils';

function Sidebar({ 
  setOverlayActive, 
  projects, 
  setProjects, 
  expanded, 
  setExpanded, 
  selectedResult, 
  setSelectedResult
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
  const removeProject = async (index) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete the project and lose all its results?"
    );
    if (confirmDelete) {
      await deleteProject(projects[index].id);
      setProjects(prevProjects => prevProjects.filter((_, i) => i !== index));
    }
  };

  // Deletes a specific result from a project
  const removeResult = async (projectIndex, resultIndex) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this result?"
    );
    if (confirmDelete) {
      const resultId = projects[projectIndex].results[resultIndex].id;
      await deleteResult(resultId);
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

    // Text content
    const doc = new jsPDF();
    const projectName = projects[selectedResult?.projectIndex]?.name;
    const resultName = selectedResult?.result?.name;
    const resultText = selectedResult?.result?.result;
    const filename = selectedResult?.result?.filename;
    const blueprintName = selectedResult?.result?.blueprint?.name;

    // PDF styling (margins, width, height)
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 20;
    
    const maxWidth = pageWidth - 2 * margin;
    const lineHeight = 10;
    
    // Tracks the current line's height, start with a bit of an offset
    let y = lineHeight * 2;

    // Add content to the PDF
    doc.setFont("helvetica", "bold");
    doc.setFontSize(20);
    doc.text("Analysis Result", margin, y);
    y += lineHeight * 2;

    doc.setFontSize(12);

    doc.text(`Project: ${projectName}`, margin, y);
    y += lineHeight;

    doc.text(`Result: ${resultName}`, margin, y);
    y += lineHeight;

    // Add filename if it exists
    if (filename) {
      doc.text(`Filename: ${filename}`, margin, y);
      y += lineHeight;
    }

    doc.text(`Blueprint: ${blueprintName || "Automatic Blueprint"}`, margin, y);
    y += lineHeight * 2;

    doc.setFont("helvetica", "normal");

    // Split the resultText into lines that fit the page
    const lines = doc.splitTextToSize(resultText, maxWidth);

    // Add lines to the PDF one at a time
    lines.forEach((line) => {
      // Signifies going over the page, so add a page and reset y (tracks height on current page)
      if (y + lineHeight > pageHeight - margin) {
        doc.addPage();
        y = margin;
      }
      doc.text(line, margin, y);
      y += lineHeight;
    });

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
                        removeProject(projectIndex);
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
                          selectedResult?.projectIndex === projectIndex && selectedResult?.result?.id === result?.id ? 'selected' : ''
                        }`}
                        onMouseEnter={() => setHoveredResult({ projectIndex, resultIndex })}
                        onMouseLeave={() => setHoveredResult({ projectIndex: null, resultIndex: null })}
                        onClick={() => openResultDetails(projectIndex, result)}
                      >
                        {result?.name}
                        {hoveredResult.projectIndex === projectIndex && hoveredResult.resultIndex === resultIndex && (
                          <FaTrash
                            className="delete-icon"
                            onClick={(e) => {
                              e.stopPropagation();
                              removeResult(projectIndex, resultIndex);
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
              <h2>Details for result: {selectedResult.result.name}</h2>

              <div className="result-details-content">

              <div className="result-data">
                <p>Project: {projects[selectedResult?.projectIndex]?.name}</p>
                <p>Blueprint: {selectedResult?.result?.blueprint?.name || 'Automatic Blueprint'}</p>
              </div>
                
                <p>
                {selectedResult.result.result}
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