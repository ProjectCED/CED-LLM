import React from 'react';
import { NavLink } from 'react-router-dom';
import { Navbar, Nav } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Header.css';

/**
 * Header component for the application.
 * This component displays the navigation bar with links to various sections.
 */

/**
 * Header component providing navigation for the app.
 * 
 * - Displays the application brand and navigation links.
 * - Uses React-Bootstrap for responsive design.
 * - Active link is highlighted for better UX.
 *
 * @component
 * @returns {JSX.Element} The rendered Header component.
 */
const Header = () => {
  return (
    <Navbar expand="lg" className="custom-navbar">
      <Navbar.Brand href="/" className="navbar-brand">CED-LLM</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" className="navbar-toggler" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link as={NavLink} to="/app/classification" className="nav-link" activeClassName="active">
            Classification
          </Nav.Link>
          <Nav.Link as={NavLink} to="/app/blueprints" className="nav-link" activeClassName="active">
            Blueprints
          </Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}

export default Header;
