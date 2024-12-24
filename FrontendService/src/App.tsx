import React, { useState } from 'react';
import './App.css'
import OrderForm from './components/OrderForm/OrderForm';
import Notifications from './components/Notifications';

function App() {
  const [orderId, setOrderId] = useState<string>('');

  return (
    <div className="App">
      <main className="container">
          <OrderForm setOrderId={setOrderId} />
          <Notifications orderId={orderId} />
      </main>
    </div>
  );
}

export default App;