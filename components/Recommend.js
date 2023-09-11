import { useEffect, useState } from "react";
import prisma from "../lib/prisma";
import Link from "next/link";

async function Recommend(){
    const [username,setUsername]=useState('');
    useEffect(()=>{
        setUsername(localStorage.getItem('username'));
    },[]);
    const recogProblem = await prisma.$queryRaw`select code from recommend where user="hk_15" order by id limit 5;`;
    const recogProblem2 = await prisma.$queryRaw`select code from recommend where user="hk_15" order by id desc limit 5;`;
    console.log(recogProblem);
    return <div>test</div>
}
export default Recommend;