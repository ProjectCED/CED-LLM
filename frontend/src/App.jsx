import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';  
import StartPage from './StartPage';
import Projects from './Projects';
import Blueprints from './Blueprints';
import Header from './Header';
import Sidebar from './Sidebar'; 
import MultiStepForm from './MultiStepForm';

/**
 * The main application component that sets up the router and manages global state.
 * Includes routing to different views and state management for projects, blueprints,
 * sidebar expansion, and overlay activation.
 *
 * @component
 */
function App() {

  /**
   * State to track whether the overlay is active.
   * @type {boolean}
   */
  const [overlayActive, setOverlayActive] = useState(false);

  /**
   * State to control the sidebar's expanded state.
   * @type {boolean}
   */
  const [expanded, setExpanded] = useState(false);

  /**
   * State to track the currently selected result in the sidebar.
   * @type {string|null}
   */
  const [selectedResult, setSelectedResult] = useState(null);
  
  /**
   * State to manage the list of projects.
   * Each project includes a name, an open state, and a list of results.
   * @type {Array<{name: string, open: boolean, results: string[]}>}
   */
  const [projects, setProjects] = useState([
    { name: 'Customer Feedback', open: false, results: ['12062024', '27092024'] },
    { name: 'Dog show data', open: false, results: ['28042023'] },
    { name: 'Market Research', open: false, results: ['17052024', '18052024', '22052024'] }
  ]);

   /**
   * State to track the currently selected blueprint.
   * @type {string}
   */
  const [blueprint, setBlueprint] = useState('');

  console.log('Projects in App:', projects);
  
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
            blueprint={blueprint}
            setBlueprint={setBlueprint}
          />
          } 
        />
        </Routes>
      </Router>
    </div>
  );
}

/**
 * The layout component for views under `/app/*`.
 * Includes the header, sidebar, and main content areas.
 *
 * @param {Object} props - The props passed to the component.
 * @param {Function} props.setOverlayActive - Callback to set the overlay active state.
 * @param {Array<{name: string, open: boolean, results: string[]}>} props.projects - The list of projects.
 * @param {Function} props.setProjects - Callback to update the list of projects.
 * @param {boolean} props.expanded - Indicates whether the sidebar is expanded.
 * @param {Function} props.setExpanded - Callback to set the expanded state of the sidebar.
 * @param {string|null} props.selectedResult - The currently selected result in the sidebar.
 * @param {Function} props.setSelectedResult - Callback to update the selected result.
 * @param {string} props.blueprint - The currently selected blueprint.
 * @param {Function} props.setBlueprint - Callback to update the selected blueprint.
 * @returns {JSX.Element} The layout with header, sidebar, and main content.
 */
function MainLayout({ 
  setOverlayActive, 
  projects, 
  setProjects, 
  expanded, 
  setExpanded, 
  selectedResult, 
  setSelectedResult,
  blueprint,  
  setBlueprint
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
          blueprint={blueprint}
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
                  setBlueprint={setBlueprint}
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