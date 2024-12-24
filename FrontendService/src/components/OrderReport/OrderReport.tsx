import React, { useState, useEffect } from 'react';
import { orderApi } from '../../services/orderApi';
import OrderReportUI from './OrderReportUI';
import { useDispatch, useSelector } from 'react-redux';
import { selectOrder } from '../../provider/Order/selectors';
import { createOrder } from '../../provider/Order/slice';

interface OrderReportProps {
  orderId: string;
  onClose: () => void;
  socketConnection?: WebSocket;
}

const OrderReport: React.FC<OrderReportProps> = ({ orderId, onClose, socketConnection }) => {
  // const [order, setOrder] = useState<Order | null>(null);
  const [error, setError] = useState<string | null>(null);

  const dispatch = useDispatch();

  const order = useSelector(selectOrder);

  useEffect(() => {
    const fetchOrderDetails = async () => {
      try {
        const orderDetails = await orderApi.getOrderDetails(orderId);
        dispatch(createOrder(orderDetails));
      } catch (err) {
        setError('Не удалось загрузить детали заказа');
        console.error(err);
      }
    };
    fetchOrderDetails();

    if (socketConnection) {
      socketConnection.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.order_id === orderId) {
            dispatch(createOrder(data));
          }
        } catch (err) {
          console.error('Error parsing socket message:', err);
        }
      };
    }

    return () => {
      if (socketConnection) {
        socketConnection.onmessage = null;
      }
    };
  }, [orderId, socketConnection]);

  if (error) {
    return (
      <div className="order-report error">
        <p>{error}</p>
        <button onClick={onClose}>Закрыть</button>
      </div>
    );
  }

  if (!order) {
    return <div>Загрузка...</div>;
  }

  return (
    <OrderReportUI order={order} onClose={onClose} />
  );
};

export default OrderReport;
