import React from "react";
import { Link } from "react-router-dom"; 
import { FaChevronRight } from "react-icons/fa";
import './StartPage.css';

/**
 * StartPage is a landing page component that introduces the application 
 * and provides a "Get Started" button for navigation to the main functionality.
 *
 * @component
 * @returns {JSX.Element} The StartPage component displaying a welcome message and navigation button.
 */
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