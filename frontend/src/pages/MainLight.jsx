import React, { useContext, useState, Suspense, useEffect } from "react";
import { AuthContext } from "../context";
import style from "../styles/Light/Main.module.css";
import MyButton from "../UI/components/buttons/MyButton";
import MyInput from "../UI/components/input/MyInput";
import "bootstrap/dist/css/bootstrap.min.css";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

const MainLight = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [accessToken, setAccessToken] = useState(
    localStorage.getItem("accessToken")
  );
  const [requestData, setRequestData] = useState({ prompt: "" });
  const handlePromptChange = (event) => {
    const prompt = event.target.value;
    setRequestData({ ...requestData, prompt });
  };

  // Функция обновления access токена
  const refreshAccessToken = async () => {
    try {
      const refreshToken = localStorage.getItem("refreshToken");
      if (!refreshToken) {
        throw new Error("Refresh token not found");
      }

      const response = await fetch(
        "http://localhost:8000/api/users/refresh/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ refresh: refreshToken }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to refresh token");
      }

      const data = await response.json();
      const newAccessToken = data.access;

      // Обновляем токен в локальном хранилище и состоянии
      localStorage.setItem("accessToken", newAccessToken);
      setAccessToken(newAccessToken);
    } catch (err) {
      console.error("Error refreshing token:", err);
      alert("Ошибка обновления токена. Пожалуйста, войдите снова.");
      // Здесь можно добавить логику выхода из аккаунта
    }
  };
  // Запускаем таймер обновления токена при загрузке компонента
  useEffect(() => {
    // Обновляем токен сразу при загрузке (по желанию)
    refreshAccessToken();

    const intervalId = setInterval(() => {
      refreshAccessToken();
    }, 5 * 60 * 1000); // 5 минут

    return () => clearInterval(intervalId); // Очистка таймера при размонтировании
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);

    try {
      const userId = getUserIdFromToken();
      const token = await refreshAccessToken();
      if (!token) {
        throw new Error("JWT token not found in localStorage");
      }

      // Отправляем POST-запрос
      const response = await fetch("http://localhost:8000/api/requests/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          user_id: userId,
          prompt: requestData.prompt,
        }),
      });

      if (response.status === 201) {
        const data = await response.json();
        const operationId = data.operationID;

        // Функция для повторного запроса изображения с задержкой
        const fetchImageWithRetry = async (retries = 5, delay = 2000) => {
          for (let i = 0; i < retries; i++) {
            const imageResponse = await fetch(
              `http://localhost:8000/api/getimage/?operation_id=${operationId}&user_id=${userId}`,
              {
                headers: {
                  Authorization: `Bearer ${token}`,
                },
              }
            );

            if (imageResponse.ok) {
              const blob = await imageResponse.blob();
              const imageUrl = URL.createObjectURL(blob);
              setImageSrc(imageUrl);
              return; // Успешно получили изображение, выходим из функции
            } else if (imageResponse.status === 404) {
              // Изображение ещё не готово, ждём и повторяем попытку
              await new Promise((res) => setTimeout(res, delay));
            } else {
              // Ошибка, прерываем попытки
              alert("Ошибка при получении изображения");
              return;
            }
          }
          alert("Изображение не появилось в течение ожидания");
        };

        // Запускаем получение изображения с повторными попытками
        await fetchImageWithRetry();
      } else {
        alert(`Ошибка при отправке запроса: статус ${response.status}`);
      }
    } catch (error) {
      alert(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const [imageSrc, setImageSrc] = useState(null);
  function getUserIdFromToken() {
    const token = localStorage.getItem("accessToken"); // Получаем токен из localStorage
    if (!token) {
      throw new Error("JWT token not found in localStorage");
    }

    // Декодируем токен (предполагаем, что он закодирован в формате base64)
    const payload = token.split(".")[1]; // Берем среднюю часть токена
    const decodedPayload = JSON.parse(atob(payload)); // Декодируем base64 и парсим JSON
    console.log(decodedPayload);
    return decodedPayload.user_id; // Предполагаем, что ID пользователя хранится в поле userId
  }

  // Функция для отправки запроса на историю запросов
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false); // Состояние для отображения истории
  const [selectedRequest, setSelectedRequest] = useState(null); // Состояние для хранения информации о выбранном запросе

  const fetchUserHistory = async () => {
    try {
      setIsLoading(true); // Начинаем загрузку
      const userId = getUserIdFromToken();
      const token = localStorage.getItem("accessToken");
      if (!token) {
        throw new Error("Access token not found");
      }

      const response = await fetch(
        `http://localhost:8000/api/users/history/?user_id=${userId}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`, // формат токена для JWT
          },
        }
      );

      if (!response.ok) {
        throw new Error(`Ошибка при получении истории: ${response.status}`);
      }

      const data = await response.json();
      console.log(data[2].operationID)
      // Предполагаем, что data — массив запросов, сортируем и берём последние 3
      const lastThree = data.slice(-3).reverse();
      setHistory(lastThree);
      setShowHistory(true); // Показываем историю после загрузки
    } catch (err) {
      alert(err.message);
    } finally {
      setIsLoading(false); // Заканчиваем загрузку
    }
  };

  // Функция для получения информации о конкретном запросе
  const fetchRequestDetails = async (requestId) => {
    try {
      setIsLoading(true);
      console.log(requestId)
      const userId = getUserIdFromToken();
      const token = localStorage.getItem("accessToken");
      const url = new URL(`https://your-api-domain.com/api/requests/${requestId}`);
      url.searchParams.append('user_id', userId);


      if (!token) {
        throw new Error("Access token not found");
      }

      const response = await fetch(
        url.toString(),
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error(`Ошибка при получении деталей запроса: ${response.status}`);
      }

      const data = await response.json();
      setSelectedRequest(data);
    } catch (err) {
      alert(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Условное форматирование элементов списка истории
  const getItemStyle = (item) => {
    // Здесь можно добавить логику для определения стиля элемента в зависимости от его свойств
    return {
      backgroundColor: item.success ? "#e6ffe6" : "#ffe6e6", // Зеленый для успешных, красный для неудачных
      padding: "10px",
      margin: "5px 0",
      borderRadius: "5px",
      cursor: "pointer", // Добавляем курсор, чтобы показать, что элемент кликабельный
    };
  };

  async function deleteUser() {
    const userId = getUserIdFromToken();
      const token = localStorage.getItem("accessToken");
    try {
      const response = await fetch(`http://localhost:8000/api/users/?user_id=${userId}`, {
        method: 'DELETE', // метод запроса DELETE
        headers: {
          'Content-Type': 'application/json', // тип контента
          'Authorization': `Bearer ${accessToken}` // токен авторизации
        }
      });
  
      if (!response.ok) {
        throw new Error(`Ошибка HTTP: ${response.status}`);
      }
  
      const data = await response.json();
      console.log('Пользователь удалён:', data);
    } catch (error) {
      console.error('Ошибка при удалении пользователя:', error);
    }
  }
  // переход между страницами
  const historyHook = useHistory();
  const returnToLogin = () => {
    historyHook.push("/login");
  };
  const returnToChangePass = () => {
    historyHook.push("/change-pass");
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
                <div style={{ height: "80% " }}>
                  {imageSrc && (
                    <img src={imageSrc} alt="Полученное изображение" />
                  )}
                </div>
              </div>
              <div className={`col-lg-3`}>
                <div className={style.MainForm}>
                  <form className={style.form}>
                    <h1>Введите промпт</h1>
                    <MyInput
                      style={{ margin: "0px", marginTop: "8%" }}
                      type="text"
                      placeholder="Введите промпт"
                      onChange={handlePromptChange}
                    />
                    <MyButton
                      style={{
                        backgroundColor: "#1F5CB6",
                        color: "#ffffff",
                        margin: "0px",
                        marginTop: "8%",
                      }}
                      onClick={handleSubmit}
                    >
                      Продолжить
                    </MyButton>
                    <MyButton
                      style={{
                        backgroundColor: "#1F5CB6",
                        color: "#ffffff",
                        margin: "0px",
                        marginTop: "8%",
                      }}
                      onClick={fetchUserHistory}
                      disabled={isLoading}
                    >
                      История
                    </MyButton>
                  </form>
                  {showHistory && (
                    <div>
                      <h2>История запросов</h2>
                      <ul>
                        {history.map((item, index) => (
                          <li
                            key={index}
                            style={getItemStyle(item)}
                            onClick={() => fetchRequestDetails(item.operationID)} // Обработчик клика
                          >
                            {item.prompt || JSON.stringify(item)}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {selectedRequest && (
                    <div>
                      <h2>Детали запроса</h2>
                      <p>ID: {selectedRequest.id}</p>
                      <p>Prompt: {selectedRequest.prompt}</p>
                      {selectedRequest.image && (
                        <img
                          src={selectedRequest.image}
                          alt="Изображение запроса"
                        />
                      )}
                    </div>
                  )}
                </div>
                <div className={style.QR}>
                  <MyButton
                    onClick={deleteUser}
                    style={{ backgroundColor: '#ffffff', color: '#1F5CB6', margin: '15px' }}
                  >
                    Удалить пользователя
                  </MyButton>
                  <MyButton
                    onClick={returnToChangePass}
                    style={{ backgroundColor: '#ffffff', color: '#1F5CB6', margin: '15px' }}
                  >
                   Поменять пароль
                  </MyButton>
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
export default MainLight;
