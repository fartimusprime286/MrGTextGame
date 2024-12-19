from datetime import datetime

from data import SharedData


class CharacterFavorability:
    _character_interactions: dict[str, list[tuple[datetime, int]]] = {}

    @staticmethod
    def favorability_exceeds_threshold(character: str, favorability: float) -> bool:
        return CharacterFavorability.favorability(character) >= favorability

    @staticmethod
    def favorability(character: str) -> int:
        interactions = CharacterFavorability._character_interactions.get(character, None)
        if interactions is None:
            interactions = []
            CharacterFavorability._character_interactions[character] = interactions

        return CharacterFavorability._compute_favorability(interactions)

    @staticmethod
    def _compute_favorability(interactions: list[tuple[datetime, int]]) -> int:
        total_favorability = 0
        for interaction in interactions:
            if SharedData.current_date >= interaction[0]:
                total_favorability += interaction[1]

        return total_favorability

    @staticmethod
    def add_favorability(character: str, favorability: int):
        interactions = CharacterFavorability._character_interactions.get(character, None)
        if interactions is None:
            interactions = []
            CharacterFavorability._character_interactions[character] = interactions

        interactions.append((SharedData.current_date, favorability))

    @staticmethod
    def remove_favorability(character: str, favorability: int):
        CharacterFavorability.add_favorability(character, -favorability)
