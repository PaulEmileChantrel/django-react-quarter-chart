import React from 'react';
import HomePage from './HomePage';
import ChartPage from './ChartPage';
import CompanieInfoPage from './CompanieInfoPage';
import {BrowserRouter as Router, Route, Routes, Link, Redirect,} from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import {Grid} from '@material-ui/core';

function App () {
    
        return (
        <Grid container spacing={1}>
            <Navbar bg="dark" variant="dark">
                <Container>
                <Navbar.Brand href="/">
                    <img
                    alt=""
                    src="images/logo_v1.png"
                    width="30"
                    height="30"
                    className="d-inline-block align-top"
                    />{' '}
                    Quantum Charts
                </Navbar.Brand>
                </Container>
            </Navbar>
            
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