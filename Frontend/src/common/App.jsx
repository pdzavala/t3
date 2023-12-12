import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [flights, setFlights] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('https://t3-backend-0esd.onrender.com/loadflights')
      .then((response) => {
        console.log(response);
        setFlights(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, []);

  return (
    <div className="App">
      <h1>Taller Integración</h1>
      {loading ? (
        <p>Cargando...</p>
      ) : (
        <div>
          <h2>Datos cargados:</h2>
          
        </div>
      )}
    </div>
  );
}

export default App;
