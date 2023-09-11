import {useRouter} from "next/router";
function LogOff(router){

    function onClick(){
        localStorage.removeItem("username");
        
    }
    return <div>
        <button onClick={onClick}>Log Off</button>
    </div>
}
export default LogOff();