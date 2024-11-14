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
  const [hoveredResult, setHoveredResult] = useState({ projectIndex: null, resultIndex: null });
  const [selectedResult, setSelectedResult] = useState(null);

  const toggleSidebar = () => {
    setExpanded(!expanded);
    if (expanded) {
      closeResultDetails();
    }
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

  const deleteResult = (projectIndex, resultIndex) => {
    setProjects(prevProjects =>
      prevProjects.map((project, i) =>
        i === projectIndex
          ? { ...project, results: project.results.filter((_, j) => j !== resultIndex) }
          : project
      )
    );
  };

  const openResultDetails = (projectIndex, result) => {
    setSelectedResult({ projectIndex, result });
    setOverlayActive(true);
  };

  const closeResultDetails = () => {
    setSelectedResult(null);
    setOverlayActive(false);
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
                        className={`project-result ${selectedResult?.result === result ? 'selected' : ''}`}
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
              <h2>Analyze Result</h2>

              <h3>Header 1</h3>
              <p>
              Text text text text text text text text text text text text text text text text text.
              </p>

              <h3>Header 2</h3>
              <p>
              Text text text text text text text text text text text text text text text text text.
              </p>

              <h3>Header 3</h3>
              <p>
              Text text text text text text text text text text text text text text text text text.
              </p>

              <h3>Header 4</h3>
              <p>
              Text text text text text text text text text text text text text text text text text.
              </p>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Sidebar;


