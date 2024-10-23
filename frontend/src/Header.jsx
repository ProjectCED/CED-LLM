import React from 'react';
import { NavLink } from 'react-router-dom';
import './Header.css';

const Header = () => {
    return (
        <nav>
          <ul>
            <li>
            <NavLink 
              to="/app/classification/file-download" // Path to the Classification page
              className={({ isActive, isPending }) => 
                // Check if the link is active or if the pathname starts with /app/classification
                isActive || window.location.pathname.startsWith('/app/classification') ? 'active' : ''
              }
            >
              Classification
            </NavLink>
            </li>
            <li>
              <NavLink 
                to="/app/projects" 
                className={({ isActive }) => isActive ? 'active' : ''}
              >
                Projects
              </NavLink>
            </li>
            <li>
              <NavLink 
                to="/app/blueprints" 
                className={({ isActive }) => isActive ? 'active' : ''}
              >
                Blueprints
              </NavLink>
            </li>
          </ul>
        </nav>
      );
  }

export default Header;