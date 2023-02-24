import React from 'react';
import EarningsList from './EarningsList';
import { MDBBadge, MDBBtn, MDBTable, MDBTableHead, MDBTableBody } from 'mdb-react-ui-kit';
import  displayWeek from './displayWeek';

export default function EarningsWeek({earningsWeek}){
    
    return (<>
        <MDBTable align='middle' >
        <MDBTableHead >
            <tr>
            <th scope='col'>Next Earnings</th>
            
            
            </tr>
        </MDBTableHead>
        <MDBTableBody >
        {earningsWeek.map((earningsList, index) =>{
            
            return (<tr>
                    <td> {displayWeek(index)} <EarningsList key={earningsList[0].id}  earningsList={earningsList} /></td></tr>)
        })}
        </MDBTableBody>
        </MDBTable>
      </>)
}