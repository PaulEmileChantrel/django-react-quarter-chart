import React from 'react';
import EarningsList from './EarningsList';
import { MDBBadge, MDBBtn, MDBTable, MDBTableHead, MDBTableBody } from 'mdb-react-ui-kit';
import  displayWeek from './displayWeek';

export default function EarningsWeek({earningsWeek}){
    
    return (<>
        <MDBTable align='middle' striped bordered>
        <MDBTableHead >
            <tr >
                <th scope='col' >Next Earnings</th>
            </tr>
        </MDBTableHead>
        <MDBTableBody >
        {earningsWeek.map((earningsList, index) =>{
            if (earningsList.length > 0) {
               
            return (<><tr key={index+3000}>
                        <td > {displayWeek(index)}</td>
                    </tr>
                    <tr key={index+10000}>
                        <td ><EarningsList key={index+1000}  earningsList={earningsList} /></td>
                    </tr></>)
        }})}
        </MDBTableBody>
        </MDBTable>
      </>)
}