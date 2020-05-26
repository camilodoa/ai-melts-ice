import React from "react";
import logo from '../logo512.png';
import Header from './components/header';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export default function About() {
  return (
    <div>
      <Header/>
      <div className="about">
        <h1 className="header my-3 mt-5">
          <a href="/"><img src={logo} className="about-logo" alt="logo" /></a>
          <p className="header my-3">
            AI Melts ICE
          </p>
          <p className="about-main">El pueblo unido jamás será vencido.</p>
        </h1>
        <main className="about-main">
          <Container>
            <Row>
              <Col sm>
                <p>
                  <a href="/">AI Melts ICE</a> is a web app designed to source and
                  visualize predictions of ICE raids in the US by county. These predictions
                  are generated by an LSTM neural network trained on data
                  (2014 - 2018) from Syracuse's <a href={'https://trac.syr.edu/phptools/immigration/arrest/about_data.html'}>TRAC web API</a>.
                  Please keep in mind that  any data shown past 2018 are predictions and may not be exact.
                </p>
              </Col>
              <Col sm>
                <p>
                  <a href="/">AI Melts ICE</a> es una aplicación web diseñada
                  para producir y visualizar predicciones de redadas de
                  inmigrantes en los Estados Unidos por condado. Estas predicciones
                  son generadas por una red neural LSTM basada en datos
                  (2014 – 2018) del <a href={'https://trac.syr.edu/phptools/immigration/arrest/about_data.html'}>web API TRAC</a> de
                  Syracuse. Téngase en cuenta que los datos después de 2018 son predicciones y pueden ser
                  inexactos.
                </p>
              </Col>
            </Row>
          </Container>
        </main>
      </div>
    </div>
  );
}
