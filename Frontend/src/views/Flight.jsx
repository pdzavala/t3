import React, { useState, useEffect } from 'react';
import { Box } from '@mui/material';
import { DataGrid, GridToolbar, gridClasses } from '@mui/x-data-grid';
import Typography from '@mui/material/Typography';
import { alpha, styled } from '@mui/material/styles';
import { useParams } from 'react-router-dom';
import axios from 'axios';

import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';

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

const Flight = () => {
  const [flight, setFlight] = useState([]);
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const { flightNumber } = useParams();

  useEffect(() => {
    console.log('flightNumber:', flightNumber);
    axios
      .get(`https://t3-backend-0esd.onrender.com/flights/${flightNumber}`)
      .then((response) => {
        console.log(response.data);
        const flightData = response.data.map((flight, index) => ({ ...flight, id: index })); 
        setFlight(flightData);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
      axios
      .get(`https://t3-backend-0esd.onrender.com/flightPassengers/${flightNumber}`)
      .then((response) => {
        console.log(response.data);
        const passengersData = response.data.map((passenger, index) => ({ ...passenger, id: index })); 
        setRows(passengersData);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [flightNumber]);
  ['avatar', 'firstName', 'lastName', 'age', 'gender', 'weight(kg)', 'height(cm)', 'seatNumber']
  const columns = [
    { field: 'avatar', headerName: 'avatar', width: 150 },
    { field: 'firstName', headerName: 'Nombre', width: 250 },
    { field: 'lastName', headerName: 'Apellido', width: 150 },
    { field: 'age', headerName: 'Edad', width: 100 },
    { field: 'gender', headerName: 'Género', width: 250 },
    { field: 'weight(kg)', headerName: 'Peso(kg)', width: 250 },
    { field: 'height(cm)', headerName: 'Estatura (cm)', width: 150 },
    { field: 'seatNumber', headerName: 'Número de asiento', width: 150 },
    

  ];

  if (loading) {
    return (
      <div>
        <Typography variant="h6">Cargando...</Typography>
      </div>
    );
  }

  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">Información vuelo número: {flightNumber}</Typography>
        </Toolbar>
      </AppBar>
      
    
      <Box>
        <Typography variant="h6">Información del vuelo</Typography>
        <Typography variant="h6">Aerolínea: {flight[0].airline}</Typography>
        <Typography variant="h6">Origen: {flight[0].name_origin}</Typography>
        <Typography variant="h6">Destino: {flight[0].name_destination}</Typography>
        <Typography variant="h6">Año: {flight[0].year}</Typography>
        <Typography variant="h6">Mes: {flight[0].month}</Typography>
        
      </Box>
      
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">Pasajeros</Typography>
        </Toolbar>
      </AppBar>
      <Box sx={{ height: 700, width: '100%', mx: 'auto', mt: 2 }}>
        <StripedDataGrid
          slots={{ Toolbar: GridToolbar }}
          rows={rows}
          columns={columns}
          getRowClassName={(params) =>
            params.indexRelativeToCurrentPage % 2 === 0 ? 'even' : 'odd'
          }
          
          getRowId={(row) => row.id}
        />
      </Box>
    </div>
  );
};

export default Flight;


    
