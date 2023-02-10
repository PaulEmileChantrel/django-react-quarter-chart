import React from 'react';
import HomePage from './HomePage';
import ChartPage from './ChartPage';
import CompanieInfoPage from './CompanieInfoPage';
import {BrowserRouter as Router, Route, Routes, Link, Redirect,} from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import {Grid} from '@material-ui/core'
import NaviBar from './Navbar';
function App () {
    
        return (
        <Grid container spacing={1}>
            <Grid item xs={12} >
                <NaviBar/>
            </Grid>
        <Router>
            <Routes>
                <Route exact path="/" element={<HomePage/>}/>
                <Route exact path="/chart/:ticker" element={<ChartPage/>} />
                <Route  path="/info/:ticker" element={<CompanieInfoPage/>} />
            </Routes>

        </Router>
        
        </Grid>);
        
    


}

export default App;