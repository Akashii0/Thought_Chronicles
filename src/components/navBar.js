import { Link } from "react-router-dom";


const Navbar = () => {
    return ( 
        <nav className="w-[80%] m-auto flex justify-between items-center">
            <h1 className="font-bold text-5xl">Blog</h1>
            <ul className="flex items-center justify-center space-x-6">
                <Link to="/home">Home</Link>
                <Link to="/newblog">New Blog</Link>
            </ul>
        </nav>
     );
}
 
export default Navbar;