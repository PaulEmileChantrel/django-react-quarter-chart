import React from 'react';
import Earnings from './Earnings';


export default function EarningsList({earningsList}){
    
    return (
        <tr>
          
        <td>
        {earningsList.map(earnings =>{
            
            return <Earnings key={earnings.id}  company={earnings} />
        })}
        </td></tr>
      )
}