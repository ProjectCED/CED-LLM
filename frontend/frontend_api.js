import React, { useState } from 'react';

function App() {
  const [data, setData] = useState('');

  const handleAnalyze = () => {
    // Send POST-request to backend
    fetch('/api/analyze', {
      method: 'POST',
    })
      .then((response) => response.json())
      .then((data) => setData(data.result))
      .catch((error) => console.error('Error analyzing file:', error));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Anaylize File</h1>
        <button onClick={handleAnalyze}>Analyze</button>
        {data && <p>{data}</p>}
      </header>
    </div>
  );
}

export default App;

