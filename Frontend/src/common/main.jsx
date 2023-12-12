import React, { useContext } from 'react';
import ReactDOM from 'react-dom/client';
import Routing from './Routing';
import { BrowserRouter } from 'react-router-dom';


function App() {
  

  return (
    <React.StrictMode>
      <BrowserRouter>

          <div className='main-container'>
            <div className='main-content'>
              <Routing />
            </div>
          </div>

      </BrowserRouter>
    </React.StrictMode>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);