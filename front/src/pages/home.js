import React from "react";
import logo from "../logo.svg";
import "./home.css";

export default function Home() {
  return (
    <header className="body">
      <img src={logo} className="logo" alt="logo"/>
      <p>
        ai.melts.ice
      </p>
    </header>
  );
}
