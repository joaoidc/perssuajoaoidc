from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass


@dataclass
class AssistantOutput:
    suggested_reply: str
    insights: list[str]
    follow_up: str


class OpenAILLM:
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()

    def _fallback(self, prompt: str) -> AssistantOutput:
        # Fallback local simples para manter o MVP funcional sem chave
        return AssistantOutput(
            suggested_reply="Entendi. Faz sentido — podemos alinhar os próximos passos ainda hoje.",
            insights=[
                "A conversa pede objetividade e confirmação de entendimento.",
                "Vale reduzir ambiguidade com prazo e responsabilidade.",
            ],
            follow_up="Se concordar, definimos agora dono e prazo de execução?",
        )

    def generate(self, prompt: str) -> AssistantOutput:
        if not self.api_key:
            return self._fallback(prompt)

        payload = {
            "model": self.model,
            "input": [
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": prompt}],
                }
            ],
            "temperature": 0.4,
        }

        req = urllib.request.Request(
            url="https://api.openai.com/v1/responses",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                body = json.loads(response.read().decode("utf-8"))
                text = _extract_output_text(body)
                return _parse_output(text)
        except Exception:
            return self._fallback(prompt)


def _extract_output_text(resp: dict) -> str:
    output = resp.get("output", [])
    chunks: list[str] = []
    for item in output:
        content = item.get("content", [])
        for c in content:
            if c.get("type") in {"output_text", "text"} and c.get("text"):
                chunks.append(c["text"])
    return "\n".join(chunks).strip()


def _parse_output(text: str) -> AssistantOutput:
    if not text:
        return AssistantOutput("", ["Sem insights."], "")

    lines = [ln.strip("-• \t") for ln in text.splitlines() if ln.strip()]
    suggested = lines[0] if lines else ""
    insights = lines[1:3] if len(lines) > 1 else ["Sem insights identificados."]
    follow = lines[3] if len(lines) > 3 else "Qual o próximo passo ideal?"
    return AssistantOutput(suggested, insights, follow)
