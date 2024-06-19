from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_openai import OpenAIEmbeddings
from .text_utils import *
import re
from langchain.docstore.document import Document
from .library_exceptions import (
    TextTooShort,
    SentenceWindow,
    OverlapError,
    InvalidChunkSize,
    InvalidChunkOverlap,
    InvalidSentenceBufferWindow,
)


def isValid(input_text, chunk_size, chunk_overlap, sentence_buffer_window):
    """
    Validates the input text and chunking parameters.

    Args:
        input_text (str): The input text to be chunked.
        chunk_size (int): The size of each chunk.
        chunk_overlap (int): The overlap between chunks.
        sentence_buffer_window (int): The buffer window size for sentence combining.

    Raises:
        InvalidChunkSize: Raised if the chunk size is invalid.
        TextTooShort: Raised if the input text is too short.
        InvalidChunkOverlap: Raised if the chunk overlap is invalid.
        OverlapError: Raised if the chunk overlap exceeds the chunk size.
        InvalidSentenceBufferWindow: Raised if the sentence buffer window is invalid.
        SentenceWindow: Raised if the sentence buffer window is too small.
    """
    sentences = list(input_text.split("."))

    if chunk_size <= 0:
        raise InvalidChunkSize()

    if len(input_text) < chunk_size:
        raise TextTooShort()

    if chunk_overlap < 0:
        raise InvalidChunkOverlap()

    if chunk_size < chunk_overlap:
        raise OverlapError()

    if sentence_buffer_window < 0:
        raise InvalidSentenceBufferWindow()

    if abs(len(sentences) * 0.1) <= sentence_buffer_window:
        raise SentenceWindow()


class TextChunker:
    """
    Class for chunking text into smaller chunks using different strategies.
    """
    def __init__(self, clean_text: str, parent_instance=None) -> None:
        self.clean_text = clean_text
        self.parent_instance = parent_instance
        isValid(
            clean_text,
            parent_instance.chunk_size,
            parent_instance.chunk_overlap,
            parent_instance.sentence_buffer_window,
        )

    def SimpleTextSplitter(self):
        """
        Splits the input text into chunks using CharacterTextSplitter.

        Returns:
            tuple: A tuple containing a list of chunks and a dictionary of chunking parameters.
        """
        try:
            params = self.parent_instance.reset_params()
            text_splitter = CharacterTextSplitter(
                chunk_size=self.parent_instance.chunk_size,
                chunk_overlap=self.parent_instance.chunk_overlap,
                separator=self.parent_instance.separator,
                strip_whitespace=self.parent_instance.strip_whitespace,
            )

            split_text = text_splitter.create_documents([self.clean_text])

            params["chunk_size"] = self.parent_instance.chunk_size
            params["chunk_overlap"] = self.parent_instance.chunk_overlap
            params["separator"] = self.parent_instance.separator
            params["strip_whitespace"] = self.parent_instance.strip_whitespace
            return split_text, params
        except Exception as e:
            raise "Error occurred during text splitting: {}".format(str(e))

    def RecursiveCharTextSplitter(self):
        """
        Splits the input text into chunks using RecursiveCharacterTextSplitter.

        Returns:
            tuple: A tuple containing a list of chunks and a dictionary of chunking parameters.
        """
        try:
            params = self.parent_instance.reset_params()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.parent_instance.chunk_size,
                chunk_overlap=self.parent_instance.chunk_overlap,
            )
            split_text = text_splitter.create_documents([self.clean_text])
            params["chunk_size"] = self.parent_instance.chunk_size
            params["chunk_overlap"] = self.parent_instance.chunk_overlap
            return split_text, params
        except Exception as e:
            raise "Error occurred during text splitting: {}".format(str(e))

    def SentenseWindowSplitter(self):
        """
        Splits the input text into chunks based on the sentence window buffer.

        Returns:
            tuple: A tuple containing a list of chunks and a dictionary of chunking parameters.
        """
        try:

            params = self.parent_instance.reset_params()
            input_text = str(self.clean_text)
            single_sentences_list = re.split(r"(?<=[.?!])\s+", input_text)
            sentences = [
                {"sentence": x, "index": i} for i, x in enumerate(single_sentences_list)
            ]
            sentences = combine_sentences(
                sentences, buffer_size=self.parent_instance.sentence_buffer_window
            )
            chunks = []
            for i, sentence in enumerate(sentences):
                doc = Document(
                    page_content=sentence["combined_sentence"],
                    metadata={"source": f"chunk:{i}"},
                )
                chunks.append(doc)

            params["sentence_buffer_window"] = (
                self.parent_instance.sentence_buffer_window
            )
            return chunks, params
        except Exception as e:
            raise "Error occurred during text splitting: {}".format(str(e))

    def SemanticSentenseSplitter(self):
        """
        Splits the input text into semantically similar sentences using OpenAI API.

        Returns:
            tuple: A tuple containing a list of chunks and a dictionary of chunking parameters.
        """
        try:
            params = self.parent_instance.reset_params()
            input_text = str(self.clean_text)
            single_sentences_list = re.split(r"(?<=[.?!])\s+", input_text)
            sentences = [
                {"sentence": x, "index": i} for i, x in enumerate(single_sentences_list)
            ]
            sentences = combine_sentences(
                sentences, buffer_size=self.parent_instance.sentence_buffer_window
            )
            oaiembeds = OpenAIEmbeddings()
            embeddings = oaiembeds.embed_documents(
                [x["combined_sentence"] for x in sentences]
            )
            for i, sentence in enumerate(sentences):
                sentence["combined_sentence_embedding"] = embeddings[i]
            distances, sentences = calculate_cosine_distances(sentences)
            chunks = create_chunk(
                distances,
                sentences,
                cutoff_percentile=self.parent_instance.sentence_cutoff_percentile,
            )

            params["sentence_buffer_window"] = (
                self.parent_instance.sentence_buffer_window
            )
            params["sentence_cutoff_percentile"] = (
                self.parent_instance.sentence_cutoff_percentile
            )

            return chunks, params
        except Exception as e:
            raise "Error occurred during text splitting: {}".format(str(e))
