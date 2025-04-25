import React, { useState, useEffect } from "react";
import MainLight from "./MainLight.jsx";
const Main = () => {
    const [darkMode, setDarkMode] = useState(false);
    useEffect(() => {
        const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");
        setDarkMode(prefersDarkScheme.matches);
        const handleChange = (e) => {
            setDarkMode(e.matches);
        };
        prefersDarkScheme.addEventListener("change", handleChange);
        return () => {
            prefersDarkScheme.removeEventListener("change", handleChange);
        };
    }, []);

    return (
        <div>
             <MainLight />
        </div>
    );
};
export default Main;