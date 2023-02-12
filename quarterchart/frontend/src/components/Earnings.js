import React from 'react'

export default function Earnings({company}) {
    
    return (
        <div>
            <a href={'/chart/' + company.ticker}>

                <p>
                    {company.ticker} | Date : {company.next_earnings_date}
                </p>
            </a>
            
            
        </div>
    )
}
