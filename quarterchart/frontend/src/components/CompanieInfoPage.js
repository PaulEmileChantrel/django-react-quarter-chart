import React from 'react';
import {useState,useRef,useEffect} from 'react'
import {useParams} from 'react-router-dom'
import  Grid  from '@material-ui/core/Grid';
import formatMktCp from './formatMktCap';
export default function CompanieInfoPage () {
    const [name,SetName] = useState('')
     
    const [summary,SetSummary] = useState('') 
    const [marketCap,SetMarketCap] = useState('')
    const [sector,SetSector] = useState('')
    const [website,SetWebsite] = useState('')
    const [industry,SetIndustry] = useState('')
    const [logo_link,SetLogoLink] = useState('')
    
    
    const {ticker} = useParams();
    getComapanieInfo()
    function getComapanieInfo(){
        fetch('/api/get-company-info?ticker='+ticker).then(res=>res.json())
        .then(data=>{
            SetName(data.name)
            SetSummary(data.summary)
            SetMarketCap(formatMktCp(data.market_cap))
            SetIndustry(data.industry)
            SetSector(data.sector)
            SetWebsite(data.website)
            SetLogoLink(data.image_link)
            
        })
    
            


    }
    

    
    return (<Grid container spacing={1}>
    <Grid item xs={12} align="center">
        <img src={logo_link}/>
        <h4>{name}</h4>
        <h4>{ticker}</h4>
    </ Grid>
    <Grid item xs={12} align="center">
        <p>Sector : {sector} | Industry : {industry} | Market Cap : {marketCap}</p>
        <p><a href ={website}>{website}</a></p>
    </ Grid>
    <Grid item xs={12} align="center">
        <h6>Company Summary :</h6>
        <p>{summary}</p>    
        </ Grid>    
    </ Grid>)
  
};

  