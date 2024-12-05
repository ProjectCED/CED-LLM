import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';  
import StartPage from './StartPage';
import Projects from './Projects';
import Blueprints from './Blueprints';
import Header from './Header';
import Sidebar from './Sidebar'; 
import MultiStepForm from './MultiStepForm';
import { getProjects } from './utils';

function App() {
  const [overlayActive, setOverlayActive] = useState(false);
  // State for Sidebar control and selected result
  const [expanded, setExpanded] = useState(false);
  const [selectedResult, setSelectedResult] = useState(null);
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    getProjects().then((projects) => {
      setProjects(projects);
    });
  }, []);
  
  return (
    <div className={`app-container ${overlayActive ? 'overlay-active' : ''}`}>
      <Router>
        <Routes>
          {/* Starting view */}
          <Route path="/" element={<StartPage />} />

          {/* Views that have Header */}
          <Route path="/app/*" element={
            <MainLayout 
            setOverlayActive={setOverlayActive} 
            projects={projects} 
            setProjects={setProjects} 
            expanded={expanded}
            setExpanded={setExpanded}
            selectedResult={selectedResult}
            setSelectedResult={setSelectedResult}
          />
          } 
        />
        </Routes>
      </Router>
    </div>
  );
}

function MainLayout({ 
  setOverlayActive, 
  projects, 
  setProjects, 
  expanded, 
  setExpanded, 
  selectedResult, 
  setSelectedResult
}) {
  return (
    <div className="main-layout">
      <Header />
      <div className="content-container">
        <Sidebar
          setOverlayActive={setOverlayActive} 
          projects={projects} 
          setProjects={setProjects} 
          expanded={expanded} 
          setExpanded={setExpanded} 
          selectedResult={selectedResult} 
          setSelectedResult={setSelectedResult} 
         />
        <div className="main-content">
          <Routes>
            <Route path="classification" 
              element={
                <MultiStepForm 
                  projects={projects} 
                  setProjects={setProjects} 
                  setExpanded={setExpanded} 
                  setSelectedResult={setSelectedResult}
                  setOverlayActive={setOverlayActive} 
                />
                } 
                />
            <Route path="projects" element={<Projects />} />
            <Route path="blueprints" element={<Blueprints />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default App;