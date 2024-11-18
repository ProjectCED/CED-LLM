import React from 'react';
import { NavLink } from 'react-router-dom';
import { Navbar, Nav } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Header.css';

const Header = () => {
    return (
      <Navbar expand="lg" className="custom-navbar">
        <Navbar.Brand href="/" className="navbar-brand">CED-LLM</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
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