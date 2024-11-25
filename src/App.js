import {BrowserRouter as Router, Routes,Route } from "react-router-dom";
import MainLayout from "./components/mainLayout";
import Home from "./pages/home"
import NewBlog from "./pages/newBlogs";
import AuthForm from "./AuthForm";


function App() {
  return (
    <Router>
      <Routes>
      <Route exact path="/" element={<AuthForm/>}/>
        <Route  path="/home" element={<MainLayout><Home/></MainLayout>}/>
        <Route path="newblog" element={<MainLayout><NewBlog/></MainLayout>}/>

      </Routes>
    </Router>
  );
}

export default App;
