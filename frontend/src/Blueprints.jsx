import React, { useState, useEffect } from 'react';
import AddBlueprint from './AddBlueprint'; 
import './Blueprints.css';
import { getBlueprints, saveBlueprint, deleteBlueprint } from './utils';

const Blueprints = () => {
  // State to hold the array of blueprints. Each blueprint has properties: 
  // id, name, description, question, addedQuestions (array), and editing (boolean)
  const [blueprints, setBlueprints] = useState([]);

  // State to manage whether the user is adding a new blueprint
  const [isAdding, setIsAdding] = useState(false); 

  // State to display a success message when a new blueprint is saved
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);

  // Loading blueprints
  useEffect(() => {
    getBlueprints().then((bps) => {
      const bps2 = bps.map((bp) => ({
        id: bp.id,
        name: bp.name,
        description: bp.description,
        question: bp.questions[0],
        addedQuestions: bp.questions.slice(1),
        editing: false,
      }));
      setBlueprints(bps2);
    });
  }, []);

  // Function to handle the addition of a new blueprint
  const handleAddNewBlueprint = (blueprint) => {
    const newBlueprint = {
      id: null, // ID should be set on the database side
      name: blueprint.name,
      description: blueprint.description, 
      question: '', 
      addedQuestions: blueprint.questions, 
      editing: false,
    };
    const id = saveBlueprint(newBlueprint);
    newBlueprint.id = id;
    setBlueprints([...blueprints, newBlueprint]);
    setIsAdding(false); 
    setShowSuccessMessage(true); 

    // Hide the success message after 3 seconds
    setTimeout(() => {
      setShowSuccessMessage(false);
    }, 3000);
  };

  // Toggle edit mode for the blueprint with the given ID
  const handleEditClick = (id) => {
    setBlueprints(blueprints.map(bp => 
      bp.id === id ? { ...bp, editing: !bp.editing } : bp
    ));
  };

  // Save changes to the blueprint by turning off edit mode
  const handleSaveClick = (id) => {
    setBlueprints(blueprints.map(bp => 
      bp.id === id ? { ...bp, editing: false } : bp
    ));
  };

  // Delete a blueprint by filtering it out of the blueprints array
  const handleDeleteClick = (id) => {
    const confirmDelete = window.confirm('Are you sure you want to delete this blueprint?');
    if (confirmDelete) {
      const success = deleteBlueprint(id);
      if (success) {
        setBlueprints(blueprints.filter(bp => bp.id !== id));
      }
    }
  };

  // Update the 'question' property for the blueprint when the input changes
  const handleInputChange = (id, value) => {
    setBlueprints(blueprints.map(bp => 
      bp.id === id ? { ...bp, question: value } : bp
    ));
  };

  // Add the current question to the addedQuestions array and clear the input
  const handleAddQuestionClick = (id) => {
    setBlueprints(blueprints.map(bp =>
      bp.id === id && bp.question ? { ...bp, addedQuestions: [...bp.addedQuestions, bp.question], question: '' } : bp
    ));
  };

  // Remove a specific question from the addedQuestions array
  const handleRemoveQuestionClick = (bpId, questionIndex) => {
    setBlueprints(blueprints.map(bp => 
      bp.id === bpId 
      ? { ...bp, addedQuestions: bp.addedQuestions.filter((_, index) => index !== questionIndex) } 
      : bp
    ));
  };

  return (
    <div className="blueprints-container">
      {showSuccessMessage && (
        <div className="success-message">
          Blueprint saved successfully!
        </div>
      )}
      
      <button className="add-button" onClick={() => setIsAdding(true)}>Add new blueprint</button>
      
      {isAdding && (
        <div className="modal-overlay">
          <div className="modal-content">
            <AddBlueprint 
              onAdd={handleAddNewBlueprint}
              onCancel={() => setIsAdding(false)}
            />
          </div>
        </div>
      )}
      
      {blueprints.map(blueprint => (
        <div key={blueprint.id} className="blueprint-card">
          <div className="blueprint-header">
            <span>{blueprint.name}</span>
            <button className="edit-button" onClick={() => handleEditClick(blueprint.id)}>
              {blueprint.editing ? 'Close' : 'Edit'}
            </button>
          </div>
          {blueprint.editing && (
            <div className="blueprint-body">
              {/* Display blueprint description */}
              <p>{blueprint.description}</p>
              <p>Type a question for the AI</p>
              
              <div className="blueprint-input-container">
                <input
                  type="text"
                  placeholder="Enter question for the AI"
                  value={blueprint.question}
                  onChange={(e) => handleInputChange(blueprint.id, e.target.value)}
                />
                <button 
                  className="add-question-button" 
                  onClick={() => handleAddQuestionClick(blueprint.id)}
                >
                  +
                </button>
              </div>

              <div className="question-container">
                {blueprint.addedQuestions.length > 0 ? (
                  <ul>
                    {blueprint.addedQuestions.map((q, index) => (
                      <li key={index} className="question-item">
                        <span>{q}</span>
                        <span 
                          className="remove-button" 
                          onClick={() => handleRemoveQuestionClick(blueprint.id, index)}
                        >
                          &#10005; {/* X mark */} 
                        </span>
                      </li>
                    ))}
                  </ul>
                ) : null}
              </div>

              <div className="blueprint-actions">
                <button className="delete-button" onClick={() => handleDeleteClick(blueprint.id)}>
                  Delete
                </button>
                <button className="save-button" onClick={() => handleSaveClick(blueprint.id)}>
                  Save
                </button>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default Blueprints;