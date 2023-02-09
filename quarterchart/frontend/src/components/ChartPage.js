import React from 'react';
import {useParams} from 'react-router-dom'
import {Grid,Typography,Button}  from '@material-ui/core';
import {useState,useRef,useEffect} from 'react'
import { Chart } from "react-google-charts";


export default function ChartPage () {
    const [dataQ,setDataQ] = useState([])
    const [dataA,setDataA] = useState([])
    const [showQuarters,setShowQuarters] = useState(true)
    const {ticker} = useParams();
    useEffect(()=>{
        getComapanieInfo()
    },[])
    function getComapanieInfo(){
        fetch('/api/get-company-chart?ticker='+ticker).then(res=>res.json())
        .then(data=>{
            console.log(data)
            setDataQ(data['quarter'])
            setDataA(data['annual'])
            setShowQuarters(data['time_periode']==='quarter')
            
        })
    
    }
    function updateTimeframe(e,timeframe){
        if ((timeframe==='annual' && showQuarters)||(timeframe=== 'quarter' && !showQuarters)){
            setShowQuarters(!showQuarters)

            const requestOptions = {
                method: 'PATCH',
                headers :{'Content-Type': 'application/json'},
                body: JSON.stringify({time_periode:timeframe}),
            }
            console.log(JSON.stringify({time_periode:timeframe}))
            fetch('/api/update-session-time-periode',requestOptions)
            .then(res=>console.log(res))
  
    }}


    return (<Grid container spacing={1}>
        <Grid item xs={12} align="center">
            <Typography component="h5" variant="h5" > {ticker} Charts</Typography>
        </Grid>
        { showQuarters ?
        <Grid item xs={12} align="center">
        
            <Button variant="contained"  color="primary" onClick={e => updateTimeframe(e,'quarter')}>Quarter</Button>
            <Button variant="contained" color="secondary" onClick={e =>updateTimeframe(e,'annual')}>Annual</Button>
            
        </Grid>:
        <Grid item xs={12} align="center">
        
            <Button variant="contained"  color="secondary" onClick={e => updateTimeframe(e,'quarter')}>Quarter</Button>
            <Button variant="contained" color="primary" onClick={e =>updateTimeframe(e,'annual')}>Annual</Button>
            
        </Grid>
        }
        <Grid item xs={12} align="center">
        { showQuarters ?
        <Chart
            chartType="Bar"
            data={dataQ}
            width="100%"
            height="400px"
            legendToggle
            
        />
        : 
        <Chart
            chartType="Bar"
            data={dataA}
            width="100%"
            height="400px"
            legendToggle
            
        />
        
        }
        </Grid>

    </Grid>)
  
};

  