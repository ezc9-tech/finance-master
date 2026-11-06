import './index.css'
import { BrowserRouter, Routes, Route } from 'react-router';
import LoginPage from './pages/LoginPage';
import RegistrationPage from './pages/RegistrationPage';
import UnderConstruction from './pages/UnderConstruction';
import { Toaster } from 'react-hot-toast';

function App() {
  return (
    <>
      <Toaster position="top-center"/>
      <BrowserRouter>
        <Routes>
          <Route path="*" element={<UnderConstruction/>} />
          <Route path="/login" element={<LoginPage/>} />
          <Route path="/register" element={<RegistrationPage/>} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App