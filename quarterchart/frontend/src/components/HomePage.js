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
import EarningsList from './EarningsList';

export default function HomePage () {
    const [name,SetName] = useState('') 
    const [companiesList,SetCompaniesList] = useState([])
    const [earningsList,setEarningsList] = useState([])
    const nameRef = useRef() 
    
    

    function loadCompanyList() {
        fetch('/api').then(response => response.json())
        .then(data => SetCompaniesList(data))
        .catch(error => console.log(error))
    }
    function loadCompanyEarningsList() {
        fetch('/api/next-earnings').then(response => response.json())
        .then(data => {console.log(data),
                setEarningsList(data)})
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
        <Grid item xs={9} align="center">
            <Grid item xs={2} align="center"></Grid>
            <Grid item xs={8} align="center">
                <Typography component="h5" variant="h5" > Companies List</Typography>
            </Grid>
            
            <Grid item xs={8} align="center">
                <FormControl component="fieldset" >
                    <TextField required={true} type="text" inputRef={nameRef}  onChange={(event) => SetName(event.target.value)}/>
                    <FormHelperText >
                        Filter companies by name or ticker
                    </FormHelperText>
                </FormControl>
                
            </Grid>
            <Grid item xs={8} align="center">
                {companiesList? <CompaniesList companies_list={companiesList}/>:null}
            </Grid>
            <Grid item xs={2} align="center"></Grid>
        </Grid>
            
        <Grid item xs={3} align="center">
            <Grid item xs={12} align="center">
                <Typography component="h6" variant="h6" > Next Earnings </Typography>
                {earningsList? <EarningsList earningsList={earningsList}/>:null}
            </Grid>
        </Grid>
       </>
        
    )

};

  