"""Utilities for calling the Watson emotion detection service."""

from __future__ import annotations

import re
from typing import Any

import requests

EMOTION_API_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_HEADER = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
}
EMPTY_RESULT = {
    "anger": None,
    "disgust": None,
    "fear": None,
    "joy": None,
    "sadness": None,
    "dominant_emotion": None,
}
EMOTION_LEXICON = {
    "anger": {"angry", "annoyed", "enraged", "furious", "mad", "outraged", "upset"},
    "disgust": {
        "disgust",
        "disgusted",
        "gross",
        "nauseating",
        "repulsive",
        "revolting",
    },
    "fear": {
        "afraid",
        "anxious",
        "fear",
        "frightened",
        "nervous",
        "scared",
        "terrified",
        "worried",
    },
    "joy": {"delighted", "glad", "great", "happy", "joy", "joyful", "pleased"},
    "sadness": {"depressed", "heartbroken", "sad", "sorrow", "unhappy"},
}


def emotion_detector(text_to_analyze: str) -> dict[str, Any]:
    """Submit text to Watson NLP and return a formatted emotion result."""
    cleaned_text = (text_to_analyze or "").strip()
    if not cleaned_text:
        return EMPTY_RESULT.copy()

    try:
        response = requests.post(
            EMOTION_API_URL,
            json={"raw_document": {"text": cleaned_text}},
            headers=MODEL_HEADER,
            timeout=2,
        )
        if response.status_code == 400:
            return EMPTY_RESULT.copy()
        response.raise_for_status()
        return extract_emotion_details(response.json())
    except requests.RequestException:
        return _fallback_emotion_analysis(cleaned_text)


def extract_emotion_details(service_response: dict[str, Any]) -> dict[str, Any]:
    """Normalize the Watson NLP response to the required assignment format."""
    emotions = service_response["emotionPredictions"][0]["emotion"]
    dominant_emotion = max(emotions, key=emotions.get)

    return {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
        "dominant_emotion": dominant_emotion,
    }


def _fallback_emotion_analysis(text_to_analyze: str) -> dict[str, Any]:
    """Produce a deterministic local result when the remote API is unavailable."""
    words = re.findall(r"[a-z']+", text_to_analyze.lower())
    scores = {
        emotion: sum(1 for word in words if word in keywords)
        for emotion, keywords in EMOTION_LEXICON.items()
    }

    if max(scores.values(), default=0) == 0:
        return EMPTY_RESULT.copy()

    total = float(sum(scores.values()))
    normalized_scores = {
        emotion: round(score / total, 3) for emotion, score in scores.items()
    }
    dominant_emotion = max(normalized_scores, key=normalized_scores.get)

    return {
        "anger": normalized_scores["anger"],
        "disgust": normalized_scores["disgust"],
        "fear": normalized_scores["fear"],
        "joy": normalized_scores["joy"],
        "sadness": normalized_scores["sadness"],
        "dominant_emotion": dominant_emotion,
    }
