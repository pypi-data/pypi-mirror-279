import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings


def combine_sentences(sentences, buffer_size=1):
    """
    Combines adjacent sentences within a buffer to create new combined sentences.

    Args:
        sentences (list): List of dictionaries containing sentence information.
        buffer_size (int, optional): Size of the buffer for combining sentences. Defaults to 1.

    Returns:
        list: List of dictionaries with combined_sentence added.
    """
    try:
        for i in range(len(sentences)):
            combined_sentence = ''
            for j in range(i - buffer_size, i):
                if j >= 0:
                    combined_sentence += sentences[j]['sentence'] + ' '
            combined_sentence += sentences[i]['sentence']
            for j in range(i + 1, i + 1 + buffer_size):
                if j < len(sentences):
                    combined_sentence += ' ' + sentences[j]['sentence']
            sentences[i]['combined_sentence'] = combined_sentence
        return sentences
    except Exception as e:
        print(f"Error in combine_sentences: {e}")
        return []


def calculate_cosine_distances(sentences):
    """
    Calculates the cosine distances between combined sentences.

    Args:
        sentences (list): List of dictionaries containing combined sentences and embeddings.

    Returns:
        tuple: Pair of lists containing distances and updated sentences.
    """
    try:
        distances = []
        for i in range(len(sentences) - 1):
            embedding_current = sentences[i]['combined_sentence_embedding']
            embedding_next = sentences[i + 1]['combined_sentence_embedding']
            similarity = cosine_similarity([embedding_current], [embedding_next])[0][0]
            distance = 1 - similarity
            distances.append(distance)
            sentences[i]['distance_to_next'] = distance
        return distances, sentences
    except Exception as e:
        print(f"Error in calculate_cosine_distances: {e}")
        return [], []


def create_chunk(distances, sentences, cutoff_percentile=90):
    """
    Creates chunks of text based on cosine distance thresholds.

    Args:
        distances (list): List of cosine distances between combined sentences.
        sentences (list): List of dictionaries containing combined sentences.
        cutoff_percentile (int, optional): Percentile threshold for cosine distances. Defaults to 90.

    Returns:
        list: List of Document objects representing chunks of text.
    """
    try:
        breakpoint_distance_threshold = np.percentile(distances, cutoff_percentile)
        indices_above_thresh = [i for i, x in enumerate(distances) if x > breakpoint_distance_threshold]
        start_index = 0
        chunks = []
        for index in indices_above_thresh:
            end_index = index
            group = sentences[start_index:end_index + 1]
            combined_text = ' '.join([d['sentence'] for d in group])
            chunks.append(combined_text)
            start_index = index + 1
        if start_index < len(sentences):
            combined_text = ' '.join([d['sentence'] for d in sentences[start_index:]])
            chunks.append(combined_text)
        chunks_doc = []
        for i, chunk in enumerate(chunks):
            doc = Document(page_content=chunk, metadata={"source": f"chunk:{i}"})
            chunks_doc.append(doc)
        return chunks_doc
    except Exception as e:
        print(f"Error in create_chunk: {e}")
        return []

    
