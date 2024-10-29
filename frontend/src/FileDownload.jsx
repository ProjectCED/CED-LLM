import React, { useState } from 'react';
import './FileDownload.css';

const FileDownload = ({ onFileUpload, onTextChange }) => {
  console.log('FileDownload component loaded'); 

  const [selectedFile, setSelectedFile] = useState(null);
  const [copiedText, setCopiedText] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);
  const [isLocked, setIsLocked] = useState(false);

  // Handle changes in the file input
  const handleFileChange = (event) => {
    const file = event.target.files[0]; 
    if (file) {
      setSelectedFile(file);            
      setCopiedText('');                
      setIsLocked(true);               
      console.log("File selected:", file);
      onFileUpload([file]);
    }
  };

  // Handle changes in the text area
  const handleTextChange = (event) => {
    const text = event.target.value;
    setCopiedText(text);
    setSelectedFile(null);

    // Lock fields if text is not empty
    if (text.trim() !== '') {
      setIsLocked(true);
    }
    console.log("Text entered:", text);
    onTextChange(text);
  };

  // Handle files dropped onto the drop zone
  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragOver(false);
    const file = event.dataTransfer.files[0];
    if (file) {
      setSelectedFile(file);
      setCopiedText('');
      setIsLocked(true);
      console.log("File dropped:", file);
      onFileUpload([file]);
    }
  };

  // Handle drag-over state (called repeatedly when file is dragged over)
  const handleDragOver = (event) => {
    event.preventDefault();
    setIsDragOver(true);
  };

  // Handle the end of drag-over state (called when the file is no longer dragged over)
  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  // Reset the selected file and text inputs
  const resetSelections = () => {
    setSelectedFile(null);
    setCopiedText('');
    onFileUpload([]);
    onTextChange('');
    setIsLocked(false);
  };

  return (
    <div className="container">
      <h2>Download file or copy paste text for analysis</h2>
      <div className="upload-wrapper">
        
        {/* File upload section */}
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
            disabled={isLocked}
          />
          <label htmlFor="file-input">
            BROWSE FILE
          </label>
          <p className="drag-drop-text">OR DRAG & DROP HERE</p>
          {/* Display selected file name */}
          {selectedFile && (
            <div className="file-info">
              <ul>
                <li>
                  <span className="file-name">{selectedFile.name}</span>
                </li>
              </ul>
            </div>
          )}
        </div>

        {/* Text upload section */}
        <div className="text-upload">
          <textarea
            placeholder="Copy paste text here"
            rows="4"
            value={copiedText}
            onChange={handleTextChange}
            disabled={isLocked && copiedText.trim() === ''}
          />
        </div>
      </div>

      {/* Button to reset both file and text inputs */}
      <button className="reset-button" onClick={resetSelections}>
        Reset Selections
      </button>
    </div>
  );
};

export default FileDownload;