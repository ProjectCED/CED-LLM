// Files & analysis
/**
 * Uploads a file to the backend server for later analysis.
 * @param {File} file PDF or text file to upload to server for analysis.
 * @returns {Promise<string>} Filename of the uploaded file.
 */
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

/**
 * Analyzes an already uploaded file using the provided blueprint.
 * @param {string} filename Filename of the uploaded file to analyze.
 * @param {Object} blueprint Blueprint to use for analysis, containing questions for LLM.
 * @returns {Promise<string>} Analysis result text with line breaks replaced by <br />.
 */
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

/**
 * Analyzes raw text using the provided blueprint.
 * @param {string} text Raw text to be analyzed using LLM.
 * @param {Object} blueprint Blueprint to use for analysis, containing questions for LLM.
 * @returns {Promise<string>} Analysis result text with line breaks replaced by <br />.
 */
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
/**
 * Fetches all user-saved blueprints from the backend server.
 * @returns {Promise<Array>} Array of blueprints with all properties.
 */
export const getBlueprints = async () => {
    const response = await fetch('/api/get_blueprints', {
      method: 'GET'
    }); 
    const blueprints = await response.json();
    return blueprints;
};

/**
 * Saves a given blueprint to backend database.
 * @param {Object} blueprint Blueprint with all properties to be saved.
 *  If the blueprint contains an ID, it will be updated in the database.
 * @returns {Promise<string>} ID of the saved/updated blueprint.
 */
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

/**
 * Deletes the blueprint with given ID from the backend database.
 * @param {string} id UUID-type ID of the blueprint to be deleted.
 * @returns {Promise<Boolean>} True if the blueprint was successfully deleted, false if not.
 */
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
// Projects
/**
 * Creates a new project with the given name, saving it to the backend database.
 *  The project will be have an empty results list initially.
 * @param {string} projectName Name of the new project. 
 * @returns {Promise<string>} ID of the newly created project.
 */
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

/**
 * Fetches all projects from the backend server. Projects contain
 *  their ID, name, and results list. Results contain all relevant data,
 *  including the blueprint used for analysis.
 * @returns {Promise<Array>} Array of projects with all properties.
 */
export const getProjects = async () => {
    const response = await fetch('/api/get_projects', {
        method: 'GET'
    });
    const projects = await response.json();
    return projects;
};

/**
 * Deletes a project from the backend database. Also deletes all results
 *  under the project (but not their blueprints).
 * @param {string} id ID of the project to be deleted. 
 * @returns {Promise<Boolean>} True if the project was successfully deleted, false if not.
 */
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
/**
 * Saves an analysis result to the backend database.
 * @param {Object} result Result object with all properties except ID attached.
 * @returns {Promise<string>} ID of the saved result.
 */
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

/**
 * Deletes an analysis result from the backend database. Will NOT delete attached blueprint.
 * @param {string} id ID of the result to be deleted.
 * @returns {Promise<Boolean>} True if the result was successfully deleted, false if not.
 */
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