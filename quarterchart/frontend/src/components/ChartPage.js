import React from 'react';
import {useParams} from 'react-router-dom'
import {Grid,Typography,Button,Link,Item}  from '@material-ui/core';
import {useState,useRef,useEffect} from 'react'
import { Chart } from "react-google-charts";
import { MDBBadge, MDBBtn, MDBTable, MDBTableHead, MDBTableBody } from 'mdb-react-ui-kit';
import { ReactBarStackChart } from './ReactBarStackChart';
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

    

    useEffect(()=>{
        getComapanieInfo()
        getComapanieChart()
        
    },[])
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
        
        <Grid item xs={8} align="center" style={{ marginTop: '3rem' }}>
            

        { showQuarters?
        <>
        
        <ReactBarChart dataQ={dataQ} title = {'Revenue, Gross Profit and Operative Income'}/>
        </>
        : <>
        
        <ReactBarChart dataQ={dataA} title = {'Revenue, Gross Profit and Operative Income'}/>
        
        </>
        
        }
        </Grid>
        </Grid>:null}
        <OtherChart otherChartDataQ = {otherChartDataQ} otherChartDataA={otherChartDataA} showQuarters={showQuarters}/>

    </Grid>)
  
};

  