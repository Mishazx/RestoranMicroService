import { createSelector } from '@reduxjs/toolkit';
import { RootState } from '../../services/store';

export const selectNowMsg = (state: RootState) => state.order.nowMsg;
export const selectOldMsg = (state: RootState) => state.order.oldMsg;

export const selectOrder = (state: RootState) => state.order.order;


export const selectOldMsgList = createSelector(
  (state: RootState) => state.order.oldMsg,
  (oldMsg) => oldMsg
);
