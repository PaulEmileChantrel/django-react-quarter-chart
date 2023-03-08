import React, { useState } from 'react';


import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import formatMktCp from './formatMktCap';


ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);






export function ReactBarChart({dataQ, title}) {
  
  const [options,setOptions] = useState({
    responsive: true,
    scales: {
      y: {
          ticks: {  callback : function(value,index,array) { return  formatMktCp(value) }}}},
    
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: title,
        font:{size:30}
      },
    },
  })
  
  
  console.log(dataQ)
  return <Bar options={options} data={dataQ} />;
}
