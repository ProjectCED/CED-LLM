// Files & analysis
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

// Blueprints
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

// Projects
export const saveProject = async (projectName) => {
    const response = await fetch('/api/save_project', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ projectName })
    });
    const id = await response.text();
    return id;
}

export const getProjects = async () => {
    const response = await fetch('/api/get_projects', {
        method: 'GET'
    });
    const projects = await response.json();
    return projects;
};

export const deleteProject = async (id) => {
    const response = await fetch('/api/delete_project', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id })
    });
    const data = await response.json();
    return data.success;
}

// Results
export const saveResult = async (result) => {
    const response = await fetch('/api/save_result', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(result)
    });
    // TODO: Should contain result id and copied blueprint (used variant) id
    const id = await response.text();
    return id;
}

export const deleteResult = async (id) => {
    const response = await fetch('/api/delete_result', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id })
    });
    const data = await response.json();
    return data.success;
}