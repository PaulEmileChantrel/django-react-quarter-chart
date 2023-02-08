import React from 'react';
import {useParams} from 'react-router-dom'
import {Grid,Typography}  from '@material-ui/core';
import {useState,useRef,useEffect} from 'react'


export default function ChartPage () {
    
    
    const {ticker} = useParams();


    return (<Grid container spacing={1}>
        <Grid item xs={12} align="center">
                <Typography component="h5" variant="h5" > {ticker} Charts</Typography>
            </Grid>

    </Grid>)
  
};

  