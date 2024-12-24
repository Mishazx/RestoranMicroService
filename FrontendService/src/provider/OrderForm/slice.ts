import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface OrderFormState {
  tableNumber: string;
  items: { id: number; name: string; quantity: number }[];
}

const initialState: OrderFormState = {
  tableNumber: '',
  items: [
    { id: 1, name: '', quantity: 1 },
  ],
};

const orderFormSlice = createSlice({
  name: 'orderForm',
  initialState,
  reducers: {
    setTableNumber(state, action: PayloadAction<string>) {
      state.tableNumber = action.payload;
    },
    addItem(state, action: PayloadAction<{ name: string; quantity: number }>) {
      const newItem = {
        ...action.payload,
        id: state.items.length ? state.items[state.items.length - 1].id + 1 : 1,
      };
      state.items.push(newItem);
    },
    changeItemName(state, action: PayloadAction<{ index: number; name: string }>) {
      state.items[action.payload.index].name = action.payload.name;
    },
    changeItemQuantity(state, action: PayloadAction<{ index: number; quantity: number }>) {
      state.items[action.payload.index].quantity = action.payload.quantity;
    },
    removeItem(state, action: PayloadAction<number>) {
      state.items.splice(action.payload, 1);
    },
    removeAllItems(state) {
      state.items = [];
    },
  },
});

export const { 
  setTableNumber, 
  addItem, 
  changeItemName, 
  changeItemQuantity, 
  removeItem, 
  removeAllItems 
} = orderFormSlice.actions;
export default orderFormSlice.reducer;