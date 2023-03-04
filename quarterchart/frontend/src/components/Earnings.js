import React from 'react'

export default function Earnings({company}) {
    
    return (
        <div>
            

                <p>
                {company.next_earnings_date} <a  href={'/chart/' + company.ticker}>{company.ticker}</a>
                </p>
            
            
            
        </div>
    )
}
