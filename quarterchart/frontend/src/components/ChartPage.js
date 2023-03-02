import React from 'react';
import {useParams} from 'react-router-dom'
import {Grid,Typography,Button,Link}  from '@material-ui/core';
import {useState,useRef,useEffect} from 'react'
import { Chart } from "react-google-charts";
import OtherChart from './OtherChart';


export default function ChartPage () {
    const [dataQ,setDataQ] = useState([])
    const [dataA,setDataA] = useState([])
    const [otherChartDataQ,setOtherChartDataQ] = useState([])
    const [otherChartDataA,setOtherChartDataA] = useState([])
    const [showQuarters,setShowQuarters] = useState(true)
    const [show,setShow] = useState(false)
    const {ticker} = useParams();

    

    useEffect(()=>{
        getComapanieInfo()
    },[])
    function getComapanieInfo(){
        fetch('/api/get-first-company-chart?ticker='+ticker).then(res=>res.json())
        .then(data=>{
            console.log(data)
            setDataQ(data['quarter'])
            setDataA(data['annual'])
            setShowQuarters(data['time_periode']==='quarter')
            setShow(true)
            fetch('/api/get-other-company-chart?ticker='+ticker)
            .then(res=>res.json()).then(data=>{
                setOtherChartDataQ(data['quarter'])
                setOtherChartDataA(data['annual'])

            })
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
            <Link  href = {'/info/'+ticker} > more info</Link>
        </Grid>
        {show ?
        <Grid item xs={12} align="center">
        { showQuarters ?
        <Grid item xs={12} align="center">
        
            <Button variant="contained"  color="primary" onClick={e => updateTimeframe(e,'quarter')} style={{ margin: '1rem' }}>Quarter</Button>
            <Button variant="outlined" color="primary" onClick={e =>updateTimeframe(e,'annual')} style={{ margin: '1rem' }}>Annual</Button>
            
        </Grid>:
        <Grid item xs={12} align="center">
        
            <Button variant="outlined"  color="primary" onClick={e => updateTimeframe(e,'quarter')} style={{ margin: '1rem' }}>Quarter</Button>
            <Button variant="contained" color="primary" onClick={e =>updateTimeframe(e,'annual')} style={{ margin: '1rem' }}>Annual</Button>
            
        </Grid>
        }
        
        <Grid item xs={12} align="center" style={{ marginTop: '3rem' }}>
        { showQuarters?
        <>
        <h1>Revenue, Gross Profit and Operative Income</h1>
        <Chart
            chartType="Bar"
            data={dataQ}
            options={{title: 'Quarter'}}
            width="80%"
            height="400px"
            legendToggle={true}
            
            
        /></>
        : <>
        <h1>Revenue, Gross Profit and Operative Income</h1>
        <Chart
            chartType="Bar"
            data={dataA}
            width="80%"
            height="400px"
            legendToggle
            options={{title: 'Annual'}}
            
        />
        </>
        
        }
        </Grid>
        </Grid>:null}
        <OtherChart otherChartDataQ = {otherChartDataQ} otherChartDataA={otherChartDataA} showQuarters={showQuarters}/>

    </Grid>)
  
};

  