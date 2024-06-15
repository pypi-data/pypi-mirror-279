import uuid
from datetime import datetime, timezone

from embedding_server_client.schema.zmq_message_header import ZmqMessageHeader, ZmqMessageType


def test_msgpack_zmq_message_header():
    message_header = ZmqMessageHeader(
        zmq_message_id=uuid.uuid4(),
        message_type=ZmqMessageType.DOCUMENT_INSERTION,
        request_ts=datetime.now(tz=timezone.utc)
    )
    print(message_header.to_json_str())

    packed = message_header.msgpack_pack()

    message_header_unpacked = ZmqMessageHeader.msgpack_unpack(packed)

    assert message_header == message_header_unpacked

    print(message_header_unpacked.to_json_str())