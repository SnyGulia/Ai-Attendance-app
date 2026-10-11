from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


def get_voice_embedding(audio_bytes):
    # Audio bytes -> 256-number voice embedding
    try:
        encoder = load_voice_encoder()

        # Read audio at 16 kHz
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)

        # Normalize volume, trim silence
        wav = preprocess_wav(audio)

        # Create embedding
        embedding = encoder.embed_utterance(wav)

        # List so it can be saved as JSON
        return embedding.tolist()

    except Exception as e:
        st.error(f"Voice recog error: {e}")
        return None


def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    # Find the closest student voice
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    best_sid = None
    best_score = -1

    for sid, stored_embedding in candidates_dict.items():
        # Skip students with no voice saved
        if stored_embedding:
            # Similarity score (dot product)
            similarity = np.dot(new_embedding, stored_embedding)

            # Keep the best match
            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    # Match only if the score passes the threshold
    if best_score >= threshold:
        return best_sid, best_score

    # No match found
    return None, best_score


def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)

        identified_results = {}

        for start, end in segments:
            # Skip very short clips
            if (end - start) < sr * 0.5:
                continue
            segment_audio = audio[start:end]

            # Clean audio
            wav = preprocess_wav(segment_audio)
            # Voice embedding
            embedding = encoder.embed_utterance(wav).tolist()

            # Find who spoke
            sid, score = identify_speaker(
                embedding, candidates_dict, threshold)

            # Keep best score per student
            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score
        return identified_results
    except Exception as e:
        st.error("Bulk Process Error")
        return {}
