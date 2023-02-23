import React from 'react';
import EarningsList from './EarningsList';


export default function EarningsWeek({earningsWeek}){
    
    return (
        earningsWeek.map(earningsList =>{
            console.log(earningsList[0].id)
            return <EarningsList key={earningsList[0].id}  earningsList={earningsList} />
        })
      )
}