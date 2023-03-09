import React from 'react'

export default function Earnings({company}) {
    
    return (
        
            <p>
                {company.next_earnings_date} <a  href={'/chart/' + company.ticker}>{company.ticker}</a>
            </p>
        
    )
}
