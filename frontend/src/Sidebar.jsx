import React, { useState } from 'react';
import './Sidebar.css';

function Sidebar() {
  const [expanded, setExpanded] = useState(false);
  const [projects, setProjects] = useState([
    { name: 'Project 1', open: false, results: ['Result 1', 'Result 2'] },
    { name: 'Project 2', open: false, results: ['Result 1'] },
    { name: 'Project 3', open: false, results: ['Result 1', 'Result 2', 'Result 3'] }
  ]);
  const [newProjectName, setNewProjectName] = useState('');

  const toggleSidebar = () => {
    setExpanded(!expanded);
  };

  // Funktio yksittäisen projektin avaamiseen/sulkemiseen
  const toggleProject = (index) => {
    setProjects(prevProjects =>
      prevProjects.map((project, i) =>
        i === index ? { ...project, open: !project.open } : project
      )
    );
  };

  // Funktio uuden projektin luomiseen
  const addProject = () => {
    if (newProjectName.trim()) {
      const newProject = {
        name: newProjectName,
        open: false,
        results: ['Result 1'] // Voidaan lisätä esim. yksi oletustulos
      };
      setProjects([...projects, newProject]);
      setNewProjectName(''); // Tyhjennetään tekstikenttä
    } else {
      alert("Project name cannot be empty");  // Jos nimi on tyhjä
    }
  };

  return (
    <div className={`sidebar ${expanded ? 'expanded' : 'collapsed'}`}>
      {/* Ikoni painiketta varten */}
      <button className="sidebar-toggle" onClick={toggleSidebar}>
      ☰  
      </button>
      
      {/* Näytetään vain, jos sidebar on laajennettu */}
      {expanded && (
        <div className="project-list">
             <h2 className="projects-title">Projects</h2>

          {projects.map((project, index) => (
            <div key={index}>
              <div className="project-header" onClick={() => toggleProject(index)}>
                {/* Nuoli-ikoni, joka vaihtuu projektin tilan mukaan */}
                {project.open ? '▴' : '▾'} {project.name}
              </div>
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
            {/* Tekstikenttä projektin nimen syöttämiseksi */}
            <input
                type="text"
                value={newProjectName}
                onChange={(e) => setNewProjectName(e.target.value)}
                placeholder="Enter project name"
                className="project-name-input"
            />
            {/* Painike uuden projektin luomiseksi */}
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