import React from 'react';
import { FC } from 'react';
import './OrderForm.css';

interface OrderFormUIProps {
  tableNumber: string;
  items: { id: number; name: string; quantity: number }[];
  onTableNumberChange: (value: string) => void;
  onItemNameChange: (index: number, value: string) => void;
  onItemQuantityChange: (index: number, value: number) => void;
  onAddItem: () => void;
  onSubmit: (e: React.FormEvent) => void;
}

const OrderFormUI: FC<OrderFormUIProps> = ({
  tableNumber,
  items,
  onTableNumberChange,
  onItemNameChange,
  onItemQuantityChange,
  onAddItem,
  onSubmit,
}) => {
  const availableOptions = ["пицца", "суши", "бургеры"];

  const getFilteredOptions = (index: number) => {
    const selectedOptions = items.map(item => item.name).filter(name => name !== "");
    return availableOptions.filter(option => !selectedOptions.includes(option) || items[index].name === option);
  };

  // useEffect(() => {
  //   // getFilteredOptions(0);
  //   // onAddItem();
  // }, [items]);

  return (
    <div className="order-form">
      <h2>Создать заказ</h2>
      <form onSubmit={onSubmit} className="form">
        <div className="form-group">
          <label>
            Номер столика:
            <input
              type="number"
              value={tableNumber}
              onChange={(e) => onTableNumberChange(e.target.value)}
              required
              className="form-input-table"
            />
          </label>
        </div>

        <div className="item-container">
          {items.map((item, index) => (
            <div key={index} className="item-row">
              <label className="item-label">
                Блюдо:
                <select
                  value={item.name}
                  onChange={(e) => onItemNameChange(index, e.target.value)}
                  required
                  className="form-input"
                >
                  <option value="">Выберите блюдо</option>
                  {getFilteredOptions(index).map(option => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </label>
              <label className="item-label">
                Количество:
                <input
                  type="number"
                  value={item.quantity}
                  onChange={(e) => onItemQuantityChange(index, parseInt(e.target.value))}
                  min="1"
                  required
                  className="form-input"
                />
              </label>
            </div>
          ))}
        </div>

        <button type="button" onClick={onAddItem} className="button add-item">
          Добавить блюдо
        </button>

        <button type="submit" className="button submit-order">
          Создать заказ
        </button>
      </form>
    </div>
  );
};

export default OrderFormUI;
