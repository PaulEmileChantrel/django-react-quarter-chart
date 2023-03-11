import React from 'react';
import {useParams} from 'react-router-dom'
import {Grid,Typography,Button,Link,ButtonGroup,Item}  from '@material-ui/core';
import {useState,useRef,useEffect} from 'react'
import { Chart } from "react-google-charts";
import { MDBBadge, MDBBtn, MDBTable, MDBTableHead, MDBTableBody } from 'mdb-react-ui-kit';

import {ReactBarChart} from './ReactBarChart';
import OtherChart from './OtherChart';
import formatMktCp from './formatMktCap';

export default function ChartPage () {
    const [dataQ,setDataQ] = useState([])
    const [dataA,setDataA] = useState([])
    const [otherChartDataQ,setOtherChartDataQ] = useState([])
    const [otherChartDataA,setOtherChartDataA] = useState([])
    const [showQuarters,setShowQuarters] = useState(true)
    const [show,setShow] = useState(false)
    const {ticker} = useParams();
    const [name,SetName] = useState('')
    const [logo_link,SetLogoLink] = useState('')

    const [timeRange, setTimeRange] = useState(4);//start at 0

    

    useEffect(()=>{
        getComapanieInfo()
        getComapanieChart()
        
    },[])

    function handleTimeRangeChange(newTimeRange){
        setTimeRange(newTimeRange);
    }
    function getComapanieInfo(){
        fetch('/api/get-company-info?ticker='+ticker).then(res=>res.json())
        .then(data=>{
            SetName(data.name)
            SetLogoLink(data.image_link)
            
        })
    }
    function getComapanieChart(){
        fetch('/api/get-first-company-chart?ticker='+ticker).then(res=>res.json())
        .then(data=>{
            
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
            handleTimeRangeChange(4)

            const requestOptions = {
                method: 'PATCH',
                headers :{'Content-Type': 'application/json'},
                body: JSON.stringify({time_periode:timeframe}),
            }
            // console.log(JSON.stringify({time_periode:timeframe}))
            fetch('/api/update-session-time-periode',requestOptions)
            .then(res=>console.log(res))

            

  
    }}
    

    return (<Grid container spacing={1}>
        
        <Grid item xs={12} align="center">
            <Grid item xs={6} align="center" >
                <img src={logo_link}/>
            </Grid>
            <Grid item xs={6} align="center" >
                <Typography component="h5" variant="h5" > {name} Charts</Typography>
            </Grid>
        </Grid>
         <Grid item xs={12} align="center">
            
            <Link  href = {'/info/'+ticker} > more infos</Link>
        </Grid>
        {show ?
        <Grid item xs={12} align="center">
        
        <Grid item xs={12} align="center">
        
            <Button variant={showQuarters? "contained":"outlined"}  color="primary" onClick={e => updateTimeframe(e,'quarter')} style={{ margin: '1rem' }}>Quarter</Button>
            <Button variant={showQuarters? "outlined":"contained"} color="primary" onClick={e =>updateTimeframe(e,'annual')} style={{ margin: '1rem' }}>Annual</Button>
            
        </Grid>
        {showQuarters?
        <ButtonGroup variant="outlined" color="primary">
        <Button
            variant = {timeRange === 4 ? "contained" : ""}
            onClick={() => handleTimeRangeChange(4)}
        >1Y </Button>
        <Button
          variant = {timeRange === 8 ? "contained" : ""}
          onClick={() => handleTimeRangeChange(8)}
        >2Y</Button>
        <Button
          variant = {timeRange === 16 ? "contained" : ""}
          onClick={() => handleTimeRangeChange(16)}
        >4Y</Button>
        <Button
          variant = {timeRange === 1000 ? "contained" : ""}
          onClick={() => handleTimeRangeChange(1000)}
        >MAX</Button>
      </ButtonGroup>:
      <ButtonGroup variant="outlined" color="primary">
      <Button
        variant = {timeRange === 4 ? "contained" : ""}
        onClick={() => handleTimeRangeChange(4)}
      >
        5Y
      </Button>
      <Button
        variant = {timeRange === 9 ? "contained" : ""}
        onClick={() => handleTimeRangeChange(9)}
      >
        10Y
      </Button>
      <Button
        variant = {timeRange === 14 ? "contained" : ""}
        onClick={() => handleTimeRangeChange(14)}
      >
        15Y
      </Button>
      <Button
        variant = {timeRange === 1000 ? "contained" : ""}
        onClick={() => handleTimeRangeChange(1000)}
      > MAX
      </Button>
    </ButtonGroup>
    }
        
        <Grid item xs={8} align="center" style={{ marginTop: '3rem' }}>
            

        { showQuarters?
        <>
        
        <ReactBarChart data={dataQ} timeRange = {timeRange} title = {'Revenue, Gross Profit and Operative Income'}/>
        </>
        : <>
        
        <ReactBarChart data={dataA} timeRange = {timeRange} title = {'Revenue, Gross Profit and Operative Income'}/>
        
        </>
        
        }
        </Grid>
        </Grid>:null}
        <Grid item xs={12} align="center">
            <OtherChart otherChartDataQ = {otherChartDataQ} otherChartDataA={otherChartDataA} showQuarters={showQuarters} timeRange = {timeRange}/>
        </Grid>
    </Grid>)
  
};

  