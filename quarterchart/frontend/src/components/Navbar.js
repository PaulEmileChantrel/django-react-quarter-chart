import React, { useState,useEffect } from 'react';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import {BrowserRouter as Router, Route, Routes, Link, Redirect,useParams} from 'react-router-dom';

function NaviBar (){
    //const [ticker,setTicker] = useState('')
    let {ticker} = useParams();
    useEffect(()=>{
        
        console.log(ticker)
    },[])
    
    return (<Navbar bg="dark" variant="dark">
            <Container>
            <Navbar.Brand href="/" className="text-white">
                <img
                alt=""
                src="/static/images/logo_v2.png"
                
                height="60"
                className="d-inline-block align-center"
                />{' '}
                
            </Navbar.Brand>
            <Nav className="me-auto" activeKey='/'>
                <Nav.Link href="/">Home</Nav.Link>
                
                
            </Nav>
            </Container>
        </Navbar>)
}

export default NaviBar;


