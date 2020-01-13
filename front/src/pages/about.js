import React from "react";
import logo from "../logo.svg";

export default function About() {
  return (
    <div className="about">
      <header className="about-header">
        <img src={logo} className="about-logo" alt="logo" />
        <p>
          <a href="/">ai.melts.ice</a>
        </p>
      </header>

      <main className="about-main">
        <p>
          <a href="/">ai.melts.ice</a> is a web app designed to source and
          visualize predictions of ICE arrests in the US by county. These predictions
          are generated by an LSTM neural network trained on ICE arrest data
          (2014 - 2018) from Syracuse's TRAC web API. Please keep in mind that
          any dates past 2018 are predictions and may not be exact.
        </p>
        <p>
          El pueblo unido jamás será vencido.
        </p>
      </main>
    </div>
  );
}
