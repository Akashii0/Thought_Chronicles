const BlogList = ({blogs,title}) => {
    // const blogs = props.blogs;
    // const title = props.title
    return ( 
        <div className="mt-40">
            <h1 className="text-5xl font-black">
                {title}
            </h1>
            {blogs.map((blog)=>(
                <div key={blog.id}>
                    <h2>{blog.title}</h2>
                    <p>Written by: {blog.author}</p>
                </div>
            ))}

        </div>
     );
}
 
export default BlogList;