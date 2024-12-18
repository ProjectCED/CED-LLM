import React, { useState } from 'react';
import { TbLayoutSidebarLeftCollapse, TbLayoutSidebarLeftExpand } from "react-icons/tb";
import { FaTrash } from "react-icons/fa";
import { AiOutlineClose } from "react-icons/ai";
import { jsPDF } from "jspdf";
import { marked } from "marked";
import './Sidebar.css';
import { saveProject, deleteProject, deleteResult } from './utils';
import ReactMarkdown from 'react-markdown';

/**
 * Sidebar component provides a collapsible interface for managing projects and their associated results.
 * It supports deleting and selecting projects or results, creating new projects and downloading result details as a PDF.
 *
 * @component
 * @param {Object} props - The props passed to the component.
 * @param {Function} props.setOverlayActive - Function to set the state of the overlay (true/false).
 * @param {Array<Object>} props.projects - List of projects, where each project contains a name, open state, and results array.
 * @param {Function} props.setProjects - Function to update the list of projects.
 * @param {boolean} props.expanded - Boolean indicating whether the sidebar is expanded or collapsed.
 * @param {Function} props.setExpanded - Function to toggle the expanded state of the sidebar.
 * @param {Object|null} props.selectedResult - Currently selected result object, or null if none is selected.
 * @param {Function} props.setSelectedResult - Function to set the currently selected result.
 * @param {string|null} props.blueprint - Blueprint name or description associated with the current result.
 * @returns {JSX.Element} A collapsible sidebar interface for managing projects and results.
 */

function Sidebar({ 
  setOverlayActive, 
  projects, 
  setProjects, 
  expanded, 
  setExpanded, 
  selectedResult, 
  setSelectedResult
  }) {

  /**
   * @type {string}
   * @description Stores the name of the new project being created.
   */
  const [newProjectName, setNewProjectName] = useState('');

   /**
   * @type {number|null}
   * @description Tracks the index of the project currently being hovered over. Null if no project is hovered.
   */
  const [hoveredProject, setHoveredProject] = useState(null);

  /**
   * @type {Object}
   * @property {number|null} projectIndex - Index of the hovered project, or null if no project is hovered.
   * @property {number|null} resultIndex - Index of the hovered result, or null if no result is hovered.
   * @description Tracks the project and result currently being hovered over.
   */
  const [hoveredResult, setHoveredResult] = useState({ projectIndex: null, resultIndex: null });

  /**
   * Toggles the sidebar between expanded and collapsed states.
   */
  const toggleSidebar = () => {
    setExpanded(!expanded);
    if (!expanded) {
      setSelectedResult(null); // Collapse closes result details
    }
  };

  /**
   * Toggles a project's open/closed state in the project list.
   *
   * @param {number} index - Index of the project to toggle.
   */
  const toggleProject = (index) => {
    setProjects(prevProjects =>
      prevProjects.map((project, i) =>
        i === index ? { ...project, open: !project.open } : project
      )
    );
  };

  /**
   * Adds a new project to the project list with the specified name.
   * Alerts the user if the project name is empty.
   */
  const addProject = async () => {
    if (newProjectName.trim()) {
      const newProject = {
        id: null,
        name: newProjectName,
        open: false,
        results: []
      };
      const id = await saveProject(newProjectName);
      newProject.id = id;
      
      setProjects([newProject, ...projects]);
      setNewProjectName('');
    } else {
      alert("Project name cannot be empty");
    }
  };

   /**
   * Deletes a project from the project list after user confirmation.
   *
   * @param {number} index - Index of the project to delete.
   */
  const removeProject = async (index) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete the project and lose all its results?"
    );

    if (!confirmDelete) return;

    const projectId = projects[index].id;
    const success = await deleteProject(projectId)

    if (!success) return;

    setProjects(prevProjects => prevProjects.filter((_, i) => i !== index));
  };

  /**
   * Deletes a specific result from a project after user confirmation.
   *
   * @param {number} projectIndex - Index of the project containing the result.
   * @param {number} resultIndex - Index of the result to delete.
   */
  const removeResult = async (projectIndex, resultIndex) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this result?"
    );
    
    if (!confirmDelete) return

    const resultId = projects[projectIndex].results[resultIndex].id;
    const success = await deleteResult(resultId);

    if (!success) return;

    setProjects(prevProjects =>
      prevProjects.map((project, i) =>
        i === projectIndex
          ? { ...project, results: project.results.filter((_, j) => j !== resultIndex) }
          : project
      )
    );
  };

  /**
   * Opens detailed view for a specific result and activates the overlay.
   *
   * @param {number} projectIndex - Index of the project containing the result.
   * @param {string} result - The result to display details for.
   */
  const openResultDetails = (projectIndex, result) => {
    setSelectedResult({ projectIndex, result });
    setOverlayActive(true);
  };

  /**
   * Closes the result details view and deactivates the overlay.
   */
  const closeResultDetails = () => {
    setSelectedResult(null);
    setOverlayActive(false);
  };

  /**
   * Downloads the currently selected result details as a PDF.
   * Uses jsPDF library to generate the PDF document.
   */
  const downloadPDF = () => {
    if (!selectedResult) return;

    // Text content
    const doc = new jsPDF();
    const projectName = projects[selectedResult?.projectIndex]?.name;
    const resultName = selectedResult?.result?.name;
    const resultText = selectedResult?.result?.result;
    const filename = selectedResult?.result?.filename;
    const blueprintName = selectedResult?.result?.blueprint?.name;

    // Convert markdown to HTML
    const htmlContent = marked(resultText);

    // PDF styling (margins, width, height)
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 20;
    
    const maxWidth = pageWidth - 2 * margin;
    const lineHeight = 10;
    
    // Tracks the current line's height, start with a bit of an offset
    let y = lineHeight * 2;

    // Construct a combined HTML with headers and info
    // You can add inline styles or use basic HTML tags for formatting
    const combinedHTML = `
      <h1>Analysis Result</h1>
      <p><strong>Project:</strong> ${projectName}</p>
      <p><strong>Result:</strong> ${resultName}</p>
      ${filename ? `<p><strong>Filename:</strong> ${filename}</p>` : ""}
      <p><strong>Blueprint:</strong> ${blueprintName || "Automatic Blueprint"}</p>
      <hr />
    ${htmlContent}
  `;

    doc.html(combinedHTML, {
      x: margin,
      y: margin,
      width: pageWidth - margin * 2,
      // Set windowWidth to something close to your actual PDF width to maintain proper scaling
      windowWidth: 800, // Experiment with this value
      callback: (doc) => {
        doc.save(`${resultName}.pdf`);
      }
    });
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
                <p>Filename: {selectedResult?.result?.filename}</p>
                <p>Blueprint: {selectedResult?.result?.blueprint?.name || 'Automatic Blueprint'}</p>
              </div> 
                <ReactMarkdown
                  components={{
                    p: ({node, ...props}) => <p style={{color: 'white', textAlign: 'left'}} {...props} />,
                    h1: ({node, ...props}) => <h1 style={{color: 'white', textAlign: 'left'}} {...props} />,
                    h2: ({node, ...props}) => <h2 style={{color: 'white', textAlign: 'left'}} {...props} />,
                    h3: ({node, ...props}) => <h3 style={{color: 'white', textAlign: 'left'}} {...props} />,
                    h4: ({node, ...props}) => <h4 style={{color: 'white', textAlign: 'left'}} {...props} />,
                    h5: ({node, ...props}) => <h5 style={{color: 'white', textAlign: 'left'}} {...props} />,
                    h6: ({node, ...props}) => <h6 style={{color: 'white', textAlign: 'left'}} {...props} />,
                    li: ({node, ...props}) => <li style={{color: 'white', textAlign: 'left'}} {...props} />,
                    strong: ({node, ...props}) => <strong style={{color: 'white', textAlign: 'left'}} {...props} />,
                    em: ({node, ...props}) => <em style={{color: 'white', textAlign: 'left'}} {...props} />,
                    blockquote: ({node, ...props}) => <blockquote style={{color: 'white', textAlign: 'left'}} {...props} />,
                    code: ({node, ...props}) => <code style={{color: 'white', textAlign: 'left'}} {...props} />,
                    pre: ({node, ...props}) => <pre style={{color: 'white', textAlign: 'left'}} {...props} />,
                    a: ({node, ...props}) => <a style={{color: 'white', textAlign: 'left'}} {...props} />,
                  }}
                >
                  {selectedResult.result.result}
                </ReactMarkdown>
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