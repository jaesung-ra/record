import prisma from "../../../../lib/prisma";
import { v4 as uuidv4 } from 'uuid';
export default async function handler(req, res) {

    const {
        method,
        body,
        query: { user },
    } = req;
    const result = await prisma.users.findUnique({
        where: { username: user },
    });
    
    if (method === 'POST') {
        console.log(body);
        
        if (result === null) {
            const create=await prisma.users.create({
                data: {
                    id: uuidv4(),
                    username: user,
                    password: body,
                },
            });
            console.log(create);
            return res.status(200).json(create);
        }
        else{
            return res.status(200).json(null);
        }
    }
    return res.status(200).json({ result, });



}