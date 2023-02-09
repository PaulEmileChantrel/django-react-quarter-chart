import React from 'react';
import {useParams} from 'react-router-dom'
import {Grid,Typography}  from '@material-ui/core';
import {useState,useRef,useEffect} from 'react'
import { Chart } from "react-google-charts";


export default function ChartPage () {
    const [data,setData] = useState([])
    
    const {ticker} = useParams();
    useEffect(()=>{
        getComapanieInfo()
    },[])
    function getComapanieInfo(){
        fetch('/api/get-company-chart?ticker='+ticker+'&time=quarter').then(res=>res.json())
        .then(data=>{
            console.log(data)
            setData(data)
            
        })
    
    }


    return (<Grid container spacing={1}>
        <Grid item xs={12} align="center">
            <Typography component="h5" variant="h5" > {ticker} Charts</Typography>
        </Grid>
        <Grid item xs={12} align="center">
        { data ?
        <Chart
            chartType="Bar"
            data={data}
            width="100%"
            height="400px"
            legendToggle
            
        />
        : null}
        </Grid>

    </Grid>)
  
};

  