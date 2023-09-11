import Link from "next/link";
import Greetings from "../../components/Greetings";
import { useRouter } from "next/router";
import prisma from "../../lib/prisma";
import styled from "styled-components";
import NavBar from "../../components/NavBar";
import { UNSAFE_LocationContext } from "react-router-dom";


const P_Button = styled.button`
float:left;`;
const N_Button = styled.button`
float:right`;
const LIST = styled.ul`
    height: 100px;
    max-height: 100px;
    overflow-x: hidden;
`;
export async function getServerSideProps(context) {

    const { pages, username } = context.query;
    const problemlist = await prisma.$queryRaw`select code,name,text,difficulty,group_concat(tag separator', ') as tag from tmp group by code order by id limit ${50 * (pages - 1)},50;`;
    const recogProblem = await prisma.$queryRaw`select code from recommend where user=${username} order by id limit 5;`;
    const recogProblem2 = await prisma.$queryRaw`select code from recommend where user=${username} order by id desc limit 5;`;
    return {
        props: {
            problemlist,
            recogProblem,
            recogProblem2,
        }
    };
}
function List({ problemlist, recogProblem, recogProblem2 }) {
    const router = useRouter();
    const { pages, username } = router.query;
    const arr = Array(70).fill().map((v, i) => i + 1);
    return (
        <div className="list-container">
            <div className="list-navbar"><NavBar /></div>
            <div className="list-recog">
                <div>
                    <div className="recog-element">
                    <h1 >Today's Problems</h1>
                    </div>
                    <div className="recog-element">
                        <h1 className="fs-5">Challenging Problems</h1>
                        {recogProblem.map((g) => (
                            <ul >
                                <li scope='row'>{g.code}</li>
                                <Link href={`/problems/${g.code}`}><a>{g.name}</a></Link>

                            </ul>
                        ))}
                    </div>
                    <div className="recog-element">
                        <h1 className="fs-5">Practice Problems</h1>
                        {recogProblem2.map((g) => (
                            <ul >
                                <li scope='row'>{g.code}</li>
                                <Link href={`/problems/${g.code}`}><a>{g.name}</a></Link>

                            </ul>
                        ))}
                    </div>
                </div>

            </div>
            <div className="list-problist">
                <div className="table-responsive">
                    <table className="table table-bordered table-light table-hover table-striped">
                        <thead className="table-dark">
                            <tr>
                                <th scope='col'>CODE</th>
                                <th scope='col'>Title</th>
                                <th scope='col'>Difficulty</th>
                            </tr>
                        </thead>
                        <tbody>
                            {problemlist.map((g) => (
                                <tr >
                                    <td scope='row'>{g.code}</td>
                                    <td><Link href={`/problems/${g.code}`}><a>{g.name}</a></Link></td>
                                    <td>{g.difficulty}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div></div>
            <div className="list-next-prev">
                <div className="container">
                    <div className="row">
                        <div className="col">
                            <Link href={`/list/${String(Number(pages) - 1)}?username=${username}`}><P_Button role="button" type="button" className="btn btn-dark" disabled={pages === '1'} >prev</P_Button></Link>
                        </div>

                        <div className="col text-center">
                            <h4>page <div className="btn-group">
                                <button className="btn btn-secondary btn-sm" type="button" >
                                    {pages}
                                </button>
                                <button type="button" className="btn btn-sm btn-secondary dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-expanded="false">
                                    <span className="visually-hidden">Toggle Dropdown</span>
                                </button>
                                <LIST className="dropdown-menu" role="menu">
                                    {arr.map((g) => (
                                        <li value={g}><a className="dropdown-item" href={`/list/${g}?username=${username}`}>{g}</a></li>
                                    ))}
                                </LIST>
                            </div></h4>
                        </div>
                        <div className="col">
                            <Link href={`/list/${String(Number(pages) + 1)}?username=${username}`}><N_Button role="button" type="button" className="btn btn-dark " disabled={pages === '70'} >next</N_Button></Link>
                        </div>
                    </div>
                </div></div>

        </div>

    );
};

export default List;
