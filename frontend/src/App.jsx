// App.jsx
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';  
import StartPage from './StartPage';
import Classification from './Classification';
import Projects from './Projects';
import Blueprints from './Blueprints';
import Header from './Header';
import Sidebar from './Sidebar'; 

function App() {
  const [overlayActive, setOverlayActive] = useState(false);

  return (
    <div className={`app-container ${overlayActive ? 'overlay-active' : ''}`}>
      <Router>
        <Routes>
          {/* Starting view */}
          <Route path="/" element={<StartPage />} />

          {/* Views that have Header */}
          <Route path="/app/*" element={<MainLayout setOverlayActive={setOverlayActive} />} />
        </Routes>
      </Router>
    </div>
  );
}

function MainLayout({ setOverlayActive }) {
  return (
    <div className="main-layout">
      <Header />
      <div className="content-container">
        <Sidebar setOverlayActive={setOverlayActive} />
        <div className="main-content"> {/* Tämä tummentuu, kun overlay on aktiivinen */}
          <Routes>
            <Route path="classification" element={<Classification />} />
            <Route path="projects" element={<Projects />} />
            <Route path="blueprints" element={<Blueprints />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default App;

