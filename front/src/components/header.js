import React from 'react';
import {useState, useEffect} from 'react';
import {withRouter} from 'react-router'
import DatePicker from 'react-datepicker';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import {FaSistrix} from 'react-icons/fa';
import logo from '../images/logo512.png';


function Header({
                    mindate, maxdate, fetchdatedata, settoday, location,
                    counties, fetchcountydata, sethere
                }) {

    const [expanded, setExpanded] = useState(false);

    return (
        <Navbar bg='light' expand='lg' sticky='top' onToggle={setExpanded} expanded={expanded}>
            <Navbar.Brand href='/'>
                <img src={logo} className="d-inline-block align-top" height="30" width="30" alt="logo"/>
                {' '}
                AI Melts ICE
            </Navbar.Brand>
            <Nav className='ml-sm-auto ml-xs-0 my-2'>
                {location.pathname === '/' ?
                    <DateForm
                        maxdate={maxdate}
                        mindate={mindate}
                        fetchdatedata={fetchdatedata}
                        settoday={settoday}
                        setexpanded={setExpanded}/>
                    :
                    null}

                {location.pathname === '/county' ?
                    <CountyForm
                        counties={counties}
                        fetchcountydata={fetchcountydata}
                        sethere={sethere}
                        setexpanded={setExpanded}/>
                    :
                    null}
            </Nav>
            <Nav className='ml-sm-auto ml-xs-0'>
                <Nav.Link href='/about'>
                    About
                </Nav.Link>
            </Nav>
        </Navbar>
    );
}

function DateForm({mindate, maxdate, fetchdatedata, settoday, setexpanded}) {

    const [date, setdate] = useState(new Date());

    return (
        <div>

            <DatePicker
                selected={date}
                onChange={date => {
                    setdate(date);
                    fetchdatedata(date);
                    settoday(date);
                }}
                dateFormat='MMMM yyyy'
                minDate={mindate}
                maxDate={maxdate}
                placeholderText='Select a month'
                showMonthYearPicker/>

            <FaSistrix className={'mx-2'} size={'1em'}/>

        </div>
    );
}

function CountyForm({counties, fetchcountydata, sethere, setexpanded}) {

    const [county, setcounty] = useState(counties.counties[0]);

    return (
        <div>
            <Form
                inline
                onSubmit={(e) => {
                    e.preventDefault();
                    fetchcountydata(county);
                    sethere(county);
                }}>
                <Form.Row>
                    <Col xs>
                        <Form.Control
                            className="mr-sm-2"
                            as="select"
                            value={county}
                            onChange={(e) => setcounty(e.target.value)}>
                            {
                                counties.counties.map((county, index) =>
                                    <option key={'county' + index}>{county}</option>
                                )
                            }
                        </Form.Control>
                    </Col>
                    <Col>
                        <LoadingButton
                            variable={county}
                            fetch={fetchcountydata}
                            setvariable={sethere}
                            setexpanded={setexpanded}/>
                    </Col>
                </Form.Row>
            </Form>
        </div>
    );
}

function LoadingButton({fetch, variable, setvariable, setexpanded}) {

    const [isLoading, setLoading] = useState(false);

    useEffect(() => {
        if (isLoading) {
            fetch(variable).then(r => {
                setLoading(false);
            });
            setvariable(variable);
            setexpanded(false);
        }
    }, [isLoading, variable]);

    const handleClick = () => setLoading(true);

    return (
        <Button
            variant='outline-primary'
            className='mr-1 mx-0 non-resizing'
            type='submit'
            disabled={isLoading}
            onClick={!isLoading ? handleClick : null}
        >
            {isLoading ?
                <Spinner as='span' role='status' animation='border' variant='primary' size='sm'/>
                :
                <FaSistrix/>}
        </Button>
    );
}

export default withRouter(Header);
