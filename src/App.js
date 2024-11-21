import {BrowserRouter as Router, Routes,Route } from "react-router-dom";
import Navbar from "./components/navBar";
import Home from "./pages/home"


function App() {
  return (
    <Router>
      <Navbar/>
      <Routes>
        <Route path="/" element={<Home/>}/>
        {/* <Route element={<Home/>}/> */}

      </Routes>
    </Router>
  );
}

export default App;
