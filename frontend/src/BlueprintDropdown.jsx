const BlueprintDropdown = ({ blueprints, selectedBlueprint, onSelectBlueprint }) => {
  return (
    <div className="dropdown-container">
      <select
        id="blueprint-select"
        value={selectedBlueprint && selectedBlueprint.name}
        onChange={(e) => {
          const index = parseInt(e.target.value);
          onSelectBlueprint(index);
        }}
      >
        <option value="">-- Select a saved blueprint --</option>
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