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



export default function HomePage () {
    

  
    return (
        <Grid container spacing={1}>

            <Grid item xs={12} align="center">
                <Typography component="h5" variant="h5" > Companies List</Typography>
            </Grid>
            
            <Grid item xs={12} align="center">
                <FormControl component="fieldset">
                    <TextField required={true} type="text" />
                    <FormHelperText >
                        <div align="center">Filter companies by name</div>
                    </FormHelperText>
                </FormControl>
                <Button variant="contained" color="primary">Search</Button>
            </Grid>
            <Grid item xs={12} align="center">
                
            </Grid>
        </Grid>
        
    )

};

  