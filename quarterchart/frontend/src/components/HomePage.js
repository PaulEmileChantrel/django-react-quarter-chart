import React from 'react';
import Button from '@material-ui/core/Button';
import  Grid  from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import TextField  from '@material-ui/core/TextField';  
import FormHelperText from '@material-ui/core/FormHelperText';
import  FormControl from '@material-ui/core/FormControl';
import {Link} from 'react-router-dom';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import {useState,useRef,useEffect} from 'react'


export default function HomePage () {
    const [name,SetName] = useState('')  
    const nameRef = useRef() 
    function searchCompanie(){
    
        SetName(nameRef.current.value)
        console.log(name)

        const requestOptions = {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        };
        fetch('/api/filterCompanie?name='+name, requestOptions).then(response => response.json()).then(data => console.log(data)).catch(error => console.log('error', error));

    }
    useEffect(() => {
        let timerId;
        if (name) {
          clearTimeout(timerId);
          timerId = setTimeout(() => {
            // Call your onChange function here
            searchCompanie()
            console.log(`Debounced value: ${name}`);
          }, 200);
        }
        return () => clearTimeout(timerId);
      }, [name]);

    

  
    return (
        <Grid container spacing={1}>

            <Grid item xs={12} align="center">
                <Typography component="h5" variant="h5" > Companies List</Typography>
            </Grid>
            
            <Grid item xs={12} align="center">
                <FormControl component="fieldset" >
                    <TextField required={true} type="text" inputRef={nameRef}  onChange={(event) => SetName(event.target.value)}/>
                    <FormHelperText >
                        Filter companies by name or ticker
                    </FormHelperText>
                </FormControl>
                <Button onClick={searchCompanie} variant="contained" color="primary">Search</Button>
            </Grid>
            <Grid item xs={12} align="center">
                
            </Grid>
        </Grid>
        
    )

};

  