import React from 'react';
import EarningsList from './EarningsList';
import { MDBBadge, MDBBtn, MDBTable, MDBTableHead, MDBTableBody } from 'mdb-react-ui-kit';


export default function EarningsWeek({earningsWeek}){
    
    return (<>
        <MDBTable align='middle' hover>
        <MDBTableHead>
            <tr>
            <th scope='col'>Next Earnings</th>
            
            
            </tr>
        </MDBTableHead>
        <MDBTableBody>
        {earningsWeek.map((earningsList, index) =>{
            
            return (<><p>Week {index}</p><EarningsList key={earningsList[0].id}  earningsList={earningsList} /></>)
        })}
        </MDBTableBody>
        </MDBTable>
      </>)
}