import React from "react";
import { Link } from "react-router-dom"; 
import './StartPage.css';

// Define a functional component named StartPage
const StartPage = () => {
  return (
    <div className="start-container">
      <div className="text-container">
        <h1>Classify, Enhance, and Transform Your Text Data!</h1>
      </div>
      <Link to="/app/classification"> 
        <button className="get-started-btn">Get started</button>
      </Link>
    </div>
  );
};

export default StartPage;