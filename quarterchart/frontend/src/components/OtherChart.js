import React from 'react';
import {Grid,Typography,Button,Link}  from '@material-ui/core';
import Charts from './Charts';
import {useEffect,useState} from 'react'

export default function OtherChart({otherChartDataQ,otherChartDataA,showQuarters}){
    const [show,setShow] = useState(false);
    const titles = ['Net Income','OpEx','Assets','Liabilities','Debts','Cash Flow','Cash','EBITDA','EPS']
    useEffect(() => {
        let ChartDataQ=[];
        let ChartDataA = [];
        otherChartDataQ.forEach((item,index)=>{
            
            
            ChartDataQ.push( <Charts key={index} data ={item} title = {title}/>)
                })


        otherChartDataA.forEach((item,index)=>{
            let title = titles[index]
            ChartDataA.push( <Charts key={index} data ={item} title = {title}/>)
                })
        setShow(true);
    },[])

    return (<>
    
        {showQuarters?
            <Grid item xs={12} align="center" style={{ marginTop: '3rem' }}>
                {otherChartDataQ.map((data,id) =>{
                    let title = titles[id]
                    return <Charts key={id}  data={data} title = {title}/>
                })}

            </Grid>
            :
            <Grid item xs={12} align="center" style={{ marginTop: '3rem' }}>
                {otherChartDataA.map((data,id) =>{
                    let title = titles[id]
                    return <Charts key={id}  data={data} title = {title}/>
                })}
            </Grid>
            }
        
    </>
    
    )




}