import React from 'react';
import Company from './Company';
import { MDBBadge, MDBBtn, MDBTable, MDBTableHead, MDBTableBody } from 'mdb-react-ui-kit';


export default function CompaniesList({companies_list}){
    
    return (
        <MDBTable align='middle'>
        <MDBTableHead>
            <tr>
            <th scope='col'>Name</th>
            <th scope='col'>Market Cap.</th>
            
            </tr>
        </MDBTableHead>
        <MDBTableBody>
            {companies_list.map(company =>{
                return <Company key={company.id}  company={company}/>
            })}
        </MDBTableBody>
        </MDBTable>
      )
}