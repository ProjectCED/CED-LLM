import React, { useState, useEffect } from 'react';
import AddBlueprint from './AddBlueprint'; 
import './Blueprints.css';
import { getBlueprints, saveBlueprint, deleteBlueprint } from './utils';

/**
 * Blueprints component is responsible for displaying, adding, editing, saving, and deleting blueprints.
 * It also manages a modal for adding new blueprints and displays success messages.
 * 
 * @component
 * @returns {JSX.Element} The rendered Blueprints component with blueprint cards and modal for adding blueprints.
 */
const Blueprints = () => {
  /**
  * State to hold the array of blueprints.
  * Each blueprint contains:
  * - `id` {number | null}: Unique identifier for the blueprint (null if not yet saved).
  * - `name` {string}: Name of the blueprint.
  * - `description` {string}: Description of the blueprint.
  * - `question` {string}: Current question being added to the blueprint.
  * - `addedQuestions` {Array<string>}: List of questions already added to the blueprint.
  * - `editing` {boolean}: Indicates whether the blueprint is in edit mode.
  * @type {Array<{id: number | null, name: string, description: string, question: string, addedQuestions: Array<string>, editing: boolean}>}
  */
  const [blueprints, setBlueprints] = useState([]);

  /**
  * State to manage whether the user is adding a new blueprint.
  * @type {boolean}
  */
  const [isAdding, setIsAdding] = useState(false); 

  /**
  * State to display a success message when a new blueprint is saved.
  * @type {boolean}
  */
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);

  /**
   * Loads blueprints from a data source when the component mounts.
   */
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

  /**
   * Handles the addition of a new blueprint.
   * 
   * @param {Object} blueprint - The blueprint object containing name, description, and questions.
   * @param {string} blueprint.name - The name of the blueprint.
   * @param {string} blueprint.description - The description of the blueprint.
   * @param {Array<string>} blueprint.questions - The questions associated with the blueprint.
   */
  const handleAddNewBlueprint = async (blueprint) => {
    const newBlueprint = {
      id: null, // ID should be set on the database side
      name: blueprint.name,
      description: blueprint.description, 
      question: '', 
      addedQuestions: blueprint.questions, 
      editing: false,
    };
    const id = await saveBlueprint(newBlueprint);
    newBlueprint.id = id;
    setBlueprints([...blueprints, newBlueprint]);
    setIsAdding(false); 
    setShowSuccessMessage(true); 

    // Hide the success message after 3 seconds
    setTimeout(() => {
      setShowSuccessMessage(false);
    }, 3000);
  };

  /**
   * Toggles the edit mode for the blueprint with the given ID.
   * 
   * @param {number} id - The ID of the blueprint to toggle edit mode.
   */
  const handleEditClick = (id) => {
    setBlueprints(blueprints.map(bp => 
      bp.id === id ? { ...bp, editing: !bp.editing } : bp
    ));
  };

    /**
   * Saves the changes to the blueprint by turning off the edit mode.
   * 
   * @param {string} id - The ID of the blueprint to save.
   */
  const handleSaveClick = async (id) => {
    const bp = blueprints.find(bp => bp.id === id);
    await saveBlueprint(bp);
    setBlueprints(blueprints.map(bp => 
      bp.id === id ? { ...bp, editing: false } : bp
    ));
  };

  /**
   * Deletes a blueprint by filtering it out of the blueprints array.
   * 
   * @param {number} id - The ID of the blueprint to delete.
   */
  const handleDeleteClick = (id) => {
    const confirmDelete = window.confirm('Are you sure you want to delete this blueprint?');
    if (confirmDelete) {
      const success = deleteBlueprint(id);
      if (success) {
        setBlueprints(blueprints.filter(bp => bp.id !== id));
      }
    }
  };

  /**
   * Updates the 'question' property for the blueprint when the input changes.
   * 
   * @param {number} id - The ID of the blueprint to update.
   * @param {string} value - The new question value to set.
   */
  const handleInputChange = (id, value) => {
    setBlueprints(blueprints.map(bp => 
      bp.id === id ? { ...bp, question: value } : bp
    ));
  };

  /**
   * Adds the current question to the addedQuestions array and clears the input.
   * 
   * @param {number} id - The ID of the blueprint to add the question to.
   */
  const handleAddQuestionClick = (id) => {
    setBlueprints(blueprints.map(bp =>
      bp.id === id && bp.question ? { ...bp, addedQuestions: [...bp.addedQuestions, bp.question], question: '' } : bp
    ));
  };

  /**
   * Removes a specific question from the addedQuestions array.
   * 
   * @param {number} bpId - The ID of the blueprint.
   * @param {number} questionIndex - The index of the question to remove.
   */
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
                          &#10005;  
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