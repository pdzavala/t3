import React, { useState, useEffect } from 'react';
import { BarChart } from '@mui/x-charts';
import { PieChart } from '@mui/x-charts';
import { Pie, Cell, Legend, Tooltip } from '@mui/x-charts';

const Charts = () => {
    const [flights, setFlights] = useState([]);
    const [loading, setLoading] = useState(true);
    const [tickets, setTickets] = useState([]);
  
    useEffect(() => {
      fetch('https://t3-backend-0esd.onrender.com/getflights')
        .then((response) => response.json())
        .then((data) => {
          setFlights(data);
          
        });
        fetch('https://t3-backend-0esd.onrender.com/tickets')
        .then((response) => response.json())
        .then((data) => {
          setTickets(data);
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
  
    const pieChartData = Object.keys(airlines).map((airline) => ({
      airline,
      totalFlights: airlines[airline],
      firstClassFlights: firstClassByAirline[airline] || 0,
      economyFlights: economyByAirline[airline] || 0,
      businessFlights: businessByAirline[airline] || 0,
    }));
  
    const COLORS = ['#8884d8', '#82ca9d', '#ffc658']; // You can add more colors if needed
  
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
  
    return (
      <div>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <PieChart width={400} height={400}>
            <Pie
              dataKey="totalFlights"
              data={pieChartData}
              cx="50%"
              cy="50%"
              outerRadius={100}
              fill="#8884d8"
              label
            >
              {pieChartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Legend content={renderLegend} />
            <Tooltip />
          </PieChart>
        )}
      </div>
    );
  };

export default Charts;
