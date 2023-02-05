import React from 'react';
import {render} from 'react-dom';
import HomePage from './HomePage';
import ChartPage from './ChartPage';
import CompanieInfoPage from './CompanieInfoPage';
import {BrowserRouter as Router, Route, Routes, Link, Redirect,} from 'react-router-dom';

export default function App () {
    
        return (<>
        
            
        <Router>
            <Routes>
                <Route exact path="/" element={<HomePage/>}/>
                <Route exact path="/chart" element={<ChartPage/>} />
                <Route  path="/info" element={<CompanieInfoPage/>} />
            </Routes>

        </Router>
        
        </>);
        
    


}

const appDiv = document.getElementById('app');
render(<App />, appDiv);