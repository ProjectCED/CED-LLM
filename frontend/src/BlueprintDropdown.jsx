const BlueprintDropdown = ({ blueprints, selectedBlueprint, onSelectBlueprint }) => {
    return (
      <div className="dropdown-container">
        
        <select
          id="blueprint-select"
          value={selectedBlueprint}
          onChange={(e) => onSelectBlueprint(e.target.value)}
        >
          <option value="">-- Select a saved blueprint --</option>
          {blueprints.map((blueprint, index) => (
            <option key={index} value={blueprint}>
              {blueprint}
            </option>
          ))}
        </select>
      </div>
    );
  };
  
  export default BlueprintDropdown;