import React from "react";
import { Link } from "react-router-dom"; 
import { FaChevronRight } from "react-icons/fa";
import './StartPage.css';

// Define a functional component named StartPage
const StartPage = () => {
  return (
    <>
      {/* Logo text in the top-left corner */}
      <div className="logo-text">CED-LLM</div>
      
      <div className="start-container">
        <div className="text-container">
          <h1>Classify, Enhance, and Transform Your Text Data!</h1>
        </div>
        <Link to="/app/classification"> 
          <button className="get-started-btn">
            Get Started
            <span className="arrow-icon">
              <FaChevronRight />
            </span>
          </button>
        </Link>
      </div>
    </>
  );
};

export default StartPage;