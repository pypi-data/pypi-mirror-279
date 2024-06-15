from uuid import UUID, uuid4
from dataclasses import dataclass
from typing import Optional, Dict, Any

from polyfactory.factories import DataclassFactory

from embedding_server_client.schema import (
    DocumentInsertionRequest,
    DocumentInsertionResponse,
    DocumentQueryRequest,
    DocumentQueryResponse)

from embedding_server_client.schema.base import Base


@dataclass
class MyMapClass(Base):
    dummy: str
    key_values: Optional[Dict[str, Any]] = None

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "session": UUID,
        }


def test_map_class():
    """
    Test if the datetime encoding and decoding works correctly.
    """

    my_map_class = MyMapClass(
        dummy="test",
        key_values={"session": uuid4()}
    )

    print(my_map_class)

    packed = my_map_class.msgpack_pack()

    print(packed)

    unpacked = MyMapClass.msgpack_unpack(packed)

    print(unpacked)

    assert my_map_class == unpacked


class DocumentInsertionRequestFactory(DataclassFactory[DocumentInsertionRequest]):
    __model__ = DocumentInsertionRequest


def test_document_insertion_request_factory():
    """
    Test if the datetime encoding and decoding works correctly.
    """
    request = DocumentInsertionRequestFactory.build()

    print(request.to_json_str())

    packed = request.msgpack_pack()

    unpacked = DocumentInsertionRequest.msgpack_unpack(packed)

    print(unpacked.to_json_str())

    assert request == unpacked


class DocumentInsertionResponseFactory(DataclassFactory[DocumentInsertionResponse]):
    __model__ = DocumentInsertionRequest


def test_document_insertion_response_factory():
    """
    Test if the datetime encoding and decoding works correctly.
    """
    document_insertion_response = DocumentInsertionResponseFactory.build()

    print(document_insertion_response.to_json_str())

    packed = document_insertion_response.msgpack_pack()

    unpacked = document_insertion_response.msgpack_unpack(packed)

    print(unpacked.to_json_str())

    assert document_insertion_response == unpacked


# Duplicate for Query

class QueryRequestFactory(DataclassFactory[DocumentQueryRequest]):
    __model__ = DocumentQueryRequest


def test_query_request_factory():
    """
    Test if the datetime encoding and decoding works correctly.
    """
    query_request = QueryRequestFactory.build()
    print(query_request.to_json_str())
    packed_request = query_request.msgpack_pack()
    unpacked_request = DocumentQueryRequest.msgpack_unpack(packed_request)
    assert query_request == unpacked_request


class QueryResponseFactory(DataclassFactory[DocumentQueryResponse]):
    __model__ = DocumentQueryResponse


def test_query_response_factory():
    """
    Test if the datetime encoding and decoding works correctly.
    """
    query_response = QueryResponseFactory.build()
    print(query_response.to_json_str())
    packed_response = query_response.msgpack_pack()
    unpacked_response = DocumentQueryResponse.msgpack_unpack(packed_response)
    assert query_response == unpacked_response
