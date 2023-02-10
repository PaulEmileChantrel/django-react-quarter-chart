import React from 'react';
import {Grid,Typography,Button,Link}  from '@material-ui/core';
import Charts from './Charts';
import {useEffect,useState} from 'react'

export default function OtherChart({otherChartDataQ,otherChartDataA,showQuarters}){
    const [show,setShow] = useState(false);
    
    useEffect(() => {
        let ChartDataQ=[];
        let ChartDataA = [];
        otherChartDataQ.forEach((item,index)=>{
            console.log(item)
            ChartDataQ.push( <Charts key={index} data ={item}/>)
                })


        otherChartDataA.forEach((item,index)=>{
            ChartDataA.push( <Charts key={index} data ={item}/>)
                })
        setShow(true);
    },[])

    return (<>
    
        {showQuarters?
            <Grid item xs={12} align="center">
                {otherChartDataQ.map((data,id) =>{
                    return <Charts key={id}  data={data}/>
                })}

            </Grid>
            :
            <Grid item xs={12} align="center">
                {otherChartDataA.map((data,id) =>{
                    return <Charts key={id}  data={data}/>
                })}
            </Grid>
            }
        
    </>
    
    )




}