export const getBlueprints = async () => {
    const response = await fetch('http://127.0.0.1:5000/get_blueprints', {
      method: 'GET'
    }); 
    const blueprints = await response.json();
    return blueprints;
  };