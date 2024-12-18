import React, { useState } from 'react';
import './AddBlueprint.css'; 

/**
 * The AddBlueprint component provides a user interface for creating a new blueprint.
 * Users can specify a name, description, and a list of questions for the blueprint.
 *
 * @component
 * @param {Object} props - The props passed to the component.
 * @param {Function} props.onAdd - Function called when the blueprint is saved.
 *        It receives an object containing `name`, `description`, and `questions`.
 * @param {Function} props.onCancel - Function called when the user cancels the action.
 */
const AddBlueprint = ({ onAdd, onCancel }) => {
  const [newBlueprintName, setNewBlueprintName] = useState('');
  const [newBlueprintDescription, setNewBlueprintDescription] = useState(''); 
  const [newQuestion, setNewQuestion] = useState('');
  const [questions, setQuestions] = useState([]);

  /**
   * Handles adding a new question to the list.
   * Prevents adding empty questions by trimming whitespace.
   */
  const handleAddQuestion = () => {
    // Only add the question if it's not empty (after trimming white spaces)
    if (newQuestion.trim()) {
      setQuestions((prevQuestions) => [...prevQuestions, newQuestion.trim()]);
      setNewQuestion(''); 
    }
  };

  /**
   * Removes a question from the list by its index.
   *
   * @param {number} index - The index of the question to remove.
   */
  const handleRemoveQuestion = (index) => {
    // Filter out the question at the specified index
    setQuestions((prevQuestions) => 
      prevQuestions.filter((_, i) => i !== index)
    );
  };

  /**
   * Handles saving the blueprint.
   * Ensures that the name field is filled before proceeding.
   * Calls the `onAdd` prop with the blueprint data and resets the form fields.
   */
  const handleSave = () => {
    // If the blueprint name is empty, show an alert
    if (!newBlueprintName.trim()) {
      alert('Name is required!'); 
      return;
    }
    // Call the onAdd function passed via props to save the blueprint data
    onAdd({
      name: newBlueprintName,
      description: newBlueprintDescription, 
      questions,
    });
    // Reset the form fields after saving
    setNewBlueprintName('');
    setNewBlueprintDescription(''); 
    setQuestions([]);
  };

  return (
    <div className="new-blueprint-form">
      <h2>Add new blueprint</h2>
      <div className="input-group">
        <span>Name *</span>
        <input
          type="text"
          placeholder="Enter name for the blueprint"
          value={newBlueprintName}
          onChange={(e) => setNewBlueprintName(e.target.value)}
        />
      </div>
      <div className="input-group">
        <span>Description</span>
        <input
          type="text"
          placeholder="Enter description for the blueprint"
          value={newBlueprintDescription}
          onChange={(e) => setNewBlueprintDescription(e.target.value)}
        />
      </div>
      <div className="input-group">
        <span>Type a question for the AI</span>
        <div className="input-with-button">
          <input
            type="text"
            placeholder="Enter question for the AI"
            value={newQuestion}
            onChange={(e) => setNewQuestion(e.target.value)}
          />
          <button 
            onClick={handleAddQuestion} 
            aria-label="Add question"
          >
            +
          </button>
        </div>
      </div>
      <div className="questions-list">
        {questions.map((question, index) => (
          <div key={index} className="question-item">
            {question}
            <button 
              onClick={() => handleRemoveQuestion(index)} 
              aria-label={`Remove question ${question}`}
            >
              &#10005;
            </button>
          </div>
        ))}
      </div>
       {/* Button group for saving or cancelling the form */}
      <div className="button-group">
        <button className="save-button-add" onClick={handleSave}>
          SAVE
        </button>
        <button className="cancel-button" onClick={onCancel}>
          CANCEL
        </button>
      </div>
      <p className="required-note">Fields marked with * are required</p>
    </div>
  );
};

export default AddBlueprint;