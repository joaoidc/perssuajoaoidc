from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List


@dataclass
class Turn:
    speaker: str
    text: str
    created_at: datetime


class ConversationState:
    def __init__(self) -> None:
        self.turns: List[Turn] = []

    def add_turn(self, speaker: str, text: str) -> None:
        self.turns.append(Turn(speaker=speaker, text=text.strip(), created_at=datetime.now(timezone.utc)))

    def recent_context(self, max_turns: int = 12) -> str:
        recents = self.turns[-max_turns:]
        return "\n".join(f"[{t.speaker}] {t.text}" for t in recents)

    def build_prompt(self) -> str:
        context = self.recent_context()
        return (
            "Você é um assistente de conversa em tempo real.\n"
            "Com base no diálogo, gere em português: \n"
            "1) Resposta sugerida curta\n"
            "2) 2 insights objetivos\n"
            "3) 1 follow-up inteligente\n\n"
            f"Contexto:\n{context}\n"
        )
