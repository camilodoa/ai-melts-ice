import React from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup';

export default function Safety() {
  return (
    <div className="safety">
      <header className="safety-header my-3">
        <p>
          safety information
        </p>
      </header>

      <main className="safety-main m-3 mx-5">
        <ListGroup variant='flush'>
          <ListGroup.Item action variant="primary" href="https://www.aclutx.org/en/know-your-rights/how-protect-yourself-during-immigration-raid">
            ACLU - How To Protect Yourself During an Immigration Raid
          </ListGroup.Item>
        </ListGroup>
      </main>

    </div>
  );
}
