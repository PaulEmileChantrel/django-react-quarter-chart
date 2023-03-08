import React from 'react';
import {Grid,Typography,Button,Link}  from '@material-ui/core';

import {useEffect,useState} from 'react'
import { ReactBarChart } from './ReactBarChart';
export default function OtherChart({otherChartDataQ,otherChartDataA,showQuarters}){
    const titles = ['Net Income','OpEx','Assets','Liabilities','Debts','Cash Flow','Cash','EBITDA','EPS']
    const stackeds = [false,false,false,true,false,false,false,false]
                    
    return (<>
    
        {showQuarters?
            <Grid item xs={8} align="center" style={{ marginTop: '3rem' }}>
                {otherChartDataQ.map((data,item) =>{
                    let title = titles[item]
                    let stacked = stackeds[item]
                    
                    return <ReactBarChart key={item}  data={data} title = {title} stacked = {stacked}/>
                })}

            </Grid>
            :
            <Grid item xs={8} align="center" style={{ marginTop: '3rem' }}>
                {otherChartDataA.map((data,item) =>{
                    let title = titles[item]
                    let stacked = stackeds[item]
                    
                    return <ReactBarChart key={item}  data={data} title = {title} stacked = {stacked}/>
                })}
            </Grid>
            }
        
    </>
    
    )




}