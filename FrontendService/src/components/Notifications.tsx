import React from 'react';
import { useState } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../services/store';
import useNotifications from '../hooks/Notification';
import { orderApi } from '../services/orderApi';
import './Notifications.css';

const Notifications = ({ orderId }: { orderId: string }) => {
    useNotifications(orderId);

    const { nowMsg, oldMsg } = useSelector((state: RootState) => state.order);
    const [isButtonClicked, setIsButtonClicked] = useState(false);

    const handleConfirmPickup = async () => {
        try {
            await orderApi.confirmPickup(orderId);
            console.log('Pickup confirmed successfully');
            setIsButtonClicked(true);
        } catch (error) {
            console.error('Failed to confirm pickup');
        }
    };

    return (
        <div className="notifications-container">
            {oldMsg.map((msg, index) => (
                <div key={index} className="notification old">
                    <strong>Сообщение:</strong>
                    <div>Статус: {msg.status}</div>
                    <div>Сообщение: {msg.msg}</div>
                    <div>Дата: {msg.date}</div>
                </div>
            ))}
            {nowMsg && (
                <div className="notification new">
                    <strong>NEW status:</strong>
                    <div>Status: {nowMsg.status}</div>
                    <div>Message: {nowMsg.msg}</div>
                    <div>Date: {nowMsg.date}</div>
                    {nowMsg.status === 'READY' && !isButtonClicked && (
                        <button onClick={handleConfirmPickup}>Confirm Pickup</button>
                    )}
                </div>
            )}
        </div>
    );
};

export default Notifications;
