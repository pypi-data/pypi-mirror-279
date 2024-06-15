import zmq

from typing import Optional, List

from embedding_server_client.error import EmbeddingClientError
from embedding_server_client.schema.base import Base, T
from embedding_server_client.schema.document import DocumentInsertionRequest, DocumentQueryRequest, DocumentQueryResponse, \
    DocumentInsertionResponse
from embedding_server_client.schema.embedding import Embedding
from embedding_server_client.schema.health_check import HealthCheck
from embedding_server_client.schema.zmq_message_header import ZmqMessageHeader, create_message_header, ZmqMessageStatus, \
    ZmqMessageType


class EmbeddingClient:
    def __init__(self, host: str):
        """
        Initializes a new instance of the BertClient.

        Args:
            host (str): The address of the BERT server to connect to.
        """
        self.host = host
        self.context = None
        self.socket = None
        self.initialize_client()

    def __del__(self):
        """
        Destructor to ensure proper cleanup. It's called when the instance is being destroyed.
        """
        self.close()

    def initialize_client(self):
        """
        Sets up the ZMQ context and socket for communication with the BERT server.
        """
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(self.host)

    def close(self):
        """
        Closes the ZMQ socket and terminates the context, releasing any system resources used.
        """
        if self.socket:
            self.socket.close()
        if self.context:
            self.context.term()

    def _send_request(self,
                      zmq_message_type: ZmqMessageType,
                      request: Optional[T] = None) -> Optional[T]:
        """
        Sends a request to the server, according to the specified message type, and waits for a response

        :param zmq_message_type: The type of the ZeroMQ message to be sent.
        :param request: The request object to be sent, if applicable.
        :return: The unpacked response if successful, or raises an exception.
        """

        message_header: ZmqMessageHeader = create_message_header(zmq_message_type)

        message_parts: List = [message_header.msgpack_pack()]
        if request:
            message_parts.append(request.msgpack_pack())

        self.socket.send_multipart(message_parts)

        try:
            resp_messages = self.socket.recv_multipart()
            if len(resp_messages) > 2:
                raise ValueError("Invalid response length")

            response_header: ZmqMessageHeader = ZmqMessageHeader.msgpack_unpack(resp_messages[0])
            if response_header.status == ZmqMessageStatus.ERROR:
                raise EmbeddingClientError(response_header)

            response_body: Base = zmq_message_type.get_associated_class
            return response_body.msgpack_unpack(resp_messages[1])
        except Exception as e:
            self.initialize_client()
            raise e

    def send_document_insertion_request(self, request: DocumentInsertionRequest) -> Optional[DocumentInsertionResponse]:
        """
        Sends an document insertion request to the BERT server and waits for a response.

        Args: request (DocumentInsertionRequest): The request object containing the data for embedding and insertion
        into vector DB.

        Returns:
            Optional[Embedding]: The embedding from the BERT server.
            None if an exception occurs during the request.

        Raises:
            ValueError: If the provided request is not of type DocumentInsertionRequest.
            Exception: For any network-related errors or data packing/unpacking issues.
        """
        if not isinstance(request, DocumentInsertionRequest):
            raise ValueError("Invalid request type provided")

        if isinstance(request.input, str):
            request.input = [request.input]

        return self._send_request(ZmqMessageType.DOCUMENT_INSERTION, request)
    
    def send_query_request(self, request: DocumentQueryRequest) -> Optional[DocumentQueryResponse]:
        """
        Sends a query request to the BERT server and waits for a response.

        Args:
            request (QueryRequest): The request object containing the query data for embedding.

        Returns:
            Optional[QueryResponse]: The chunks (list of strings) from the BERT server.
            None if an exception occurs during the request.

        Raises:
            ValueError: If the provided request is not of type QueryRequest.
            Exception: For any network-related errors or data packing/unpacking issues.
        """
        if not isinstance(request, DocumentQueryRequest):
            raise ValueError("Invalid request type provided")

        return self._send_request(ZmqMessageType.DOCUMENT_QUERY, request)

    def send_health_check_request(self) -> Optional[HealthCheck]:
        """
        Sends a HealthCheck request to the server and waits for a HealthCheck response.

        :return: A HealthCheck response or None
        """
        return self._send_request(ZmqMessageType.HEALTH_CHECK)
