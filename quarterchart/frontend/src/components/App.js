import React from 'react';
import {render} from 'react-dom';
import HomePage from './HomePage';
import ChartPage from './ChartPage';
import CompanieInfoPage from './CompanieInfoPage';
import {BrowserRouter as Router, Route, Routes, Link, Redirect,} from 'react-router-dom';

function App () {
    
        return (<>
        
            
        <Router>
            <Routes>
                <Route exact path="/" element={<HomePage/>}/>
                <Route exact path="/chart/:ticker" element={<ChartPage/>} />
                <Route  path="/info/:ticker" element={<CompanieInfoPage/>} />
            </Routes>

        </Router>
        
        </>);
        
    


}

export default App;