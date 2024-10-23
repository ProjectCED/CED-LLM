import React, { useState, useEffect } from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Call backend API
    fetch('http://localhost:5000/api/data')
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error('Error fetching data:', error));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Calling Flask API from React</h1>
        {data ? <p>{data.message}</p> : <p>Loading...</p>}
      </header>
    </div>
  );
}

export default App;

