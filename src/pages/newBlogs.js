// import axios from "axios";
import {  useState } from "react";
import { useNavigate } from "react-router-dom";
import api from '../api/axiosConfig';  // Import the configured axios instance

const NewBlog = () => {
    const [title,setTitle] = useState("")
    const [body,setBody] = useState("")
    const [isPending,setIspending]= useState(false)
    const navigate = useNavigate();

    const handleSubmit=(e)=>{
        e.preventDefault();
        const post = { title, body };
        setIspending(true);

        api.post('/blogs', post, {
            withCredentials: true,  // Ensure credentials are sent
        })
        .then(() => {
            setIspending(false);
            navigate("/home");
            console.log("blog posted successfully");
        })
        .catch((error) => {
            console.error("There was an error creating the blog post!", error);
            setIspending(false);
            navigate("/");
        });
    }


    return ( 
        
        <form className="flex flex-col justify-center w-[100%] items-center mt-20" onSubmit={handleSubmit}>
            <div className="flex flex-col space-y-2 w-[50%]">
                <label>Blog Title</label>
                <input
                className="w-full h-20 rounded-2xl indent-5"
                type="text"
                required
                value={title}
                onChange={(e)=>setTitle(e.target.value)}
                ></input>

            </div>
            <div className="flex flex-col space-y-2 w-[50%]">
                <label>Body</label>
                <textarea
                className="w-full h-44 rounded-2xl indent-5"
                type="text"
                required
                value={body}
                onChange={(e)=>setBody(e.target.value)}
                ></textarea>

            </div>
            {!isPending &&<button className="bg-black text-white p-5 mt-5 rounded-2xl hover:scale-105 transition-all ease-in-out duration-300">Add new blog</button>}
                {isPending &&<button className="bg-black text-white p-5 mt-5 rounded-2xl hover:scale-105 transition-all ease-in-out duration-300"disabled>Adding new blog...</button>}
        </form>
     );
}
 
export default NewBlog;
