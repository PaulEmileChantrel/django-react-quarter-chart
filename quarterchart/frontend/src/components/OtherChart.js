import React from 'react';
import {Grid,Typography,Button,Link}  from '@material-ui/core';

import { ReactBarChart } from './ReactBarChart';
export default function OtherChart({otherChartDataQ,otherChartDataA,showQuarters}){
    const titles = ['Margin (%)','Operating Expense','Assets Vs Liabilities','Liabilities','Cash Flow','Cash Position','Debts','EBITDA','EPS']
    const stackeds = [false,true,false,true,false,false,false,false]
                    
    return (<>
    
        {showQuarters?
            <Grid item xs={8} align="center" >
                {otherChartDataQ.map((data,item) =>{
                    let title = titles[item]
                    let stacked = stackeds[item]
                    
                    if (data.datasets.length){
                        return (<Grid key={item+1000} item xs={12} align="center" style={{ marginTop: '3rem' }}> 
                                <ReactBarChart key={item}  data={data} title = {title} stacked = {stacked} />
                        </Grid>)
                    }
                })}

            </Grid>
            :
            <Grid item xs={8} align="center" style={{ marginTop: '3rem' }}>
                {otherChartDataA.map((data,item) =>{
                    let title = titles[item]
                    let stacked = stackeds[item]
                    if (data.datasets.length){
                        return <ReactBarChart key={item}  data={data} title = {title} stacked = {stacked}/>
                    }
                })}
            </Grid>
            }
        
    </>
    
    )




}