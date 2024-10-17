import React, { createContext, useState, useEffect } from "react";
import { post, get } from "../utils/api";
import { toast } from "react-toastify";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const login = async (email, password) => {
        try {
            const response = await post(
                "/api/customUser/token/",
                {
                    email,
                    password,
                },
                {
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                }
            );
            if (response.code === 200 && response.data) {
                localStorage.setItem("token", response.data.token);
                localStorage.setItem("user_id", response.data.user_id);
                setUser({ id: response.data.user_id, email });
            }
            return response;
        } catch (err) {
            console.error("Login error:", err);
            return err.response ? err.response.data : { code: 500, msg: "未知错误" };
        }
    };

    const register = async (name, email, password) => {
        try {
            const response = await post("/api/customUser/create/", {
                email,
                password,
                name,
            });
            if (response.code === 201 && response.data) {
                return await login(email, password);
            } else {
                throw new Error(response.msg || "注册失败");
            }
        } catch (err) {
            toast.error(err.message);
            throw err;
        }
    };

    const logout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("user_id");
        setUser(null);
        toast.info("您已成功登出");
    };

    const getCurrentUser = () => {
        return user;
    };

    useEffect(() => {
        const checkAuth = async () => {
            const token = localStorage.getItem("token");
            const userId = localStorage.getItem("user_id");
            if (token && userId) {
                try {
                    // 这里可以添加一个验证 token 的 API 调用
                    setUser({ id: userId });
                } catch (err) {
                    localStorage.removeItem("token");
                    localStorage.removeItem("user_id");
                }
            }
            setLoading(false);
        };

        checkAuth();
    }, []);

    const value = {
        user,
        setUser,
        loading,
        error,
        login,
        register,
        logout,
        getCurrentUser,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};
