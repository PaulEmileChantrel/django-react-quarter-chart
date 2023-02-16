import React from 'react'
import formatMktCp from './formatMktCap';
import { MDBBadge, MDBBtn, MDBTable, MDBTableHead, MDBTableBody } from 'mdb-react-ui-kit';

export default function Company({company}) {
    
    return (
        <tr>
          <td>
            <a href={'/chart/' + company.ticker}>
            <div className='d-flex align-items-center'  >
              <img
                src={'/static/images/company_logo/'+company.ticker.toLowerCase()+'.webp'}
                alt=''
                style={{ width: '45px', height: '45px' }}
                
              />
              <div className='ms-3'>
                <p className='fw-bold mb-1'>{company.name}</p>
                <p className='text-muted mb-0'>{company.ticker}</p>
              </div>
            </div>
            </a>
          </td>
          <td>
            <p className='fw-normal mb-1'>$ {formatMktCp(company.market_cap)}</p>
            
          </td>
          <td>
            <p className='fw-normal mb-1'>$ {Math.round(company.share_price*100)/100}</p>
            
          </td>
          
        </tr>
        
        
    )
}
