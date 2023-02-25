import React from 'react';
import Earnings from './Earnings';


export default function EarningsList({earningsList}){
    
    return (
        
        earningsList.map(earnings =>{
            console.log(earnings.id);
            return <Earnings key={earnings.id}  company={earnings} />
        })
        
      )
}