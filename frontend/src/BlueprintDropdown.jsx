const BlueprintDropdown = ({ blueprints, selectedBlueprint, onSelectBlueprint }) => {
  return (
    <div className="dropdown-container">
      <select
        id="blueprint-select"
        value={selectedBlueprint}
        onChange={(e) => {
          const index = parseInt(e.target.value);
          onSelectBlueprint(index);
        }}
      >
        <option value="">-- Select a saved blueprint --</option>
        {blueprints.map(([id, name], index) => (
          <option key={index} value={index}>
            {name}
          </option>
        ))}
      </select>
    </div>
  );
};
  
  export default BlueprintDropdown;