# NOTE: These pydantic models are defined in multiple places
# packages/egp-ml-proxy/types_chatcompletion.py
# packages/egp-api-backend/egp_api_backend/server/internal/applications/models/chat_completion_models.py
# packages/egp-py/sdk/models/completions/chat_completion_models.py
# Please make sure that any changes you've made are reflected in these places!


from typing import List, Literal, Optional

from pydantic import BaseModel


class ChatCompletionMessage(BaseModel):
    """
    Represents a message in a chat completion process.

    Attributes:
        role (Literal["model", "user", "system"]): The role of the message sender.
        text (str): The content of the message.
        UUID (str): The unique identifier of the message.
    """

    role: Literal["model", "user", "system"]
    text: str
    UUID: str


class ContextDocument(BaseModel):
    """
    Represents a document related to the chat context.

    Attributes:
        document_id (str): The unique identifier of the document.
        title (Optional[str]): The title of the document.
        description (Optional[str]): The description of the document.
        attachment_url (Optional[str]): The URL of the original document (e.g., PDF).
        metadata (Optional[dict]): Additional metadata for the document.
    """

    document_id: str
    title: Optional[str]
    description: Optional[str]
    attachment_url: Optional[str]
    metadata: Optional[dict]


class RetrievedContextItem(BaseModel):
    """
    Represents an item retrieved in the context of a chat.

    Attributes:
        id (str): The unique identifier of the retrieved context item.
        type (Literal["context_chunk", "document", "sql", "external_url", "other"]): The type of the retrieved item.
        content (str): The content of the retrieved item.
        source_url (Optional[str]): The URL of the resource from which the chunk was drawn.
        page_number (Optional[str]): The page number where the content was found.
        context_document (Optional[ContextDocument]): The related context document.
        score (Optional[float]): The relevance score of the retrieved item.
    """

    id: str
    type: Literal["context_chunk", "document", "sql", "external_url", "other"]
    content: str
    source_url: Optional[str]
    page_number: Optional[str]
    context_document: Optional[ContextDocument]
    score: Optional[float]


class ResponseStatus(BaseModel):
    """
    Represents the status of a response in the chat completion process.

    Attributes:
        request_id (str): The unique identifier of the request.
        timestamp (str): The timestamp of the response in ISO format.
        status (Literal["in-progress", "success", "error"]): The status of the response.
        chunk_number (Optional[int]): The chunk number of the response, if streaming is supported.
        error_message (Optional[str]): The error message, if any.
    """

    request_id: str
    timestamp: str  # ISO-formatted datetime string
    status: Literal["in-progress", "success", "error"]
    chunk_number: Optional[int]
    error_message: Optional[str]


class ChatCompletionRequest(BaseModel):
    """
    Represents a request for chat completion.

    Attributes:
        id (str): The unique identifier of the request.
        version (str): The version of the request schema.
        messages (List[ChatCompletionMessage]): A list of messages in the chat.
        app_config (Optional[dict]): The application configuration.
        metadata (Optional[dict]): Additional metadata for the request.
    """

    id: str
    version: str
    messages: List[ChatCompletionMessage]
    app_config: Optional[dict]
    metadata: Optional[dict]


class ChatCompletionResponse(BaseModel):
    """
    Represents a response from a chat completion request.

    Attributes:
        version (str): The version of the response schema.
        response (ChatCompletionMessage): The response message.
        retrieved_context (List[RetrievedContextItem]): A list of retrieved context chunks and citations.
        additional_items (List[RetrievedContextItem]): A list of additional retrieved items.
        metadata (Optional[dict]): Additional metadata for the response.
        response_status (ResponseStatus): The status of the response.
    """

    version: str
    response: ChatCompletionMessage
    retrieved_context: List[RetrievedContextItem]
    additional_items: List[RetrievedContextItem]
    metadata: Optional[dict]
    response_status: ResponseStatus
