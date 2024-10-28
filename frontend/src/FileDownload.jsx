import React, { useState } from 'react';
import './FileDownload.css';  

const FileDownload = ({ onFileUpload, onTextChange }) => {
  
  console.log('FileDownload component loaded');
  const [selectedFile, setSelectedFile] = useState(null);
  const [copiedText, setCopiedText] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);
  
  // Handle file selection from input field
  const handleFileChange = (event) => {
    const file = event.target.files[0]; // Allow only one file
    setSelectedFile(file);
    setCopiedText(''); // Clear the copied text if a file is selected
    console.log("File selected:", file);
    onFileUpload([file]); // Send the file to the MultiStepForm component
  };

  // Handle changes to the text input area
  const handleTextChange = (event) => {
    const text = event.target.value; // Get the value from the event
    setCopiedText(text);
    setSelectedFile(null); // Clear the file if text is entered
    console.log("Text entered:", text);
    onTextChange(text);  // Send the entered text to the MultiStepForm component
  };

   // Remove a specific file from the selected files list
  const removeFile = () => {
    setSelectedFile(null);
  };

  // Handle file drop (drag and drop functionality
  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragOver(false); 
    const file = event.dataTransfer.files[0]; // Allow only one file
    setSelectedFile(file);
    setCopiedText(''); // Clear the copied text if a file is dropped
    console.log("File dropped:", file);
    onFileUpload(file);  // Update the file in MultiStepForm
  };

  // Handle drag-over event (when a file is being dragged over the drop zone)
  const handleDragOver = (event) => {
    event.preventDefault();
    setIsDragOver(true); 
  };

  // Handle drag-leave event (when a file is dragged out of the drop zone)
  const handleDragLeave = () => {
    setIsDragOver(false); 
  };

  return (
    <div className="container">
      <h2>Download file or copy paste text for analysis</h2>
      <div className="upload-wrapper">
        <div 
          className={`file-upload ${isDragOver ? 'drag-over' : ''}`} 
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onDragLeave={handleDragLeave}
        >
          <input
            type="file"
            onChange={handleFileChange}
            style={{ display: 'none' }}
            id="file-input"
            disabled={copiedText.length > 0} // Disable file input if there's text 
          />
          <label htmlFor="file-input">
            BROWSE FILES
          </label>
          <p className="drag-drop-text">OR DRAG & DROP HERE</p> 
          {selectedFile && (
            <div className="file-info">
              <ul>
              <li>
                  <span className="file-name">{selectedFile.name}</span>
                  <span
                    className="remove-file"
                    onClick={removeFile}
                    title="Remove file"
                  >
                    &#10005;
                  </span>
                </li>
              </ul>
            </div>
          )}
        </div>

        <div className="text-upload">
          <textarea
            placeholder="Copy paste text here"
            rows="4"
            value={copiedText}
            onChange={handleTextChange}
            disabled={selectedFile !== null} // Disable textarea if a file is selected
          />
        </div>
      </div>

    </div>
  );
};

export default FileDownload;