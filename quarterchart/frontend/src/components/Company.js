import React from 'react'
import formatMktCp from './formatMktCap';
import { MDBBadge, MDBBtn, MDBTable, MDBTableHead, MDBTableBody } from 'mdb-react-ui-kit';

export default function Company({company}) {
    
    return (
        <tr>
          <td>
            <div className='d-flex align-items-center' href={'/chart/' + company.ticker} >
              <img
                src={'/static/images/company_logo/'+company.ticker.lower()+'.webp'}
                alt=''
                style={{ width: '45px', height: '45px' }}
                className='rounded-circle'
              />
              <div className='ms-3'>
                <p className='fw-bold mb-1'>{company.name}</p>
                <p className='text-muted mb-0'>{company.ticker}</p>
              </div>
            </div>
          </td>
          <td>
            <p className='fw-normal mb-1'>{formatMktCp(company.market_cap)}</p>
            
          </td>
          
        </tr>
        
        
    )
}
