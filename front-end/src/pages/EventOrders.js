import React, { useState, useEffect } from 'react';
import { get, patch, del } from '../utils/api';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import { CalendarIcon, CurrencyDollarIcon, CheckCircleIcon, XCircleIcon, TicketIcon, TrashIcon, ArrowLeftIcon } from '@heroicons/react/24/outline';

const EventOrders = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [events, setEvents] = useState({});
    const navigate = useNavigate();

    useEffect(() => {
        fetchOrders();
    }, []);

    const fetchOrders = async () => {
        try {
            const response = await get('/api/events/venue-booking/');
            if (response.code === 200 && response.data) {
                setOrders(response.data);
                fetchEvents(response.data);
            } else {
                throw new Error(response.msg || '获取订单失败');
            }
        } catch (err) {
            toast.error(err.message || '获取订单失败');
        } finally {
            setLoading(false);
        }
    };

    const fetchEvents = async (orders) => {
        const uniqueEventIds = [...new Set(orders.map(order => order.event_id))];
        const eventPromises = uniqueEventIds.map(async (id) => {
            try {
                const response = await get(`/api/events/event/${id}/`);
                if (response.code === 200 && response.data) {
                    return { [id]: response.data };
                }
            } catch (err) {
                console.error(`获取活动 ${id} 失败:`, err);
            }
            return null;
        });

        const eventResults = await Promise.all(eventPromises);
        const newEvents = Object.assign({}, ...eventResults.filter(Boolean));
        setEvents(newEvents);
    };

    const cancelOrder = async (orderId) => {
        try {
            const response = await patch(`/api/events/venue-booking/${orderId}/`, {
                booking_status: false
            });
            if (response.code === 200 && response.data) {
                setOrders(orders.map(order => 
                    order.id === orderId 
                        ? { ...order, booking_status: false } 
                        : order
                ));
                toast.success('订单已成功取消');
            } else {
                throw new Error(response.msg || '取消订单失败');
            }
        } catch (err) {
            toast.error(err.message || '取消订单失败');
        }
    };

    const deleteOrder = async (orderId) => {
        try {
            await del(`/api/events/venue-booking/${orderId}/`);
            setOrders(orders.filter(order => order.id !== orderId));
            toast.success('订单已成功删除');
        } catch (err) {
            toast.error('删除订单失败');
        }
    };

    const handleGoBack = () => {
        navigate(-1);
    };

    if (loading) {
        return <div className="flex justify-center items-center h-screen">
            <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
        </div>;
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex items-center mb-6">
                <button
                    onClick={handleGoBack}
                    className="bg-white p-2 rounded-full shadow-md hover:bg-gray-100 transition duration-300 mr-4"
                >
                    <ArrowLeftIcon className="h-6 w-6 text-gray-600" />
                </button>
                <h1 className="text-3xl font-bold text-gray-800">我的活动订单</h1>
            </div>
            {orders.length > 0 ? (
                <div className="bg-white shadow-md rounded-lg overflow-hidden">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">活动名称</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">日期</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">票数</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">价格</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {orders.map((order) => (
                                <tr key={order.id} className={!order.booking_status ? 'bg-gray-100' : ''}>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div className="text-sm font-medium text-gray-900">{events[order.event_id]?.name || '加载中...'}</div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div className="flex items-center text-sm text-gray-900">
                                            <CalendarIcon className="h-5 w-5 text-gray-400 mr-2" />
                                            {new Date(order.booking_date).toLocaleDateString()}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div className="flex items-center text-sm text-gray-900">
                                            <TicketIcon className="h-5 w-5 text-gray-400 mr-2" />
                                            {order.number_of_tickets}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div className="flex items-center text-sm font-medium text-gray-900">
                                            <CurrencyDollarIcon className="h-5 w-5 text-green-500 mr-2" />
                                            {order.total_amount}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${order.booking_status ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                            {order.booking_status ? '已确认' : '已取消'}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                        {order.booking_status ? (
                                            <button 
                                                onClick={() => cancelOrder(order.id)} 
                                                className="text-indigo-600 hover:text-indigo-900"
                                            >
                                                取消订单
                                            </button>
                                        ) : (
                                            <button 
                                                onClick={() => deleteOrder(order.id)} 
                                                className="text-red-600 hover:text-red-900"
                                            >
                                                <TrashIcon className="h-5 w-5" />
                                            </button>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ) : (
                <div className="text-center text-gray-600 bg-white p-8 rounded-lg shadow-md">
                    <p className="text-xl mb-4">您还没有任何活动订单。</p>
                    <a href="/events" className="text-blue-500 hover:text-blue-700 transition duration-300">
                        立即报名活动 →
                    </a>
                </div>
            )}
        </div>
    );
};

export default EventOrders;
