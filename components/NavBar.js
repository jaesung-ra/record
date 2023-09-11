import Link from "next/link";
import { useRouter } from "next/router";
import Greetings from "./Greetings";
import styled from "styled-components";
import { NodeNextRequest } from "next/dist/server/base-http/node";

function NavBar() {
    async function onSubmit(event){
        event.preventDefault();
        console.log(event.target.childNodes[0].value);
        const probName=event.target.childNodes[0].value;
        event.target.childNodes[0].value = "";
        const res = await (await fetch(`/api/problems/${probName}`)).json();
        res==='none'?alert("problem does not exist"):router.push(`/problems/${res}`);;
    }
    const router = useRouter();
    return (
        <nav className="navbar navbar-light navbar-expand-lg navbar-bg">
            <div className="container-fluid">

                <div>
                    <a className="navbar-brand" href="#"><Greetings /></a>
                    <button onClick={() => {
                        localStorage.removeItem("username");
                        router.replace("/")
                    }} role="button" type="button" className="btn btn-light btn-xs text-center fs-6">Sign off</button>
                </div>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        <li className="nav-item">
                            <a className="nav-link active" aria-current="page" href="/list/1">Home</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link active" aria-current="page" href="/list/1">Profile</a>
                        </li>
                    </ul>

                    <form className="d-flex" role="search" onSubmit={onSubmit}>
                        <input className="form-control me-2" type="search" placeholder="Search" aria-label="Search"></input>
                        <button className="btn btn-success" type="submit" >Search</button>
                    </form>

                </div>

            </div>
        </nav>
    )
}

export default NavBar;