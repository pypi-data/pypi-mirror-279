import pytest
from embedding_server_client.schema.base import Base, encoder_default, decode_with_map, json_serializer
from uuid import UUID
from datetime import datetime, timezone
from enum import Enum
from dataclasses import dataclass


class TestEnum(Enum):
    VALUE1 = 1
    VALUE2 = 2


TestEnum.__test__ = False


@dataclass
class DerivedClass(Base):
    id: UUID
    timestamp: datetime
    status: TestEnum

    @classmethod
    def decode_map(cls):
        return {'id': UUID, 'timestamp': datetime, 'status': TestEnum}


@pytest.fixture
def sample_object():
    return DerivedClass(UUID('12345678-1234-1234-1234-1234567890ab'),
                        datetime(2024, 1, 1, tzinfo=timezone.utc),
                        TestEnum.VALUE1)


def test_msgpack_serialization_deserialization(sample_object):
    packed = sample_object.msgpack_pack()
    assert packed is not None
    unpacked = DerivedClass.msgpack_unpack(packed)
    assert unpacked == sample_object


def test_json_serialization(sample_object):
    json_str = sample_object.to_json_str()
    assert '12345678-1234-1234-1234-1234567890ab' in json_str
    assert '2024-01-01T00:00:00+00:00' in json_str
    assert 'VALUE1' in json_str


def test_custom_encoders(sample_object):
    encoded_uuid = encoder_default(sample_object.id)
    assert encoded_uuid == sample_object.id.bytes

    encoded_datetime = encoder_default(sample_object.timestamp)
    assert isinstance(encoded_datetime, int)

    encoded_enum = encoder_default(sample_object.status)
    assert encoded_enum == sample_object.status.value


def test_custom_decoders(sample_object):
    decoded_obj = decode_with_map({'id': sample_object.id.bytes,
                                   'timestamp': int(sample_object.timestamp.timestamp() * 1_000_000_000),
                                   'status': sample_object.status.value},
                                  DerivedClass.decode_map())
    assert decoded_obj['id'] == sample_object.id
    assert decoded_obj['timestamp'] == sample_object.timestamp
    assert decoded_obj['status'] == sample_object.status
