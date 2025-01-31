import axios from 'axios';
import qs from 'qs';

const API_URL = 'http://127.0.0.1:8000';

// Авторизация: вход
export const login = async (credentials) => {
  // Преобразуем объект в формат form-data
  const data = qs.stringify(credentials);

  const response = await axios.post(`${API_URL}/login`, data, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });

  return response.data;
};


// Регистрация пользователя
export const register = async (userData) => {
  const response = await axios.post(`${API_URL}/register`, userData, {
    headers: {
      'Content-Type': 'application/json', // Явное указание заголовков
    },
  });
  return response.data;
};

// Получение защищенных данных (для авторизованных пользователей)
export const fetchDashboardData = async (token) => {
    const response = await axios.get(`${API_URL}/dashboard`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    return response.data;
};
