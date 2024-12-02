import React, { useState } from 'react';
import './FileDownload.css';

/**
 * FileDownload component allows the user to upload a file via a file input 
 * or drag and drop, or paste text for analysis. It handles file and text 
 * selection, locking the input fields once a selection is made, and provides 
 * a reset button to clear the selections.
 *
 * @component
 * @param {Object} props - The properties passed to the component.
 * @param {Function} props.onFileUpload - Callback function triggered when a file is uploaded or selected.
 * @param {Function} props.onTextChange - Callback function triggered when the text input is changed.
 * @returns {JSX.Element} The rendered FileDownload component with file and text upload options.
 */
const FileDownload = ({ onFileUpload, onTextChange }) => {
  console.log('FileDownload component loaded'); 

  /**
   * State to store the selected file.
   * @type {File | null}
   */
  const [selectedFile, setSelectedFile] = useState(null);

  /**
   * State to store the copied text from the text area.
   * @type {string}
   */
  const [copiedText, setCopiedText] = useState('');

  /**
   * State to track if a file is being dragged over the drop zone.
   * @type {boolean}
   */
  const [isDragOver, setIsDragOver] = useState(false);

  /**
   * State to lock the file and text inputs after selection.
   * @type {boolean}
   */
  const [isLocked, setIsLocked] = useState(false);

  /**
   * Handles changes in the file input, updates the selected file and locks the inputs.
   * @param {React.ChangeEvent<HTMLInputElement>} event - The change event triggered by the file input.
   */
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

  /**
   * Handles changes in the text input, updates the copied text and locks the inputs if text is entered.
   * @param {React.ChangeEvent<HTMLTextAreaElement>} event - The change event triggered by the text area.
   */
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

  /**
   * Handles file drop onto the drop zone, updates the selected file and locks the inputs.
   * @param {React.DragEvent<HTMLDivElement>} event - The drop event triggered when a file is dropped.
   */
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

  /**
   * Handles the drag-over state (called repeatedly when file is dragged over).
   * @param {React.DragEvent<HTMLDivElement>} event - The drag event triggered during the drag-over.
   */
  const handleDragOver = (event) => {
    event.preventDefault();
    setIsDragOver(true);
  };

  /**
   * Handles the end of the drag-over state (called when the file is no longer dragged over).
   */
  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  /**
   * Resets the file and text selections, and unlocks the input fields.
   */
  const resetSelections = () => {
    setSelectedFile(null);
    setCopiedText('');
    onFileUpload([]);
    onTextChange('');
    setIsLocked(false);
  };

  return (
    <div className="container">
      <h2>Upload a file or copy and paste text for analysis. You can clear your selection by pressing the Reset Selections button.</h2>
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