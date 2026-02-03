import {BrowserRouter, Route, Routes} from "react-router-dom";
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
      </BrowserRouter>
  )
}

export default App
