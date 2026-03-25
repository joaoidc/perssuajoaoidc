from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TranscriptChunk:
    speaker: str
    text: str


class STTEngine:
    def transcribe(self, pcm_bytes: bytes, speaker: str) -> TranscriptChunk:
        raise NotImplementedError


class MockSTT(STTEngine):
    def transcribe(self, pcm_bytes: bytes, speaker: str) -> TranscriptChunk:
        fake = "Trecho de fala reconhecido" if pcm_bytes else ""
        return TranscriptChunk(speaker=speaker, text=fake)


class VoskSTT(STTEngine):
    """Stub para integração com Vosk (gratuito/local).

    Implementação real prevista no próximo milestone.
    """

    def transcribe(self, pcm_bytes: bytes, speaker: str) -> TranscriptChunk:
        raise NotImplementedError("VoskSTT ainda não implementado no MVP inicial.")
