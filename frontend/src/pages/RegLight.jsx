import React, { useContext, useState} from "react";
import { AuthContext } from "../context";
import style from "../styles/Light/Registration.module.css"
import MyButton from "../UI/components/buttons/MyButton";
import MyInput from "../UI/components/input/MyInput";
import 'bootstrap/dist/css/bootstrap.min.css';
import { useTranslation } from 'react-i18next';
import { useHistory } from 'react-router-dom';


const RegLight = () => {
    const { isAuth, setIsAuth } = useContext(AuthContext);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);
    
    const [loginData, setLoginData] = useState({ username: '', password: '', email: '' });
    const handleUsernameChange = (event) => {
        const username = event.target.value;
        setLoginData({ ...loginData, username });
    };

    const handlePasswordChange = (event) => {
        const password = event.target.value;
        setLoginData({ ...loginData, password });
    };
    const handleEmailChange = (event) => {
        const email = event.target.value;
        setLoginData({ ...loginData, email });
    };
    const handleSubmit = async (event) => {
        event.preventDefault();
        setIsLoading(true);
        setError(null);
        
        try {
            const response = await fetch('http://localhost:8000/api/users/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loginData)
            });
            console.log('Registration successful:');
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Registration failed');
            }

            const data = await response.json();
            console.log('Registration successful:', data);
            setSuccess(true);
            handleRedirectToLogin();

        } catch (err) {
            console.error('Registration error:', err);
            setError(err.message || 'Something went wrong');
        } finally {
            setIsLoading(false);
        }
    };
    // переход между страницами
    const history = useHistory();
    const handleRedirectToLogin = () => {
        history.push('/login');
    };
    const returnToLogin = () => {
        history.push('/login');
    };
    const returnOurTeam = () => {
        history.push('/ourteam');
    };
    const { t, i18n } = useTranslation('translation');
    return (
        <div>
            {/** контейнер страницы */}
            <div className={style.LoginPage}>
                {/** заголовок*/}
                <div className={style.Header}>
                    <a
                        onClick={returnToLogin}
                        className={style.HeaderLink}
                    >
                        Генератор Гена
                    </a>
                </div>
                <div className="container-fluid">
                    <div className={style.MainPage}>
                        <div className="row">
                            <div className={'col-lg-2'}></div>
                            <div className={`col-lg-5 text-center`}>
                                <div className={style.Info}>
                                    <h2>Генератор Гена</h2>
                                    <h3 className={style.text}>Сервис для генерации изображения по промпту</h3>
                                    <div className={style.Link}>
                                        <a className={style.text}>App Store</a>
                                        <a className={style.text}>Google Play</a>
                                        <a className={style.text}>Linux</a>
                                        <a className={style.text}>Windows</a>
                                    </div>
                                </div>
                            </div>
                            <div className={`col-lg-3`}>
                                <div className={style.MainForm}>
                                    <form className={style.form} >
                                        <h1>Начать пользоваться</h1>
                                        <MyInput
                                            style={{ margin: '0px', marginTop: '8%' }}
                                            type="text"
                                            placeholder='Введите имя пользователя'
                                            onChange={handleUsernameChange}
                                        />
                                        <MyInput
                                            style={{ margin: '0px', marginTop: '8%' }}
                                            type="text"
                                            placeholder='Введите email'
                                            onChange={handleEmailChange}
                                        />
                                        <MyInput
                                            style={{ margin: '0px', marginTop: '8%' }}
                                            type="password"
                                            placeholder='Введите пароль'
                                            onChange={handlePasswordChange}
                                        />
                                        <MyButton
                                            style={{ backgroundColor: '#1F5CB6', color: '#ffffff', margin: '0px', marginTop: '8%' }}
                                            onClick={handleSubmit}
                                        >
                                            Продолжить
                                        </MyButton>
                                    </form>
                                </div>
                                <div className={style.QR} >
                                    <div className={style.textQr}>
                                        <h5 className={style.text}>Да итоговый дизайн отличается от дизайн макета</h5>
                                        <h6 className={style.text}>ИЗВИНИТЕ</h6>
                                        <a className={style.more}>фронтендер не умеет красить кнопки</a>
                                    </div>
                                </div>
                            </div>
                            {/** ссылки внизу страницы */}
                            <div className={style.Bottom}>
                                <h4>Гена © 2025</h4>
                                <a
                                    className={style.text}
                                    onClick={returnOurTeam}
                                    style={{ marginRight: "15%" }}
                                >
                                    Github
                                </a>
                                <a
                                    onClick={() => i18n.changeLanguage('en')}
                                    className={style.text}
                                >
                                    English
                                </a>
                                <a
                                    onClick={() => i18n.changeLanguage('ru')}
                                    className={style.text}
                                    style={{ marginRight: "10%" }}
                                >
                                    Русский
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
export default RegLight;