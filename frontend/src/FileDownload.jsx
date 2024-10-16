import React, { useState } from 'react';
import './FileDownload.css';  
import { useNavigate } from 'react-router-dom';

const FileDownload = () => {
  
  console.log('FileDownload component loaded');
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [copiedText, setCopiedText] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);

  const navigate = useNavigate()
  
  // Handle file selection from input field
  const handleFileChange = (event) => {
    const files = Array.from(event.target.files);
    setSelectedFiles((prevFiles) => [...prevFiles, ...files]);
  };

  // Handle changes to the text input area
  const handleTextChange = (event) => {
    setCopiedText(event.target.value);
  };

  // Handle navigation or validation
  const handleContinue = () => {
    console.log("Navigating to classification-selection");
    // Check if there's at least one file or text input
    if (selectedFiles.length > 0 || copiedText.trim().length > 0) { // or any other condition
      navigate('/app/classification/classification-selection');
    } else {
      alert('Please select at least one file!');
    }
  };

   // Remove a specific file from the selected files list
  const removeFile = (fileToRemove) => {
    setSelectedFiles((prevFiles) =>
      prevFiles.filter((file) => file !== fileToRemove)
    );
  };

  // Handle file drop (drag and drop functionality
  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragOver(false); 
    const files = Array.from(event.dataTransfer.files);
    setSelectedFiles((prevFiles) => [...prevFiles, ...files]);
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
      <h2>Download file(s) or copy paste text for analysis</h2>
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
            multiple 
          />
          <label htmlFor="file-input">
            BROWSE FILES
          </label>
          <p className="drag-drop-text">OR DRAG & DROP HERE</p> 
          {selectedFiles.length > 0 && (
            <div className="file-info">
              <ul>
                {selectedFiles.map((file, index) => (
                  <li key={index}>
                    <span className="file-name">{file.name}</span> 
                    <span
                      className="remove-file"
                      onClick={() => removeFile(file)}
                      title="Remove file"
                    >
                      &#10005; 
                    </span>
                  </li>
                ))}
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
          />
        </div>
      </div>

      <button onClick={handleContinue} className="continue-button">
        Continue
      </button>
    </div>
  );
};

export default FileDownload;