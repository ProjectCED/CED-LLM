export const getBlueprints = async () => {
    const response = await fetch('http://127.0.0.1:5000/get_blueprints', {
      method: 'GET'
    }); 
    const blueprints = await response.json();
    return blueprints;
};

export const analyzeUploadedFile = async (filename) => {
const response = await fetch('http://127.0.0.1:5000/analyze_file', {
    method: 'POST',
    body: filename,
    });

    let data = await response.json();
    data = data.replace(/\\n/g, '<br />');
    return data;
};

export const saveBlueprint = async (blueprint) => {
    const response = await fetch('http://127.0.0.1:5000/save_blueprint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(blueprint)
    });
    const id = await response.text();
    return id;
};