import { useEffect, useState } from "react";

function Greetings(){
    const [username,setUsername]=useState('');
    useEffect(()=>{
        setUsername(localStorage.getItem('username'));
    },[]);
    return <div>
            <h1 className="fs-3">welcome <button className="btn btn-success">{username}</button></h1>
        </div>
}
export default Greetings;