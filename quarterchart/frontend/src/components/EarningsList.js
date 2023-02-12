import React from 'react';
import Earnings from './Earnings';


export default function EarningsList({earningsList}){
    
    return (
        earningsList.map(earnings =>{
            return <Earnings key={earnings.id}  company={earnings} />
        })
      )
}