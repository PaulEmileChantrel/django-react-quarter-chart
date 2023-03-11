import React from 'react';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import {useParams} from 'react-router-dom';

function NaviBarInfo (){
    const {ticker} = useParams();
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
            <Nav className="me-auto" activeKey={"/chart/"+ticker}>
                <Nav.Link href="/">Home</Nav.Link>
                <Nav.Link href={"/chart/"+ticker}>{ticker} Charts</Nav.Link>
                <Nav.Link href={"/info/"+ticker}>More Infos</Nav.Link>
            </Nav>
            </Container>
        </Navbar>)
}

export default NaviBarInfo;


