import React from 'react';
import Company from './Company';


export default function CompaniesList({companies_list}){
    
    return (
        companies_list.map(company =>{
            return <Company key={company.id}  company={company}/>
        })
      )
}