import React from 'react';
import {useState,useRef,useEffect} from 'react'
import {useParams} from 'react-router-dom'
import formatMktCp from './formatMktCap';
import { MDBBadge, MDBBtn, MDBTable, MDBTableHead, MDBTableBody } from 'mdb-react-ui-kit';
import {Grid,Typography,Button,Link}  from '@material-ui/core';

export default function CompanieInfoPage () {
    const [name,SetName] = useState('')
     
    const [summary,SetSummary] = useState('') 
    const [marketCap,SetMarketCap] = useState('')
    const [sector,SetSector] = useState('')
    const [website,SetWebsite] = useState('')
    const [industry,SetIndustry] = useState('')
    const [logo_link,SetLogoLink] = useState('')
    const [next_earnings,SetNextEarnings] = useState('')
    
    
    const {ticker} = useParams();
    useEffect(() => {
        
        getComapanieInfo()
    },[]);
    
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
            SetNextEarnings(data.next_earnings_date)
            
        })
    
            


    }

    
    return (<Grid item xs={12} align="center">
    <Grid item xs={12} align="center">
        <img src={logo_link}/>
        <h4>{name} ({ticker})</h4>
        <Link  href = {'/chart/'+ticker} > back to chart</Link>
        
    </ Grid>
    <Grid item xs={8} align="center" style={{ marginTop: '3rem' }}>
        <MDBTable align='middle' bordered>
            <MDBTableHead light>
                <tr >
                    <th scope='col' >Sector</th>
                    <th scope='col' >Industry</th>
                    <th scope='col' >Market Cap.</th>
                    <th scope='col' >Next Earnings</th>
                    <th scope='col' >website</th>
                </tr>
            </MDBTableHead>
            <MDBTableBody >
                <tr>


                    <td>{sector}</td>
                    <td>{industry}</td>
                    <td>{marketCap}</td>
                    <td>{next_earnings}</td>
                    <td><a href={website}>{website}</a></td>

                </tr>
           
            </MDBTableBody>
        </MDBTable>
    </ Grid>
    <Grid item xs={8} align="center" style={{ marginTop: '3rem' }}>
        <h6>Company Summary :</h6>
        <p>{summary}</p>    
        </ Grid>    
    </ Grid>)
  
};

  