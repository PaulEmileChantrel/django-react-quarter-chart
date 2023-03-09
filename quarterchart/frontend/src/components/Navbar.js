import React from 'react';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';


function NaviBar (){
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
            </Container>
        </Navbar>)
}

export default NaviBar;


