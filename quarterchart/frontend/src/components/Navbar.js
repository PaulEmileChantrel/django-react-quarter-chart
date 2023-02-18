import React from 'react';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';


function NaviBar (){
    return (<Navbar bg="dark" variant="dark">
            <Container>
            <Navbar.Brand href="/" className="text-white">
                <img
                alt=""
                src="/static/images/logo_v1.png"
                width="50"
                height="50"
                className="d-inline-block align-center"
                />{' '}
                Quarter Charts
            </Navbar.Brand>
            </Container>
        </Navbar>)
}

export default NaviBar;


