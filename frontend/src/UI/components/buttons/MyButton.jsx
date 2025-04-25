import React from "react";
import style from '../../../styles/MyButton.module.css'

const MyButton = ({children, ...props}) => {
    return (
        <button {...props} className={style.MyButton}>
            {children}
        </button>
    );
};

export default MyButton;
