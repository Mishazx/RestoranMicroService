export interface Order {
  order_id: string;
  table_number: number;
  items: { name: string; quantity: number; status: string }[];
  name: string;
  quantity: number;
  status: string;
  created_at: string;
}

export interface OrderMsg {
  order_id: string;
  status: string;
  msg: string;
  date: string;
}