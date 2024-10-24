import React from 'react';
import { NavLink } from 'react-router-dom';
import './Header.css';

const Header = () => {
    return (
        <nav>
          <ul>
            <li>
            <NavLink 
              to="/app/classification" 
              className={({ isActive }) => isActive ? 'active' : ''}
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