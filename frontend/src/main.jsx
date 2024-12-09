import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'
/**
 * This is the main entry point for the React application.
 * It sets up the root React component and renders the application within the DOM.
 */

/**
 * Mounts the root React component into the DOM.
 * @function
 * @param {HTMLElement} rootElement - The root DOM element where the React app will be mounted.
 */
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
