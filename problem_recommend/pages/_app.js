import 'bootstrap/dist/css/bootstrap.css';
import '../styles/globals.css'
import { useEffect } from 'react';
import dynamic from "next/dynamic";
import React from "react";

const styles = {
    layout: {
        display: 'flex',
        width: '100%',
        height: '100%',
        flexDirection: 'column',
    },
    header: {
        height: 60,
    },
    main: {
        flex: 1,
    },
    footer: {
        height: 60,
    },
}

function MyApp({Component, pageProps}){
    useEffect(()=>{
        import("bootstrap/dist/js/bootstrap");
        
    },[]);
    return(
        
            <Component {...pageProps}/>
        
        
    )
}
export default MyApp;