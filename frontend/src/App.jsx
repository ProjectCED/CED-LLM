import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './App.css';  
import StartPage from './StartPage';
import Classification from './Classification';
import Projects from './Projects';
import Blueprints from './Blueprints';
import Header from './Header';

function App() {
  return (
    <Router>
      <Routes>
        {/* Starting view */}
        <Route path="/" element={<StartPage />} />

        {/* Views that have Header */}
        <Route path="/app/*" element={<MainLayout />} />
      </Routes>
    </Router>
  );
}

// MainLayout is responsible for ensuring that the Header is visible on all subpages.
function MainLayout() {
  return (
    <>
      <Header /> 
      <Routes>
        <Route path="classification" element={<Classification />} />
        <Route path="projects" element={<Projects />} />
        <Route path="blueprints" element={<Blueprints />} />
      </Routes>

    </>
  );
}

export default App;
