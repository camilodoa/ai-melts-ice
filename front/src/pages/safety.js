import React from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup';

export default function Safety() {
  const undocumented_links = [
    ['Prepare emergency plans',
    'https://www.immigrantdefenseproject.org/emergency-preparedness/'],
    ['Know your rights',
    'https://www.immigrantdefenseproject.org/ice-home-and-community-arrests/'],
    ["Learn more about ICE trends",
    'https://www.immigrantdefenseproject.org/wp-content/uploads/ICEwatch-Trends-Report.pdf'],
    ['Find safe community spaces',
    'https://www.nolo.com/legal-encyclopedia/is-there-anywhere-i-m-safe-from-an-ice-arrest.html'],
    ['Protect yourself during an immigration raid',
    'https://www.aclutx.org/en/know-your-rights/how-protect-yourself-during-immigration-raid'],
    ['Stay safe when ICE comes to your door',
    'https://nationalimmigrationproject.org/iceWatch.html']
  ];

  const undocumented_link_group = undocumented_links.map((elem, index) =>
    <ListGroup.Item
      action
      variant="primary"
      key={'undocumented'+index}
      href={elem[1]}
      target="blank">
        <h4 className="float-left">
        {elem[0]}
        </h4>
    </ListGroup.Item>
  );

  const ally_links = [
    ['Find local options for protecting immigrants',
    'https://www.ilrc.org/sites/default/files/resources/local_options-20161215.pdf'],
    ['Help immigrants caught up in ICE raids',
    'https://qz.com/1664310/how-to-help-immigrants-caught-up-in-ice-raids/'],
    ['Tell congress to cut funding for ICE and CBP',
    'https://www.afsc.org/action/cut-funding-ice-and-cbp']

  ]
  const ally_link_group = ally_links.map((elem, index) =>
    <ListGroup.Item
      action
      variant="primary"
      key={'ally'+index}
      href={elem[1]}
      target="blank">
        <h4 className="float-left">
        {elem[0]}
        </h4>
    </ListGroup.Item>
  );


  return (
    <div className="safety">
      <h1 className="safety-header my-3">
        <p>
          safety information
        </p>
      </h1>

      <div className="my-3">
        <h3 className="safety-main my-3 mx-5 pull-left">
          <p>
            if you are undocumented:
          </p>
        </h3>
        <main className="mx-5">
          <ListGroup>
            {undocumented_link_group}
          </ListGroup>
        </main>
      </div>

      <div className="my-3">
        <h3 className="safety-main my-3 mx-5">
          <p>
            if you are are an ally:
          </p>
        </h3>
        <main className="m-3 mx-5">
          <ListGroup>
            {ally_link_group}
          </ListGroup>
        </main>
      </div>

    </div>
  );
}
