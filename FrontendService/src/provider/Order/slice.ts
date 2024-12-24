import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Order, OrderMsg } from '../../types/Order';

export interface OrderState {
  order: Order | null
  nowMsg: OrderMsg | null
  oldMsg: OrderMsg[]
}

const initialState: OrderState = {
  order: null,
  nowMsg: null,
  oldMsg: [],
};

const orderSlice = createSlice({
  name: 'order',
  initialState,
  reducers: {
    createOrder: (state, action: PayloadAction<Order>) => {
      state.order = action.payload;
    },
    addOrderMsg: (state, action: PayloadAction<OrderMsg>) => {
      if (state.nowMsg) {
        state.oldMsg.push(state.nowMsg);
      }
      state.nowMsg = action.payload;
      if(state.order) {
        state.order.status = action.payload.status;
      }

      const dateTime = action.payload.date;
      if (dateTime) {
        state.nowMsg.date = dateTime.split('T')[1].split('.')[0];
      }
    },
  },
});

export const { createOrder, addOrderMsg } = orderSlice.actions;
export default orderSlice.reducer;