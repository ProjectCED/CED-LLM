/**
 * BlueprintDropdown renders a dropdown menu for selecting a blueprint from a list of options.
 *
 * @component
 * @param {Object} props - The props passed to the component.
 * @param {Array<{name: string}>} props.blueprints - Array of blueprint objects. Each blueprint should have a `name` property.
 * @param {Object|null} props.selectedBlueprint - The currently selected blueprint object. Can be null if no blueprint is selected.
 * @param {Function} props.onSelectBlueprint - Callback function called when a blueprint is selected. 
 *        Receives the index of the selected blueprint as an argument.
 * @returns {JSX.Element} The dropdown menu for selecting a blueprint.
 */
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