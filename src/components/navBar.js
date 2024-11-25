import { Link } from "react-router-dom";
import api from "../api/axiosConfig";
import { useNavigate } from "react-router-dom";


const Navbar = () => {
    const navigate = useNavigate();
    
    const handleLogout = async () => {
        try {
            await api.post('/logout', {}, { withCredentials: true });
            localStorage.removeItem('isAuthenticated'); // Clear authentication state
            navigate('/');  // Use React Router navigation
        } catch (error) {
            console.error('Logout error:', error);
        }
    };

    return ( 
        <nav className="w-[80%] m-auto flex justify-between items-center">
            <h1 className="font-bold text-5xl">Blog</h1>
            <ul className="flex items-center justify-center space-x-6">
                <Link to="/home">Home</Link>
                <Link to="/newblog">New Blog</Link>
                <Link to="/logout" onClick={handleLogout}>Logout</Link>
            </ul>
        </nav>
     );
}
 
export default Navbar;