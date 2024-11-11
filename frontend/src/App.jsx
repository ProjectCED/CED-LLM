import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './App.css';  
import StartPage from './StartPage';
import Classification from './Classification';
import Projects from './Projects';
import Blueprints from './Blueprints';
import Header from './Header';
import Sidebar from './Sidebar'; 

function App() {
  return (
    <div className="app-container">
      <Router>
        <Routes>
          {/* Starting view */}
          <Route path="/" element={<StartPage />} />

          {/* Views that have Header */}
          <Route path="/app/*" element={<MainLayout />} />
        </Routes>
      </Router>
    </div>
  );
}

// MainLayout is responsible for ensuring that the Header is visible on all subpages.
function MainLayout() {
  return (
    <div className="main-layout">
      <Header />  {/* Header yläosassa */}
      <div className="content-container">
        <Sidebar /> {/* Sivupalkki vasemmalla */}
        <div className="main-content"> {/* Pääsisältö oikealla */}
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
