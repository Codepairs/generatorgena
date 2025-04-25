
import React, { useState, useEffect } from 'react';
// import './App.css';
import { AuthContext } from './context/index.js';
import AppRouter from './components/AppRouter.jsx';

function App() {
  const [isAuth, setIsAuth] = useState(false);
  useEffect(() => {
    if (localStorage.getItem('auth')) {
      setIsAuth(true)
    }
  }, [])
  return (
    <AuthContext.Provider value={{
      isAuth,
      setIsAuth,
    }}>
      <AppRouter />
    </AuthContext.Provider>
  );
}

export default App;
