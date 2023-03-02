import React from 'react';
import Button from '@material-ui/core/Button';
import Grid  from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import TextField  from '@material-ui/core/TextField';  
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import {Link} from 'react-router-dom';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import {useState,useRef,useEffect} from 'react'
import CompaniesList from './CompaniesList';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import EarningsWeek from './EarningsWeek';

export default function HomePage () {
    const [name,SetName] = useState('') 
    const [companiesList,SetCompaniesList] = useState([])
    const [earningsWeek,setEarningsWeeks] = useState([])
    const nameRef = useRef() 
    
    
    function order_by_weeks(data) {
        // console.log(data)
        Date.prototype.getWeek = function() {
            const onejan = new Date(this.getFullYear(), 0, 1);
            const week = Math.ceil((((this - onejan) / 86400000) + onejan.getDay() + 1) / 7);
            return week - 1;
        };
        
        const today = new Date();
        let first_week = today.getWeek();
        let week = []
        let weeks = []
        let date,date_str,item;
    
        let i = 0;
        while ( i < data.length) {
            date = new Date(data[i].next_earnings_date);
            date_str = date.toLocaleDateString('en-US', { month: 'numeric', day: 'numeric' });
            item = {id:data[i].id,next_earnings_date:date_str,ticker:data[i].ticker}
            if (date.getWeek() == first_week) {
                week.push(item)
                i++;
            }
            
            else {
                weeks.push(week)
                week = []
                first_week ++;
            }
            
        
        }
        
        return weeks
        
          
          
          
    }
    function loadCompanyList() {
        fetch('/api').then(response => response.json())
        .then(data => SetCompaniesList(data))
        .catch(error => console.log(error))
    }
    function loadCompanyEarningsList() {
        fetch('/api/next-earnings').then(response => response.json())
        .then(data =>order_by_weeks(data))
        .then(data => setEarningsWeeks(data))
        .catch(error => console.log(error))
    }
    function searchCompanie(){
    
        SetName(nameRef.current.value)
        

        const requestOptions = {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        };
        fetch('/api/filterCompany?name='+name, requestOptions).then(response => response.json()).then(data => SetCompaniesList(data)).catch(error => console.log('erroR', error));

    }
    useEffect(() => {
        
        loadCompanyEarningsList()
    },[]);
    useEffect(() => {
        let timerId;
        loadCompanyList()
        
        if (name) {
          clearTimeout(timerId);
          timerId = setTimeout(() => {
            // Call your onChange function here
            searchCompanie()
            //console.log(`Debounced value: ${name}`);
          }, 300);
        }
        return () => clearTimeout(timerId);
      }, [name]);

    
    
  
    return (
        <>
        <Grid item xs={9} md={9} align="center"  >
            
            <Grid item xs={10} align="center">
                <Typography component="h5" variant="h5" > Companies List</Typography>
            </Grid>
            
            <Grid item xs={10} align="center" >
                <FormControl component="fieldset" >
                    <TextField required={true} type="text" inputRef={nameRef}  onChange={(event) => SetName(event.target.value)}/>
                    <FormHelperText >
                        Filter companies by name or ticker
                    </FormHelperText>
                </FormControl>
                
            </Grid>
            
            <Grid item xs={10} align="center"  style={{ marginTop: '3rem' }}>
                {companiesList? <CompaniesList companies_list={companiesList}/>:null}
            </Grid>
            
        </Grid>
            
        <Grid item xs={3} md={3} align="center" >
            <Grid item xs={10} align="center">
                
                {earningsWeek? <EarningsWeek earningsWeek={earningsWeek}/>:null}
            </Grid>
        </Grid>
       </>
        
    )

};

  