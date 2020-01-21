import React from "react";
import Header from '../components/header';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export default function Donate() {
  return (
    <div>
      <Header/>

      <Container className='my-5'>
        <Row className="justify-content-md-center">
          <Col>
            <h3 className="my-5 mx-5 text-center">
              <p>
                If you want to help support the site:
              </p>
            </h3>
            <main className="mx-5">
              <embed height="600px" width="100%" src="https://www.gofundme.com/mvc.php?route=widgets/mediawidget&fund=aimeltsice&image=1&preview=1" type="text/html"></embed>
            </main>
          </Col>
        </Row>
      </Container>



    </div>
  );
}
