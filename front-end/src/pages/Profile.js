import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/authContext';
import { get, patch } from '../utils/api';
import { toast } from 'react-toastify';

const Profile = () => {
  const { user, setUser } = useContext(AuthContext);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      const response = await get('/api/customUser/me/');
      if (response.code === 200 && response.data) {
        setName(response.data.name);
        setEmail(response.data.email);
      }
    } catch (err) {
      toast.error('获取用户信息失败');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const updateData = { name };
      if (password) {
        updateData.password = password;
      }
      const response = await patch('/api/customUser/me/', updateData);
      if (response.code === 200 && response.data) {
        setUser({ ...user, name: response.data.name });
        toast.success('个人资料更新成功');
        setIsEditing(false);
        setPassword('');
      }
    } catch (err) {
      toast.error('更新失败，请稍后再试');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h2 className="text-2xl font-bold mb-4">个人资料</h2>
      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
            电子邮箱
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="email"
            type="email"
            value={email}
            disabled
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="name">
            姓名
          </label>
          {isEditing ? (
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          ) : (
            <p className="py-2 px-3 text-gray-700">{name}</p>
          )}
        </div>
        {isEditing && (
          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
              新密码 (留空则不修改)
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        )}
        {isEditing ? (
          <div className="flex items-center justify-between">
            <button
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="button"
              onClick={handleSubmit}
            >
              保存
            </button>
            <button
              className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="button"
              onClick={() => {
                setIsEditing(false);
                setPassword('');
              }}
            >
              取消
            </button>
          </div>
        ) : (
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="button"
            onClick={() => setIsEditing(true)}
          >
            编辑
          </button>
        )}
      </div>
    </div>
  );
};

export default Profile;