import React from 'react';
import Company from './Company';
import { MDBBadge, MDBBtn, MDBTable, MDBTableHead, MDBTableBody } from 'mdb-react-ui-kit';


export default function CompaniesList({companies_list}){
    
    return (
        <MDBTable align='middle' hover >
        <MDBTableHead >
            <tr>
            
            <th scope='col'>Name</th>
            <th scope='col'>Market Cap.</th>
            <th scope='col'>Share</th>
            <th scope='col'>1D Var.</th>

            
            </tr>
        </MDBTableHead>
        <MDBTableBody className='removeLink'>
            {companies_list.map(company =>{
                return <Company key={company.id}  company={company}/>
            })}
        </MDBTableBody>
        </MDBTable>
      )
}