import Head from "next/head";
import { useRouter } from "next/router";
import { useEffect } from "react";
import Link from 'next/link'
import styled from "styled-components";
import Image from 'next/image';
const S_SigninForm = styled.form`
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
  height:100%;
`;
const DIV = styled.div`
display: grid;
min-height: 100vh;
position: relative;
place-items: center;
`;




function Home() {



  return (

    <DIV>
      <nav className="navbar navbar-light navbar-expand-lg mainpage-navbar ">
        <div className="container-fluid">
          <h5 className="title-homepage">Practice Recommender</h5>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
            <ul className="navbar-nav">
              <li className="nav-item">
                <Link href="/signin"><button role="button" type="button" className="btn btn-light btn-xs text-center fs-6 signin-btn">Sign in</button></Link>
              </li>
              <li className="nav-item">
                <Link href="/signup"><button role="button" type="button" className="btn btn-light btn-xs text-center fs-6 signup-btn">Sign up</button></Link>

              </li>
            </ul>
          </div>
        </div>
      </nav>
      <div className="div-container">

        <div className="img">
          <div className="quote">
            <div className="big">
              <p>Easy,</p>
              <p>Effective,</p>
              <p>Efficient.</p>
            </div>
            <div className="small">
              <p>Practice recommendation is designed to help students learn programming in Easy, Effective, and Efficient way</p>
            </div>
          </div>
          <div className="img-div1"><Image src='/img1.png' width='300' height='300'></Image></div>
        </div>

        <div className="img bgc-beige">
        <div className="img-div1"><Image src='/img2.png' width='300' height='300'></Image></div>
          <div className="quote">
            <div className="big">
              <p>Get</p>
              <p>Personalized</p>
              <p>Recommendations</p>
            </div>
            <div className="small">
              <p>Recommendations specifically chosen  for YOU</p>
            </div>
          </div>
        </div>
        
        <div className="img">
          <div className="quote">
            <div className="big last">
              <p>Similar, Easier</p>
              <p>Opposite, Harder</p>
              <p>Problems at once.</p>
            </div>
            <div className="small">
              <p>Find other problems based on tags, and difficulties</p>
            </div>
          </div>
          <div className="img-div1"><Image src='/img3.png' width='300' height='300'></Image></div>
        </div>

        
      </div>
      <p className="mt-5 mb-3 text-muted">&copy; 2017-2020</p>
    </DIV>
  );
}

export default Home;

