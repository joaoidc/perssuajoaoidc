from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator


@dataclass
class AudioFrame:
    speaker: str
    pcm_bytes: bytes


class AudioCapture:
    def frames(self) -> Iterator[AudioFrame]:
        raise NotImplementedError


class MockDualAudioCapture(AudioCapture):
    def __init__(self) -> None:
        self._script = [
            AudioFrame("Pessoa", b"olha, queria atualizar o status"),
            AudioFrame("Você", b"claro, podemos revisar agora"),
            AudioFrame("Pessoa", b"qual o prazo final?"),
            AudioFrame("Você", b"entrego ate sexta"),
        ]

    def frames(self) -> Iterator[AudioFrame]:
        for item in self._script:
            yield item


class WindowsWasapiDualCapture(AudioCapture):
    """Stub para WASAPI + loopback no Windows.

    Implementação real fica para integração nativa no próximo passo.
    """

    def frames(self) -> Iterator[AudioFrame]:
        raise NotImplementedError("WindowsWasapiDualCapture ainda não implementado neste MVP.")
