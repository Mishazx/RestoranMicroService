# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: order.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'order.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0border.proto\x12\x05order\"6\n\x08MenuItem\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08quantity\x18\x03 \x01(\x05\"\x87\x01\n\x05Order\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x14\n\x0ctable_number\x18\x02 \x01(\x05\x12\x1e\n\x05items\x18\x03 \x03(\x0b\x32\x0f.order.MenuItem\x12\"\n\x06status\x18\x04 \x01(\x0e\x32\x12.order.OrderStatus\x12\x12\n\ncreated_at\x18\x05 \x01(\t\"J\n\x12\x43reateOrderRequest\x12\x14\n\x0ctable_number\x18\x01 \x01(\x05\x12\x1e\n\x05items\x18\x02 \x03(\x0b\x32\x0f.order.MenuItem\"\x95\x01\n\x13\x43reateOrderResponse\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x14\n\x0ctable_number\x18\x02 \x01(\x05\x12\x1e\n\x05items\x18\x03 \x03(\x0b\x32\x0f.order.MenuItem\x12\"\n\x06status\x18\x04 \x01(\x0e\x32\x12.order.OrderStatus\x12\x12\n\ncreated_at\x18\x05 \x01(\t\"#\n\x0fGetOrderRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\"P\n\x18UpdateOrderStatusRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\"\n\x06status\x18\x02 \x01(\x0e\x32\x12.order.OrderStatus\"-\n\x19\x43onfirmOrderPickupRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t*_\n\x0bOrderStatus\x12\x0b\n\x07PENDING\x10\x00\x12\x0b\n\x07\x43OOKING\x10\x01\x12\t\n\x05READY\x10\x02\x12\r\n\tDELIVERED\x10\x03\x12\r\n\tPICKED_UP\x10\x04\x12\r\n\tCANCELLED\x10\x05\x32\x98\x02\n\x0cOrderService\x12\x46\n\x0b\x43reateOrder\x12\x19.order.CreateOrderRequest\x1a\x1a.order.CreateOrderResponse\"\x00\x12\x32\n\x08GetOrder\x12\x16.order.GetOrderRequest\x1a\x0c.order.Order\"\x00\x12\x44\n\x11UpdateOrderStatus\x12\x1f.order.UpdateOrderStatusRequest\x1a\x0c.order.Order\"\x00\x12\x46\n\x12\x43onfirmOrderPickup\x12 .order.ConfirmOrderPickupRequest\x1a\x0c.order.Order\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ORDERSTATUS']._serialized_start=610
  _globals['_ORDERSTATUS']._serialized_end=705
  _globals['_MENUITEM']._serialized_start=22
  _globals['_MENUITEM']._serialized_end=76
  _globals['_ORDER']._serialized_start=79
  _globals['_ORDER']._serialized_end=214
  _globals['_CREATEORDERREQUEST']._serialized_start=216
  _globals['_CREATEORDERREQUEST']._serialized_end=290
  _globals['_CREATEORDERRESPONSE']._serialized_start=293
  _globals['_CREATEORDERRESPONSE']._serialized_end=442
  _globals['_GETORDERREQUEST']._serialized_start=444
  _globals['_GETORDERREQUEST']._serialized_end=479
  _globals['_UPDATEORDERSTATUSREQUEST']._serialized_start=481
  _globals['_UPDATEORDERSTATUSREQUEST']._serialized_end=561
  _globals['_CONFIRMORDERPICKUPREQUEST']._serialized_start=563
  _globals['_CONFIRMORDERPICKUPREQUEST']._serialized_end=608
  _globals['_ORDERSERVICE']._serialized_start=708
  _globals['_ORDERSERVICE']._serialized_end=988
# @@protoc_insertion_point(module_scope)
