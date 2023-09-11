import Link from "next/link";
import Greetings from "../../components/Greetings";
import { useRouter } from "next/router";
import NavBar from "../../components/NavBar";

export async function getServerSideProps() {

  const problemlist = await prisma.$queryRaw`select code,name,text,group_concat(tag separator', ') from problems group by code limit 0,50;`;
  


  return {
    props: {
      problemlist
    }
  };
}
function List({ problemlist }) {
  const router = useRouter();

  return (
    
    <div>
      <NavBar/>
      <Greetings />
      <button onClick={() => {
        localStorage.removeItem("username");
        router.replace("/")
      }}>Log Off</button>
      <h1>Problem List</h1>
      <ul>
        {problemlist.map((g) => (
          <li key={g.code}>{g.name}</li>
        ))}
      </ul>
      <div>
        <h1>Today's Problems</h1>
      </div>
    </div>

  );
};

export default List;
