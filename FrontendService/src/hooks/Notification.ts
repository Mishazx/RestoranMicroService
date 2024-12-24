import { useEffect } from "react";
import { webSocketService } from "../services/websocket";
import { Notification } from "../types/Notification";
import { useDispatch } from "react-redux";
import { addOrderMsg } from "../provider/Order/slice";


const useNotifications = (orderId: string) => {
  const dispatch = useDispatch();

  useEffect(() => {
    if (!orderId) return;

    const handleOrderUpdate = (data: Notification) => {
      dispatch(addOrderMsg({
        order_id: data.order_id,
        status: data.status,
        msg: data.message,
        date: data.timestamp
      }));
    };

    webSocketService.connectToOrder(orderId, handleOrderUpdate);

    return () => {
      webSocketService.disconnect();
    };
  }, [orderId, dispatch]);

};

export default useNotifications;