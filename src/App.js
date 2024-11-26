import {BrowserRouter as Router, Routes,Route } from "react-router-dom";
import MainLayout from "./components/mainLayout";
import Home from "./pages/home"
import NewBlog from "./pages/newBlogs";
import AuthForm from "./login/AuthForm";
import BlogDetails from "./components/blogDetails";


function App() {
  return (
    <Router>
      <Routes>
      <Route exact path="/" element={<AuthForm/>}/>
        <Route  path="/home" element={<MainLayout><Home/></MainLayout>}/>
        <Route path="newblog" element={<MainLayout><NewBlog/></MainLayout>}/>
        <Route path="/blogs/:id" element={<MainLayout><BlogDetails/></MainLayout>}/>
      </Routes>
    </Router>
  );
}

export default App;
