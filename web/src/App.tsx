import {BrowserRouter, Route, Routes} from "react-router-dom";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";
import EmailDetail from "./pages/EmailDetail";
import "./App.css";

function App() {
  return (
      <BrowserRouter>
          <Routes>
              {/*TODO: Add login path (landing vs login)*/}
              <Route path="/" element={<Landing />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/email/:id" element={<EmailDetail />} />
          </Routes>
          <ToastContainer
              position="top-right"
              autoClose={3000}
              hideProgressBar={false}
              closeOnClick
          />
      </BrowserRouter>
  )
}

export default App
