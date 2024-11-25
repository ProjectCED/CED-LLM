// Component renders a dropdown menu for selecting a blueprint from a list of options
const BlueprintDropdown = ({ blueprints, selectedBlueprint, onSelectBlueprint }) => {
    return (
      <div className="dropdown-container">
        {/* Render a select element for choosing a blueprint */}
        <select
          id="blueprint-select"
          value={selectedBlueprint}
          onChange={(e) => onSelectBlueprint(e.target.value)}
        >
          {/* Default option prompting the user to select a blueprint */}
          <option value="">-- Select a saved blueprint --</option>
          {/* Iterate over the blueprints array and create an option element for each blueprint */}
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