import React from 'react';
import { Chart } from "react-google-charts";

export default function Charts ({data,title}){
    console.log(data)
    return (<>{data.length?<>
        <h1>{title}</h1>
        <Chart
            chartType="Bar"
            data={data}
            width="80%"
            height="400px"
            options={{title: 'test'}}
            
            
            /></>:null}</>
    )
};