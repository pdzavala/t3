import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box} from '@mui/material';
import { DataGrid,  GridToolbar, gridClasses} from '@mui/x-data-grid';
import Typography from '@mui/material/Typography';
import { alpha, styled } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import TablePagination from '@mui/material/TablePagination';
import { useNavigate } from 'react-router-dom';
import Flight from '../views/Flight';

const ODD_OPACITY = 0.2;
 

const StripedDataGrid = styled(DataGrid)(({ theme }) => ({
    [`& .${gridClasses.row}.even`]: {
      backgroundColor: "#d6d4ff3b",
      '&:hover, &.Mui-hovered': {
        backgroundColor: alpha(theme.palette.primary.main, ODD_OPACITY),
        '@media (hover: none)': {
          backgroundColor: 'transparent',
        },
      },
      '&.Mui-selected': {
        backgroundColor: alpha(
          theme.palette.primary.main,
          ODD_OPACITY + theme.palette.action.selectedOpacity,
        ),
        '&:hover, &.Mui-hovered': {
          backgroundColor: alpha(
            theme.palette.primary.main,
            ODD_OPACITY +
              theme.palette.action.selectedOpacity +
              theme.palette.action.hoverOpacity,
          ),
          // Reset on touch devices, it doesn't add specificity
          '@media (hover: none)': {
            backgroundColor: alpha(
              theme.palette.primary.main,
              ODD_OPACITY + theme.palette.action.selectedOpacity,
            ),
          },
        },
      },
    },
  }));

function App() {
    const [loading, setLoading] = useState(true);
    const [rows, setRows] = useState([]);
    const navigate = useNavigate();
  
    useEffect(() => {
      axios.get('https://t3-backend-0esd.onrender.com/getflights')
        .then((response) => {
          console.log('Type of response.data:', typeof response.data);
          const flightsData = response.data.map((flight, index) => ({ ...flight, id: index }));
          setRows(flightsData);
          setLoading(false);
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
          setLoading(false);
        });
    }, []);

    const columns = [
      {
        field: 'flightNumber',
        headerName: 'Vuelo',
        width: 150,
        renderCell: (params) => (
          <div
            style={{ cursor: 'pointer' }}
            onClick={() => navigate(`/flight/${params.row.flightNumber}`)}
          >
            {params.row.flightNumber}
          </div>
        ),
      },
      { field: 'name_origin', headerName: 'Origen', width: 250 },
      { field: 'name_destination', headerName: 'Destino', width: 150 },
      { field: 'airline', headerName: 'Aerolínea', width: 200 },
      { field: 'year', headerName: 'Año', width: 100 },
      { field: 'month', headerName: 'Mes', width: 100 },
      { field: 'edad_promedio', headerName: 'Edad Promedio', width: 150 },
      { field: 'cantidad_pasajeros', headerName: 'Cantidad Pasajeros', width: 150 },
      { field: 'distancia', headerName: 'Distancia', width: 150 },
    ];
  const [pg, setpg] = React.useState(0); 
  const [rpg, setrpg] = React.useState(15); 
  
    function handleChangePage(event, newpage) { 
        setpg(newpage); 
    } 
  
    function handleChangeRowsPerPage(event) { 
        setrpg(parseInt(event.target.value, 10)); 
        setpg(0); 
    }
  
  return (
    <div className="App">
      
      {loading ? (
        <div>
        <AppBar position="static">
          <Toolbar>
            
            <Typography variant="h6">
              Cargando datos de vuelos...
            </Typography>
            
          </Toolbar>
        </AppBar>
        
        </div>
      ) : (
        <div>
            <AppBar position="static">
            <Toolbar>
              
              <Typography variant="h6">
                Flights
              </Typography>
              
            </Toolbar>
          </AppBar>
          <Box sx={{ height: 'auto', width: '100%', mx: 'auto', mt: 2 }}>
            <StripedDataGrid
              slots={{ Toolbar: GridToolbar }}
              rows={rows}
              columns={columns}
              getRowClassName={(params) =>
                params.indexRelativeToCurrentPage % 2 === 0 ? 'even' : 'odd'
              }
              
              getRowId={(row) => row.id}
              
              rowsPerPageOptions={[]} 
              component="div"
              count={rows.length} 
              rowsPerPage={rpg} 
              page={pg} 
              onPageChange={handleChangePage} 
              onRowsPerPageChange={handleChangeRowsPerPage} 
              onSelectionModelChange={(selection) => {
                if (selection.length > 0) {
                  const selectedFlight = rows.find((row) => row.id === selection[0]);
                  if (selectedFlight) {
                    console.log(selectedFlight.flightNumber);
                    navigate(`/flight/${selectedFlight.flightNumber}`);
                  }
                }
              }}
              
            />
           
          </Box>
        </div>
      )}
    </div>
  );
}

export default App;
