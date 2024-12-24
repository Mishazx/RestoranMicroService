import React, { FC, useState } from 'react';
import OrderFormUI from './OrderFormUI';
import OrderReport from '../OrderReport/OrderReport';
import { useDispatch, useSelector } from 'react-redux';
import { addItem, setTableNumber, removeAllItems, changeItemQuantity, changeItemName } from '../../provider/OrderForm/slice';
import { RootState } from '../../services/store';
import { orderApi } from '../../services/orderApi';

interface OrderFormProps {
  setOrderId: (orderId: string) => void;
  socketConnection?: WebSocket;
}

const OrderForm: FC<OrderFormProps> = ({ setOrderId, socketConnection }) => {
  const dispatch = useDispatch();
  const [currentOrderId, setCurrentOrderId] = useState<string | null>(null);
  const tableNumber = useSelector((state: RootState) => state.orderForm.tableNumber);
  const items = useSelector((state: RootState) => state.orderForm.items);

  const handleTableNumberChange = (value: string) => {
    dispatch(setTableNumber(value));
  };

  const handleAddItem = () => {
    dispatch(addItem({ name: '', quantity: 0 }));
  };

  const onItemNameChange = (index: number, value: string) => {
    dispatch(changeItemName({ index, name: value }));
  };

  const onItemQuantityChange = (index: number, value: number) => {
    dispatch(changeItemQuantity({ index, quantity: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const data = {
        table_number: Number(tableNumber),
        items: items.map((item) => ({
          id: item.id.toString(), // Convert id to string
          name: item.name,
          quantity: item.quantity.toString()
        })) 
      };
      const response = await orderApi.createOrder(data);
      setOrderId(response.id);
      setCurrentOrderId(response.id);
      console.log('Заказ успешно создан!');
      // Очищаем форму
      dispatch(setTableNumber(''));
      dispatch(removeAllItems());
    } catch (error) {
      alert('Ошибка при создании заказа');
      console.error('Error:', error);
    }
  };

  const handleCloseOrderReport = () => {
    setCurrentOrderId(null);
  };

  return (
    <>
      {currentOrderId ? (
        <OrderReport 
          orderId={currentOrderId} 
          onClose={handleCloseOrderReport} 
          socketConnection={socketConnection} 
        />
      ) : (
        <OrderFormUI
          tableNumber={tableNumber}
          items={items}
          onTableNumberChange={handleTableNumberChange}
          onItemNameChange={onItemNameChange}
          onItemQuantityChange={onItemQuantityChange}
          onAddItem={handleAddItem}
          onSubmit={handleSubmit}
        />
      )}
    </>
  );
};

export default OrderForm;
