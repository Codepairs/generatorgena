import React, { useContext, useState } from "react";
import { AuthContext } from "../context";
import style from "../styles/Light/Login.module.css";
import MyButton from "../UI/components/buttons/MyButton";
import MyInput from "../UI/components/input/MyInput";
import 'bootstrap/dist/css/bootstrap.min.css';
import { useTranslation } from 'react-i18next';
import { useHistory } from 'react-router-dom';

const LoginLight = () => {
    // состояния для авторизации (об это я подумаю позже)
    const { isAuth, setIsAuth } = useContext(AuthContext);
    // переменные 
    const [loginData, setLoginData] = useState({ name: '', password: '' });
    // не помню зачем делала, но пусть пока будут
    const [submitted, setSubmitted] = useState(false);
    // для чтения логина из поля ввода
    const handleUsernameChange = (event) => {
        const name = event.target.value;
        setLoginData({ ...loginData, name: name });
    };
    // для чтения пароля из поля ввода
    const handlePasswordChange = (event) => {
        const password = event.target.value;
        setLoginData({ ...loginData, password });
    };
    const handleRedirectToMain = () => {
        history.push('/main');
    };
    const [isRemember, setRemember] = useState()

    const login = async (event) => {
        event.preventDefault();
        setSubmitted(true);

        const url = 'http://localhost:8000/api/users/login/';

        const data = {
            username: loginData.name,
            password: loginData.password
        };
        console.log('AAAAAAAAAAAAA')
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                console.error('Ошибка при выполнении запроса:');
                return
            }

            const result = await response.json();

            localStorage.setItem('accessToken', result.access);
            localStorage.setItem('refreshToken', result.refresh);
            handleRedirectToMain();
            console.log(result)
        } catch (error) {
            console.error('Error during login:', error);
        }
    };
    // для смены языка с русского на английский и тд
    const { t, i18n } = useTranslation();
    // для перехода между страницами
    const history = useHistory();
    // при нажатии на кнопку регистрации
    const handleRedirectToRegistration = () => {
        history.push('/registration');
    };
    // при нажатии на надпись Забыли пароль?
    const handleRedirectToChangeCode = () => {
        history.push('/change-code');
    };
    const returnToLogin = () => {
        history.push('/login');
    };
    const returnOurTeam = () => {
        history.push('/ourteam');
    };
    const returnLinks = () => {
        history.push('/links');
    };
    // проверка корректны ли данные, которые введены в поля логина и пароля
    const [showForgotPassword, setShowForgotPassword] = useState(false);
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
                {/** основные компоненты */}
                <div className="container-fluid">
                    <div className={style.MainPage}>
                        <div className="row">
                            {/** пустота*/}
                            <div className={'col-lg-2'}></div>
                            {/** основная информация и ссылки для скачивания */}
                            <div className={`col-lg-5 text-center`}>
                                <div className={style.Info}>
                                    <h2>Генератор Гена</h2>
                                    <h3>Сервис для генерации изображения по промпту</h3>
                                    <div className={style.Link}>
                                        <a
                                            onClick={returnLinks}
                                            className={style.text}
                                        >
                                            App Store
                                        </a>
                                        <a
                                            onClick={returnLinks}
                                            className={style.text}
                                        >
                                            Google Play
                                        </a>
                                        <a
                                            onClick={returnLinks}
                                            className={style.text}
                                        >
                                            Linux
                                        </a>
                                        <a
                                            onClick={returnLinks}
                                            className={style.text}
                                        >
                                            Windows
                                        </a>
                                    </div>
                                </div>
                            </div>
                            {/** форма*/}
                            <div className={`col-lg-3`}>
                                <div className={style.MainForm}>
                                    <form className={style.form} onSubmit={login} >
                                        <h1>Войти</h1>
                                        <MyInput
                                            className={style.inputLogin}
                                            type="text"
                                            placeholder='Введите имя пользователя'
                                            onChange={handleUsernameChange}
                                        />
                                        <MyInput
                                            className={style.inputPass}
                                            type="password"
                                            placeholder='Введите пароль'
                                            onChange={handlePasswordChange}
                                        />
                                        { // условное отображение, чтобы можно было перейти на страницу смены пароля
                                            showForgotPassword
                                                ?
                                                <a
                                                    onClick={handleRedirectToChangeCode}
                                                    className={style.error}
                                                >
                                                    Забыли пароль?
                                                </a>
                                                :
                                                <div className={style.Remember}>
                                                    <p className={style.remember}>
                                                        <input
                                                            onChange={(e) => setRemember(e.target.checked)}
                                                            type="checkbox"
                                                            checked name="remember"
                                                        />
                                                        Сохранить данные?
                                                    </p>
                                                </div>}
                                        <MyButton

                                            type="submit"
                                            style={{ backgroundColor: '#1F5CB6', color: '#ffffff' }}
                                        >
                                            Войти
                                        </MyButton>
                                        <MyButton
                                            onClick={handleRedirectToRegistration}
                                            style={{ backgroundColor: '#ffffff', color: '#1F5CB6', margin: '0px' }}
                                        >
                                            Зарегистрироваться
                                        </MyButton>
                                    </form>
                                </div>
                                {/** QR */}
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
export default LoginLight;