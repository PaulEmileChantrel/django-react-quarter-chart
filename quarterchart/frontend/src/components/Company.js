import React from 'react'
import formatMktCp from './formatMktCap';
export default function Company({company}) {
    
    return (
        <div>
            <a href={'/chart/' + company.ticker}>

                <p>
                    {company.name} ({company.ticker}) | Market Cap: {formatMktCp(company.market_cap)}
                </p>
            </a>
            
            
        </div>
    )
}
