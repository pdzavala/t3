import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip } from 'recharts';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

const renderLegend = (props) => {
  const { payload } = props;

  return (
    <ul>
      {payload.map((entry, index) => (
        <li key={`item-${index}`}>
          <span style={{ backgroundColor: entry.color }} />
          {entry.value}
        </li>
      ))}
    </ul>
  );
};

const Chart = ({ dataKey, data, colors, legendTitle }) => {
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">{legendTitle}</Typography>
        </Toolbar>
      </AppBar>
      <PieChart width={400} height={400}>
        <Pie
          dataKey={dataKey}
          data={data}
          cx="50%"
          cy="50%"
          outerRadius={100}
          fill="#8884d8"
          label
        >
          {Object.keys(data[0]).map((key, index) => (
            <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
          ))}
        </Pie>
        <Legend content={renderLegend} />
        <Tooltip formatter={(value, name) => [`${name}: ${value} flights`, name]} />
      </PieChart>
    </div>
  );
};

const Charts = () => {
    const [flights, setFlights] = useState([]);
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
      fetch('https://t3-backend-0esd.onrender.com/getflightspass')
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          setFlights(data);
          setLoading(false);
        });
    }, []);

  const aggregateData = () => {
    const airlines = {};
    const firstClassByAirline = {};
    const economyByAirline = {};
    const businessByAirline = {};

    flights.forEach((flight) => {
      const airline = flight.airline;

      airlines[airline] = (airlines[airline] || 0) + 1;

      if (flight.class === 'First Class') {
        firstClassByAirline[airline] = (firstClassByAirline[airline] || 0) + 1;
      } else if (flight.class === 'Economy') {
        economyByAirline[airline] = (economyByAirline[airline] || 0) + 1;
      } else if (flight.class === 'Business') {
        businessByAirline[airline] = (businessByAirline[airline] || 0) + 1;
      }
    });

    return { airlines, firstClassByAirline, economyByAirline, businessByAirline };
  };
  const { airlines, firstClassByAirline, economyByAirline, businessByAirline } = aggregateData();

  const COLORS = ['#8884d8', '#82ca9d', '#ffc658'];

  const chartData = Object.keys(airlines).map((airline) => ({
    airline,
    totalFlights: airlines[airline] || 0,
    firstClassFlights: firstClassByAirline[airline] || 0,
    economyFlights: economyByAirline[airline] || 0,
    businessFlights: businessByAirline[airline] || 0,
  }));

  return (
    <div>
      {loading ? (
        <div>Cargando datos...</div>
      ) : (
        <div>
          
          <Chart dataKey="totalFlights" data={chartData} colors={COLORS} legendTitle="Vuelos por aerolínea" />
          <Chart dataKey="businessFlights" data={chartData} colors={COLORS} legendTitle="Vuelos Business" />
          <Chart dataKey="firstClassFlights" data={chartData} colors={COLORS} legendTitle="Vuelos First Class" />
          <Chart dataKey="economyFlights" data={chartData} colors={COLORS} legendTitle="Vuelos Economy" />
        </div>
      )}
    </div>
  );
};

export default Charts;