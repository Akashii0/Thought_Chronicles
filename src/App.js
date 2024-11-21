import {BrowserRouter as Router, Routes,Route } from "react-router-dom";
import Navbar from "./components/navBar";
import Home from "./pages/home"
import NewBlog from "./pages/newBlogs";


function App() {
  return (
    <Router>
      <Navbar/>
      <Routes>
        <Route exact path="/" element={<Home/>}/>
        <Route path="newblog" element={<NewBlog/>}/>

      </Routes>
    </Router>
  );
}

export default App;
