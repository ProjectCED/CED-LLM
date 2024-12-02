export const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch('/api/upload_file', {
        method: 'POST',
        body: formData
    });
    const filename = await response.text();
    return filename;
};

export const analyzeUploadedFile = async (filename, blueprint) => {
const response = await fetch('/api/analyze_file', {
        method: 'POST',
        body: JSON.stringify({ filename, blueprint }),
        headers: {
            'Content-Type': 'application/json'
        }
    });

    let data = await response.json();
    data = data.replace(/\\n/g, '<br />');
    return data;
};

export const analyzeText = async (text, blueprint) => {
    const response = await fetch('/api/analyze_text', {
        method: 'POST',
        body: JSON.stringify({ text, blueprint }),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    let data = await response.json();
    data = data.replace(/\\n/g, '<br />');
    return data;
}

export const getBlueprints = async () => {
    const response = await fetch('/api/get_blueprints', {
      method: 'GET'
    }); 
    const blueprints = await response.json();
    return blueprints;
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

export const getResults = async (project_id) => {
    const response = await fetch('/api/get_results_under_project', {
        method: 'POST',
        body: JSON.stringify({ project_id }),
    });
    const results = await response.json();
    return results;
    }