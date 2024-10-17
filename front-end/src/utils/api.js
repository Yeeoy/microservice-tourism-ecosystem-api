import axios from "axios";

// 创建 axios 实例
const api = axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL || "http://localhost:8000", // 更新为正确的基础URL
    timeout: 10000,
    headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
    },
});

// 请求拦截器
api.interceptors.request.use(
    (config) => {
        // 从 localStorage 获取 token
        const token = localStorage.getItem("token");
        if (token) {
            config.headers["Authorization"] = `Token ${token}`;
        }

        // 添加 CSRF token
        const csrfToken = getCookie("csrftoken");
        if (csrfToken) {
            config.headers["X-CSRFTOKEN"] = csrfToken;
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 获取 CSRF token 的函数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

// 响应拦截器
api.interceptors.response.use(
    (response) => {
        return response.data;
    },
    (error) => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    // 未授权，可能是token过期
                    // 这里可以处理登出逻辑
                    localStorage.removeItem("token");
                    window.location.href = "/login";
                    break;
                case 404:
                    console.error("请求的资源不存在");
                    break;
                case 500:
                    console.error("服务器错误");
                    break;
                default:
                    console.error(`未处理的错误: ${error.response.status}`);
            }
        } else if (error.request) {
            console.error("未收到响应", error.request);
        } else {
            console.error("请求配置时出错", error.message);
        }
        return Promise.reject(error);
    }
);

// 封装 GET 请求
export const get = (url, params = {}) => api.get(url, { params });

// 封装 POST 请求
export const post = (url, data = {}, config = {}) =>
    api.post(url, data, config);

// 封装 PUT 请求
export const put = (url, data = {}) => api.put(url, data);

// 封装 DELETE 请求
export const del = (url) => api.delete(url);

// 封装 PATCH 请求
export const patch = (url, data = {}) => api.patch(url, data);

export default api;
