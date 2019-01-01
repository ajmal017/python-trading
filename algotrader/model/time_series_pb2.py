# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: algotrader/model/time_series.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='algotrader/model/time_series.proto',
  package='algotrader.model',
  syntax='proto3',
  serialized_pb=_b('\n\"algotrader/model/time_series.proto\x12\x10\x61lgotrader.model\"\x8a\x01\n\x0eTimeSeriesItem\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12\x38\n\x04\x64\x61ta\x18\x02 \x03(\x0b\x32*.algotrader.model.TimeSeriesItem.DataEntry\x1a+\n\tDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x01:\x02\x38\x01\"W\n\x15TimeSeriesUpdateEvent\x12\x0e\n\x06source\x18\x01 \x01(\t\x12.\n\x04item\x18\x02 \x01(\x0b\x32 .algotrader.model.TimeSeriesItem\"\xa8\x03\n\nTimeSeries\x12\x11\n\tseries_id\x18\x01 \x01(\t\x12\x12\n\nseries_cls\x18\x02 \x01(\t\x12\x0c\n\x04keys\x18\x03 \x03(\t\x12\x0c\n\x04\x64\x65sc\x18\x04 \x01(\t\x12\x32\n\x06inputs\x18\x05 \x03(\x0b\x32\".algotrader.model.TimeSeries.Input\x12\x1a\n\x12\x64\x65\x66\x61ult_output_key\x18\x06 \x01(\t\x12\x1d\n\x15missing_value_replace\x18\x07 \x01(\x01\x12\x12\n\nstart_time\x18\x08 \x01(\x03\x12\x10\n\x08\x65nd_time\x18\t \x01(\x03\x12/\n\x05items\x18\n \x03(\x0b\x32 .algotrader.model.TimeSeriesItem\x12:\n\x07\x63onfigs\x18\x0b \x03(\x0b\x32).algotrader.model.TimeSeries.ConfigsEntry\x1a%\n\x05Input\x12\x0e\n\x06source\x18\x01 \x01(\t\x12\x0c\n\x04keys\x18\x02 \x03(\t\x1a.\n\x0c\x43onfigsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_TIMESERIESITEM_DATAENTRY = _descriptor.Descriptor(
  name='DataEntry',
  full_name='algotrader.model.TimeSeriesItem.DataEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='algotrader.model.TimeSeriesItem.DataEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='algotrader.model.TimeSeriesItem.DataEntry.value', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=152,
  serialized_end=195,
)

_TIMESERIESITEM = _descriptor.Descriptor(
  name='TimeSeriesItem',
  full_name='algotrader.model.TimeSeriesItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='algotrader.model.TimeSeriesItem.timestamp', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='algotrader.model.TimeSeriesItem.data', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_TIMESERIESITEM_DATAENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=57,
  serialized_end=195,
)


_TIMESERIESUPDATEEVENT = _descriptor.Descriptor(
  name='TimeSeriesUpdateEvent',
  full_name='algotrader.model.TimeSeriesUpdateEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='source', full_name='algotrader.model.TimeSeriesUpdateEvent.source', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='item', full_name='algotrader.model.TimeSeriesUpdateEvent.item', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=197,
  serialized_end=284,
)


_TIMESERIES_INPUT = _descriptor.Descriptor(
  name='Input',
  full_name='algotrader.model.TimeSeries.Input',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='source', full_name='algotrader.model.TimeSeries.Input.source', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='keys', full_name='algotrader.model.TimeSeries.Input.keys', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=626,
  serialized_end=663,
)

_TIMESERIES_CONFIGSENTRY = _descriptor.Descriptor(
  name='ConfigsEntry',
  full_name='algotrader.model.TimeSeries.ConfigsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='algotrader.model.TimeSeries.ConfigsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='algotrader.model.TimeSeries.ConfigsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=665,
  serialized_end=711,
)

_TIMESERIES = _descriptor.Descriptor(
  name='TimeSeries',
  full_name='algotrader.model.TimeSeries',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='series_id', full_name='algotrader.model.TimeSeries.series_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='series_cls', full_name='algotrader.model.TimeSeries.series_cls', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='keys', full_name='algotrader.model.TimeSeries.keys', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='desc', full_name='algotrader.model.TimeSeries.desc', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='inputs', full_name='algotrader.model.TimeSeries.inputs', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_output_key', full_name='algotrader.model.TimeSeries.default_output_key', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='missing_value_replace', full_name='algotrader.model.TimeSeries.missing_value_replace', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='start_time', full_name='algotrader.model.TimeSeries.start_time', index=7,
      number=8, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='end_time', full_name='algotrader.model.TimeSeries.end_time', index=8,
      number=9, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='items', full_name='algotrader.model.TimeSeries.items', index=9,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='configs', full_name='algotrader.model.TimeSeries.configs', index=10,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_TIMESERIES_INPUT, _TIMESERIES_CONFIGSENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=287,
  serialized_end=711,
)

_TIMESERIESITEM_DATAENTRY.containing_type = _TIMESERIESITEM
_TIMESERIESITEM.fields_by_name['data'].message_type = _TIMESERIESITEM_DATAENTRY
_TIMESERIESUPDATEEVENT.fields_by_name['item'].message_type = _TIMESERIESITEM
_TIMESERIES_INPUT.containing_type = _TIMESERIES
_TIMESERIES_CONFIGSENTRY.containing_type = _TIMESERIES
_TIMESERIES.fields_by_name['inputs'].message_type = _TIMESERIES_INPUT
_TIMESERIES.fields_by_name['items'].message_type = _TIMESERIESITEM
_TIMESERIES.fields_by_name['configs'].message_type = _TIMESERIES_CONFIGSENTRY
DESCRIPTOR.message_types_by_name['TimeSeriesItem'] = _TIMESERIESITEM
DESCRIPTOR.message_types_by_name['TimeSeriesUpdateEvent'] = _TIMESERIESUPDATEEVENT
DESCRIPTOR.message_types_by_name['TimeSeries'] = _TIMESERIES

TimeSeriesItem = _reflection.GeneratedProtocolMessageType('TimeSeriesItem', (_message.Message,), dict(

  DataEntry = _reflection.GeneratedProtocolMessageType('DataEntry', (_message.Message,), dict(
    DESCRIPTOR = _TIMESERIESITEM_DATAENTRY,
    __module__ = 'algotrader.model.time_series_pb2'
    # @@protoc_insertion_point(class_scope:algotrader.model.TimeSeriesItem.DataEntry)
    ))
  ,
  DESCRIPTOR = _TIMESERIESITEM,
  __module__ = 'algotrader.model.time_series_pb2'
  # @@protoc_insertion_point(class_scope:algotrader.model.TimeSeriesItem)
  ))
_sym_db.RegisterMessage(TimeSeriesItem)
_sym_db.RegisterMessage(TimeSeriesItem.DataEntry)

TimeSeriesUpdateEvent = _reflection.GeneratedProtocolMessageType('TimeSeriesUpdateEvent', (_message.Message,), dict(
  DESCRIPTOR = _TIMESERIESUPDATEEVENT,
  __module__ = 'algotrader.model.time_series_pb2'
  # @@protoc_insertion_point(class_scope:algotrader.model.TimeSeriesUpdateEvent)
  ))
_sym_db.RegisterMessage(TimeSeriesUpdateEvent)

TimeSeries = _reflection.GeneratedProtocolMessageType('TimeSeries', (_message.Message,), dict(

  Input = _reflection.GeneratedProtocolMessageType('Input', (_message.Message,), dict(
    DESCRIPTOR = _TIMESERIES_INPUT,
    __module__ = 'algotrader.model.time_series_pb2'
    # @@protoc_insertion_point(class_scope:algotrader.model.TimeSeries.Input)
    ))
  ,

  ConfigsEntry = _reflection.GeneratedProtocolMessageType('ConfigsEntry', (_message.Message,), dict(
    DESCRIPTOR = _TIMESERIES_CONFIGSENTRY,
    __module__ = 'algotrader.model.time_series_pb2'
    # @@protoc_insertion_point(class_scope:algotrader.model.TimeSeries.ConfigsEntry)
    ))
  ,
  DESCRIPTOR = _TIMESERIES,
  __module__ = 'algotrader.model.time_series_pb2'
  # @@protoc_insertion_point(class_scope:algotrader.model.TimeSeries)
  ))
_sym_db.RegisterMessage(TimeSeries)
_sym_db.RegisterMessage(TimeSeries.Input)
_sym_db.RegisterMessage(TimeSeries.ConfigsEntry)


_TIMESERIESITEM_DATAENTRY.has_options = True
_TIMESERIESITEM_DATAENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
_TIMESERIES_CONFIGSENTRY.has_options = True
_TIMESERIES_CONFIGSENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
# @@protoc_insertion_point(module_scope)
