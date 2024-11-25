//import api from "../api/axiosConfig";
import UseFetch from "./useFetch";
import { useParams } from "react-router-dom";

const BlogDetails = () => {
    const {id} = useParams();
    const {data:blog,loading,error} = UseFetch(`http://localhost:8000/blogs/${id}`);
    return ( 
        <div>
            {loading && <div>Loading...</div>}
            {error && <div>{error}</div>}
            {blog && (<article className="mt-40 w-[80%] m-auto flex flex-col gap-5 justify-center items-center">
                    <h2 className="text-4xl font-black">{blog.title}</h2>
                    <div>{blog.body}</div>
                    {/* <button onClick={handleClick}>Delete</button> */}
                    <p className="text-[14px]">Written by: {blog.owner.author}</p>
                </article>)}
        </div>
     );
}
 
export default BlogDetails;