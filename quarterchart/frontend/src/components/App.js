import React from 'react';
import HomePage from './HomePage';
import ChartPage from './ChartPage';
import CompanieInfoPage from './CompanieInfoPage';
import {BrowserRouter as Router, Route, Routes, Link, Redirect,} from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import {Grid} from '@material-ui/core'
import NaviBar from './Navbar';
import NaviBarChart from './NavbarChart';
import NaviBarInfo from './NavbarInfo';
function App () {
    
        return (
        <Grid container spacing={7} >
            <Grid item xs={12} >
                <Router>
                    <Routes>
                        <Route exact path="/" element={<NaviBar/>} />
                        <Route exact path="/chart/:ticker" element={<NaviBarInfo/>} />
                        <Route path="/info/:ticker" element={<NaviBarChart/>} />
                    </Routes>
                </Router>
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