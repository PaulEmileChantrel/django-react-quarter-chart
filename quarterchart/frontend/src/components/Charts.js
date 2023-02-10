import React from 'react';
import { Chart } from "react-google-charts";

export default function Charts ({data}){

    return (
        <Chart
            chartType="Bar"
            data={data}
            width="80%"
            height="300px"
            legendToggle
            />
    )
};