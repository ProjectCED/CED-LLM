export const getBlueprints = async () => {
    const response = await fetch('/api/get_blueprints', {
      method: 'GET'
    }); 
    const blueprints = await response.json();
    return blueprints;
};

export const analyzeUploadedFile = async (filename) => {
const response = await fetch('/api/analyze_file', {
    method: 'POST',
    body: filename,
    });

    let data = await response.json();
    data = data.replace(/\\n/g, '<br />');
    return data;
};

export const saveBlueprint = async (blueprint) => {
    const response = await fetch('/api/save_blueprint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(blueprint)
    });
    const id = await response.text();
    return id;
};

export const deleteBlueprint = async (id) => {
  const response = await fetch('/api/delete_blueprint', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ id })
  });
  const data = await response.json();
  return data.success;
};

export const testMistral = async () => {
    const response = await fetch("/api/mistral", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "prompt": "Explain the theory of relativity in layman's terms."
        })
    });
    const data = await response.json();
    console.log(data);
    return data;
}