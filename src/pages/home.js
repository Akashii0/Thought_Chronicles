import axios from "axios";
import { useState,useEffect } from "react";
import BlogList from "../components/blogList";



const Home = () => {
const [blogs, setBlogs] = useState([])
    useEffect (() => {
        axios.get("http://localhost:8000/blogs")
        .then(res =>{
            setBlogs(res.data)
        })
        
        .catch(err =>{
            console.log(err)
        })
        
    },[])
    return ( 
        <div className="mt-40">
            
            {blogs && <BlogList blogs={blogs} title={"All Blogs"}/>}
        </div>
     );
}
 
export default Home;