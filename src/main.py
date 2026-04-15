"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


USERS = {
    "Hip-Hop Fan": {
        "genre":          "hip-hop",
        "mood":           "melancholic",
        "energy":         0.68,
        "danceability":   0.74,
        "likes_acoustic": False,
    },
    "Acoustic Low-Energy Listener": {
        "genre":          "folk",
        "mood":           "sad",
        "energy":         0.22,
        "danceability":   0.34,
        "likes_acoustic": True,
    },
    "High-Tempo EDM Listener": {
        "genre":          "electronic",
        "mood":           "euphoric",
        "energy":         0.95,
        "danceability":   0.92,
        "likes_acoustic": False,
    },
}


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 3) -> None:
    print(f"\n{'=' * 52}")
    print(f"  {label}")
    print(f"  Wants: {user_prefs['genre']} | {user_prefs['mood']} | energy {user_prefs['energy']}")
    print(f"{'=' * 52}")
    results = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(results, start=1):
        print(f"  {rank}. {song['title']} by {song['artist']}  [{score:.2f}]")
        print(f"     {explanation}")
    print()


def main() -> None:
    songs = load_songs("../data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for label, user_prefs in USERS.items():
        print_recommendations(label, user_prefs, songs, k=3)


if __name__ == "__main__":
    main()
