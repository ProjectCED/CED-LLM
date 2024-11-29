// Component renders a dropdown menu for selecting a blueprint from a list of options
const BlueprintDropdown = ({ blueprints, selectedBlueprint, onSelectBlueprint }) => {
  return (
    <div className="dropdown-container">
      {/* Render a select element for choosing a blueprint */}
      <select
        id="blueprint-select"
        value={selectedBlueprint && selectedBlueprint.name}
        onChange={(e) => {
          const index = parseInt(e.target.value);
          onSelectBlueprint(index);
        }}
      >
        {/* Default option prompting the user to select a blueprint */}
        <option value="">-- Select a saved blueprint --</option>
        {/* Iterate over the blueprints array and create an option element for each blueprint */}
        {blueprints.map((blueprint, index) => (
          <option key={index} value={index}>
            {blueprint.name}
          </option>
        ))}
      </select>
    </div>
  );
};
  
export default BlueprintDropdown;