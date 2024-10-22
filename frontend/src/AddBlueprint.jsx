import React, { useState } from 'react';
import './AddBlueprint.css'; 

const AddBlueprint = ({ onAdd, onCancel }) => {
  const [newBlueprintName, setNewBlueprintName] = useState('');
  const [newBlueprintDescription, setNewBlueprintDescription] = useState(''); 
  const [newQuestion, setNewQuestion] = useState('');
  const [questions, setQuestions] = useState([]);

  // Function to handle adding a new question
  const handleAddQuestion = () => {
    // Only add the question if it's not empty (after trimming white spaces)
    if (newQuestion.trim()) {
      setQuestions((prevQuestions) => [...prevQuestions, newQuestion.trim()]);
      setNewQuestion(''); 
    }
  };

  // Function to remove a specific question by index
  const handleRemoveQuestion = (index) => {
    // Filter out the question at the specified index
    setQuestions((prevQuestions) => 
      prevQuestions.filter((_, i) => i !== index)
    );
  };

  // Function to handle saving the blueprint
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
            + {/* Plus symbol for the button */}
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
              &#10005; {/* X symbol (cross) for the remove button */}
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
      {/* Note indicating required fields */}
      <p className="required-note">Fields marked with * are required</p>
    </div>
  );
};

export default AddBlueprint;