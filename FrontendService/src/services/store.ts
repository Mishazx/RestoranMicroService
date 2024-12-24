import { combineReducers, configureStore } from '@reduxjs/toolkit';
import orderFormReducer from '../provider/OrderForm/slice';
import orderReducer from '../provider/Order/slice';

const rootReducer = combineReducers({
  order: orderReducer,
  orderForm: orderFormReducer,
});

const store = configureStore({
  reducer: rootReducer,
});

store.subscribe(() => {
  console.log('Store: ', store.getState());
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;