class WebSocketService {
  private socket: WebSocket | null = null;
  private orderSocket: WebSocket | null = null;

  // Подключение к общему WebSocket для всех заказов
  connectToAllOrders(onMessage: (data: any) => void) {
    this.socket = new WebSocket('ws://localhost:8080/ws/orders');
    
    this.socket.onopen = () => {
      console.log('Connected to orders websocket');
    };

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    this.socket.onclose = () => {
      console.log('Disconnected from orders websocket');
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  // Подключение к WebSocket для конкретного заказа
  connectToOrder(orderId: string, onMessage: (data: any) => void) {
    this.orderSocket = new WebSocket(`ws://localhost:8080/ws/orders/${orderId}`);
    
    this.orderSocket.onopen = () => {
      console.log(`Connected to order ${orderId} websocket`);
    };

    this.orderSocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    this.orderSocket.onclose = () => {
      console.log(`Disconnected from order ${orderId} websocket`);
    };

    this.orderSocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  // Отключение от всех WebSocket соединений
  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
    if (this.orderSocket) {
      this.orderSocket.close();
      this.orderSocket = null;
    }
  }
}

export const webSocketService = new WebSocketService();

