import React, {useState, Suspense } from "react";
import style from "../styles/Light/Main.module.css";
import MyButton from "../UI/components/buttons/MyButton";
import MyInput from "../UI/components/input/MyInput";
import "bootstrap/dist/css/bootstrap.min.css";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

const ChangePassLight = () => {
    const [oldPassword, setOldPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
  
    // Обработчик изменения для input'ов
    const handlePasswordChange = (event) => {
      const { placeholder, value } = event.target;
  
      if (placeholder === 'Введите старый пароль') {
        setOldPassword(value);
      } else if (placeholder === 'Введите новый пароль') {
        setNewPassword(value);
      }
    };
  async function changePassword() {
    // Переменные для смены пароля
    const token = localStorage.getItem("accessToken");

    // URL API для смены пароля
    const url = 'http://localhost:8000/api/users/change-password/';
  
    // Тело запроса в формате JSON
    const body = {
      old_password: oldPassword,
      new_password: newPassword,
    };
  
    try {
      const response = await fetch(url, {
        method: 'PUT', // Метод PUT как в серверной функции
        headers: {
          'Content-Type': 'application/json',               // Тип контента
          'Authorization': `Bearer ${token}`,          // Токен авторизации
        },
        body: JSON.stringify(body), // Преобразуем тело в JSON
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log('Успех:', data.message); // Ожидаем сообщение "Пароль успешно изменён"
      } else {
        const errorData = await response.json();
        console.error('Ошибка:', errorData);
      }
    } catch (error) {
      console.error('Ошибка сети или запроса:', error);
    }
  }
  // переход между страницами
  const historyHook = useHistory();
  const returnToLogin = () => {
    historyHook.push("/login");
  };
  const returnOurTeam = () => {
    historyHook.push("/ourteam");
  };
  const { t, i18n } = useTranslation("translation");
  return (
    <div>
      <Suspense fallback={<div>Loading...</div>}></Suspense>
      {/** контейнер страницы */}
      <div className={style.LoginPage}>
        {/** заголовок*/}
        <div className={style.Header}>
          <a onClick={returnToLogin} className={style.HeaderLink}>
            Генератор Гена
          </a>
        </div>
        <div className="container-fluid">
          <div className={style.MainPage}>
            <div className="row">
              <div className={"col-lg-2"}></div>
              <div className={`col-lg-5 text-center`}>
                <div className={style.Info}>
                  <h2>Генератор Гена</h2>
                </div>
            
              </div>
              <div className={`col-lg-3`}>
                <div className={style.MainForm}>
                  <form className={style.form}>
                    <h1>Обновить пароль</h1>
                    <MyInput
                      style={{ margin: "0px", marginTop: "8%" }}
                      type="password"
                      placeholder="Введите старый пароль"
                      onChange={handlePasswordChange}
                    />
                    <MyInput
                      style={{ margin: "0px", marginTop: "8%" }}
                      type="password"
                      placeholder="Введите новый пароль"
                      onChange={handlePasswordChange}
                    />
                    <MyButton
                      style={{
                        backgroundColor: "#1F5CB6",
                        color: "#ffffff",
                        margin: "0px",
                        marginTop: "8%",
                      }}
                      onClick={changePassword}>
                      Продолжить
                    </MyButton>
                    </form>
                </div>
                <div className={style.QR}>

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
                  onClick={() => i18n.changeLanguage("en")}
                  className={style.text}
                >
                  English
                </a>
                <a
                  onClick={() => i18n.changeLanguage("ru")}
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
export default ChangePassLight;
