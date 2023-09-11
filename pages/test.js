import Head from "next/head";
import { useRouter } from "next/router";
import { useEffect } from "react";
import Link from 'next/link'
import styled from "styled-components";
export default function () {

    return (
        <div className="list-container">
            <div className="list-navbar"></div>
            <div className="list-recog"></div>
            <div className="list-problist"></div>
            <div className="list-next-prev"></div>
            
        </div>

    );
}
