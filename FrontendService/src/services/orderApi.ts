import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

export interface OrderItem {
  id?: string;
  name: string;
  quantity: string;
}

export interface CreateOrderData {
  table_number: number;
  items: OrderItem[];
}

export const orderApi = {
  confirmPickup: async (orderId: string) => {
    try {
      const response = await axios.put(`${BASE_URL}/orders/${orderId}/confirm-pickup`);
      return response.data;
    } catch (error) {
      console.error('Error confirming pickup:', error);
      throw error;
    }
  },

  createOrder: async (data: CreateOrderData) => {
    try {
      const response = await axios.post(`${BASE_URL}/orders/`, data);
      return response.data;
    } catch (error) {
      console.error('Error creating order:', error);
      throw error;
    }
  },

  getOrderDetails: async (orderId: string) => {
    try {
      const response = await axios.get(`${BASE_URL}/orders/${orderId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching order details:', error);
      throw error;
    }
  },
};
