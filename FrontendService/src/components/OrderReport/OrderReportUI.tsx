import { Order } from '../../types/Order';
import { FC } from 'react';
import './OrderReport.css';

interface OrderReportUIProps {
  order: Order;
  onClose: () => void;
}

const OrderReportUI: FC<OrderReportUIProps> = ({order, onClose}) => {
  return (
    <div className="order-report">
      <button className="close-button" onClick={onClose}>✖</button>
      <h2>Отчет о заказе</h2>
      <div className="order-details">
        <p>Номер заказа: {order.order_id}</p>
        <p>Столик: {order.table_number}</p>
        <p>Время создания: {new Date(order.created_at).toLocaleString()}</p>
        <p>Статус: {order.status}</p>
      </div>
      <div className="order-items">
        <h3>Блюда:</h3>
        <table>
          <thead>
            <tr>
              <th>Блюдо</th>
              <th>Количество</th>
            </tr>
          </thead>
          <tbody>
            {order.items.map((item, index) => (
              <tr key={index}>
                <td>{item.name}</td>
                <td>{item.quantity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* {orderStatus.total_price && (
        <div className="order-total">
          <h3>Итого: {orderStatus.total_price} ₽</h3>
        </div>
      )} */}
    </div>
  );
};

export default OrderReportUI;