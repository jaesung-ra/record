import Link from "next/link";
import Greetings from "../../components/Greetings";
import { useRouter } from "next/router";
import NavBar from "../../components/NavBar";
import styled from "styled-components";
import prisma from "../../lib/prisma";
import { useState } from "react";

const DIV = styled.div`
padding:30px;
left:30px;
`;

const DIV2 = styled.div`
padding:0px 30px;
left:30px;`;

export async function getServerSideProps(context) {


    const { code } = context.query;
    const problem = await prisma.$queryRaw`select code,name,text,level,difficulty,group_concat(tag separator', ') as tag from tmp where code =${code} group by code;`;
    const tag_sim = await prisma.$queryRaw`select * from tag_sim where pcode=${code} and similar = "yes";`;
    const op_tag = await prisma.$queryRaw`select * from tag_sim where pcode=${code} and similar = "no" order by rand() limit 5;`;
    const level = problem[0].level;
    const sim_diff_problem_recog = await prisma.$queryRaw`select code,name,group_concat(tag separator', ') as tag from tmp where level =${level} group by code order by rand() limit 3;`;
    const low_diff_problem_recog = await prisma.$queryRaw`select code,name,group_concat(tag separator', ') as tag from tmp where level =${level - 1} group by code order by rand() limit 3;`;
    const high_diff_problem_recog = await prisma.$queryRaw`select code,name,group_concat(tag separator', ') as tag from tmp where level =${level + 1} group by code order by rand() limit 3;`;
    return {
        props: {
            problem,
            tag_sim,
            op_tag,
            sim_diff_problem_recog,
            low_diff_problem_recog,
            high_diff_problem_recog,
        }
    };
}
function List({ problem, tag_sim, op_tag, sim_diff_problem_recog, low_diff_problem_recog, high_diff_problem_recog }) {
    const router = useRouter();
    const tags = problem[0].tag.split(", ");
    const { code } = router.query;
    const [isActive, setIsActive] = useState(false);
    const [isCorrect, setisCorrect] = useState(false);
    const [isIncorrect, setisIncorrect] = useState(false);
    
    async function onClick(event) {
        event.preventDefault();
        console.log(event.target.className);
        setIsActive(current => true);
        //Correct button clicked
        if (event.target.className == "btn btn-success btn-space") {
            setisCorrect(current => true);
            setisIncorrect(current => false);
        }
        //Incorrect button clicked
        else {
            setisIncorrect(current => true);
            setisCorrect(current => false);
        }
    }

    return (
        <div className="code-container">
            <div className="code-navbar"><NavBar /></div>

            <div className="code-title">
                <h1 className="fs-4">{problem[0].name}</h1>
                <p>Problem Code: {problem[0].code}</p>
                <p>Difficulty Rating: {problem[0].difficulty}</p>
                <p>Tags: {tags.map((tag) => (
                    <button className="btn btn-sm btn-outline-success col-xs-2 mr-5 btn-space disabled">{tag}   </button>

                ))}</p>
            </div>

            <div className="code-problem">
                <h1>Problem</h1>
                <p >
                    {problem[0].text}
                </p>
                
            </div>

            <div className="code-editor">
                <form>
                <textarea name='submit' placeholder="Write your code here" rows="34" ></textarea>
                
                </form>
            </div>

            <div className="code-button">
                <div className="text-center">
                    <button className="btn btn-success btn-space" onClick={onClick}>Correct</button>
                    <button className="btn btn-danger" onClick={onClick}>Incorrect</button>
                </div>
            </div>
            <div className="code-recog">
                <div className="opposite">
                    <div className={isActive ? "col " : "col d-none"}>
                        <h5>Opposite Problems</h5>
                        <ul>
                            {op_tag.map((g) => (
                                <li > <Link href={`/problems/${g.ccode}`}><a>{g.ccode}</a></Link> </li>
                            ))}
                        </ul>
                    </div>
                </div>
                <div className="similar">
                    <div className={isActive ? "col " : "col d-none"}>
                        <h5>Similar Problems</h5>
                        <ul>
                            {tag_sim.map((g) => (
                                <li > <Link href={`/problems/${g.ccode}`}><a>{g.ccode}</a></Link> </li>
                            ))}
                        </ul>
                    </div>
                </div>
                <div className="same-level">
                    <div className={isActive ? "col " : "col d-none"}>
                        <h5>Similar Difficulty Problems</h5>
                        <ul>
                            {sim_diff_problem_recog.map((g) => (
                                <li > <Link href={`/problems/${g.code}`}><a>{g.code}</a></Link> </li>
                            ))}
                        </ul>
                    </div>
                </div>
                <div className="chal-easy-level">
                    <div className={isCorrect ? "col " : "col d-none"}>
                        <h5>Challenging Problems</h5>
                        <ul>
                            {high_diff_problem_recog.map((g) => (
                                <li > <Link href={`/problems/${g.code}`}><a>{g.code}</a></Link> </li>
                            ))}
                        </ul>
                    </div>
                    <div className={isIncorrect ? "col " : "col d-none"}>
                        <h5>Easier Problems</h5>
                        <ul>
                            {low_diff_problem_recog.map((g) => (
                                <li><Link href={`/problems/${g.code}`}><a>{g.code}</a></Link> </li>

                            ))}
                        </ul>

                    </div>
                </div>
            </div>
        </div>
    );

    /*
    return (
        <div>
            <NavBar />
            <DIV className="text-center">
                <h1 className="fs-4">{problem[0].name}</h1>
                <p>Problem Code: {problem[0].code}</p>
                <p>Difficulty Rating: {problem[0].difficulty}</p>
                <p>Tags: {tags.map((tag) => (
                    <button className="btn btn-sm btn-outline-success col-xs-2 mr-5 btn-space disabled">{tag}   </button>

                ))}</p>
            </DIV>
            <div className="container">
                <div className="row text-left">
                    <DIV2 className="col">
                        <h1 className="fs-6">Problem</h1>
                        <p >
                            {problem[0].text}
                        </p>
                    </DIV2>
                    <div className="col">
                        <h1 className="fs-6">Submit</h1>
                        <form>
                            <textarea name='submit' placeholder="Write your code here" rows="20" cols="80"></textarea>
                            <div className="text-center">
                                <button className="btn btn-success btn-space" onClick={onClick}>Correct</button>
                                <button className="btn btn-danger" onClick={onClick}>Incorrect</button>
                            </div>
                        </form>
                    </div>
                    <DIV2 >
                        <div><h1 className="fs-6">Other Problems to Solve</h1></div>
                        <div className={isActive ? "col " : "col d-none"}>
                            <div>Similar Problems</div>
                            {tag_sim.map((g) => (
                                <ul > <Link href={`/problems/${g.ccode}`}><a>{g.ccode}</a></Link> </ul>
                            ))}
                        </div>
                        <div className={isActive ? "col " : "col d-none"}>
                            <div>Opposite Problems</div>
                            {op_tag.map((g) => (
                                <ul > <Link href={`/problems/${g.ccode}`}><a>{g.ccode}</a></Link> </ul>
                            ))}
                        </div>
                        <div className={isIncorrect ? "col " : "col d-none"}>
                            <div>Easier Problems</div>
                            {low_diff_problem_recog.map((g) => (
                                <ul > <Link href={`/problems/${g.code}`}><a>{g.code}</a></Link> </ul>
                            ))}
                        </div>
                        <div className={isActive ? "col " : "col d-none"}>
                            <div>Similar Difficulty Problems</div>
                            {sim_diff_problem_recog.map((g) => (
                                <ul > <Link href={`/problems/${g.code}`}><a>{g.code}</a></Link> </ul>
                            ))}
                        </div>
                        <div className={isCorrect ? "col " : "col d-none"}>
                            <div>Challenging Problems</div>
                            {high_diff_problem_recog.map((g) => (
                                <ul > <Link href={`/problems/${g.code}`}><a>{g.code}</a></Link> </ul>
                            ))}
                        </div>
                    </DIV2>

                </div>
            </div>

        </div>


    );
    */
};

export default List;
