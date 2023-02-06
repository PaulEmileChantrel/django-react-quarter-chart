import React from 'react';
import {useState,useRef,useEffect} from 'react'
import {useParams} from 'react-router-dom'
export default function CompanieInfoPage () {
    const [name,SetName] = useState('')
     
    const [summary,SetSummary] = useState('') 
    const [marketCap,SetMarketCap] = useState('')
    const [sector,SetSector] = useState('')
    const [website,SetWebsite] = useState('')
    const [industry,SetIndustry] = useState('')
    const [logo_link,SetLogoLink] = useState('')
    
    
    const {ticker} = useParams();
    
    
    
    return (<>
    <div>
        <img src={logo_link}/>
        <h4>{name}</h4>
        <h4>{ticker}</h4>
    </div>
    <div>
        <p>Sector : {sector} | Industry : {industry} | Market Cap : {marketCap}</p>
        <p>{website}</p>
    </div>
    <div>
        <h6>Company Summary :</h6>
        <p>{summary}</p>    
    </div>    
    </>)
  
};

  