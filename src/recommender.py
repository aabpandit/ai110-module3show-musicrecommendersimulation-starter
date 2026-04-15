from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    reasons = []

    # Genre: binary match — weight 0.35
    genre_score = 1.0 if song["genre"] == user_prefs.get("genre", "") else 0.0
    if genre_score == 1.0:
        reasons.append(f"genre match ({song['genre']})")
    else:
        reasons.append(f"genre mismatch ({song['genre']} != {user_prefs.get('genre', '?')})")

    # Mood: binary match — weight 0.20
    mood_score = 1.0 if song["mood"] == user_prefs.get("mood", "") else 0.0
    if mood_score == 1.0:
        reasons.append(f"mood match ({song['mood']})")
    else:
        reasons.append(f"mood mismatch ({song['mood']})")

    # Energy: proximity score — weight 0.30
    target_energy = user_prefs.get("energy", 0.5)
    energy_score = 1.0 - abs(target_energy - song["energy"])
    reasons.append(f"energy {song['energy']:.2f} vs target {target_energy:.2f}")

    # Danceability: proximity score — weight 0.15
    target_dance = user_prefs.get("danceability", 0.5)
    dance_score = 1.0 - abs(target_dance - song["danceability"])

    score = (
        0.35 * genre_score
        + 0.20 * mood_score
        + 0.30 * energy_score
        + 0.15 * dance_score
    )

    return round(score, 4), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
