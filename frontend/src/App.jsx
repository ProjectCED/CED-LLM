import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';  
import StartPage from './StartPage';
import Projects from './Projects';
import Blueprints from './Blueprints';
import Header from './Header';
import Sidebar from './Sidebar'; 
import MultiStepForm from './MultiStepForm';

function App() {
  const [overlayActive, setOverlayActive] = useState(false);

  // State for project list, with each project containing results
  const [projects, setProjects] = useState([
    { name: 'Customer Feedback', open: false, results: ['12062024', '27092024'] },
    { name: 'Dog show data', open: false, results: ['28042023'] },
    { name: 'Market Research', open: false, results: ['17052024', '18052024', '22052024'] }
  ]);

  console.log('Projects in App:', projects);
  
  return (
    <div className={`app-container ${overlayActive ? 'overlay-active' : ''}`}>
      <Router>
        <Routes>
          {/* Starting view */}
          <Route path="/" element={<StartPage />} />

          {/* Views that have Header */}
          <Route path="/app/*" element={<MainLayout setOverlayActive={setOverlayActive} projects={projects} setProjects={setProjects} />} />
        </Routes>
      </Router>
    </div>
  );
}

function MainLayout({ setOverlayActive, projects, setProjects }) {
  return (
    <div className="main-layout">
      <Header />
      <div className="content-container">
        <Sidebar setOverlayActive={setOverlayActive} projects={projects} setProjects={setProjects} />
        <div className="main-content"> {/* Tämä tummentuu, kun overlay on aktiivinen */}
          <Routes>
            <Route path="classification" element={<MultiStepForm projects={projects} setProjects={setProjects} />} />
            <Route path="projects" element={<Projects />} />
            <Route path="blueprints" element={<Blueprints />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default App;


