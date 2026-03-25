# Perssua Windows Assistant (MVP inicial)

MVP executável da ideia: ouvir dois lados da conversa, transcrever e sugerir respostas/insights privados.

## O que já está implementado
- Interface desktop local em **Tkinter** com duas colunas de transcrição (`Você` e `Pessoa`).
- Estado de conversa com resumo de contexto recente.
- Botão para gerar:
  - resposta sugerida,
  - insights,
  - follow-up.
- Integração com OpenAI via HTTP nativo (sem SDK obrigatório).
- Modo fallback local quando `OPENAI_API_KEY` não está configurada.
- Simulador de conversa (demo) para validar fluxo fim a fim.

## Estrutura
- `app/main.py`: UI e orquestração.
- `app/conversation.py`: modelo de mensagem e construção de contexto.
- `app/llm.py`: cliente OpenAI + fallback local.
- `app/stt.py`: interfaces de STT (mock e stub para Vosk).
- `app/audio.py`: interfaces de captura (mock e stub Windows/WASAPI).

## Rodar
```bash
python -m app.main
```

## OpenAI (opcional)
Configure variável de ambiente:
```bash
export OPENAI_API_KEY="sua_chave"
```
No Windows (PowerShell):
```powershell
setx OPENAI_API_KEY "sua_chave"
```

## Próximos passos (milestone seguinte)
1. Implementar captura real dual no Windows com WASAPI (mic + loopback).
2. Integrar STT gratuito local (Vosk ou faster-whisper).
3. Adicionar VAD e transcrição parcial contínua.
4. Persistência local criptografada opcional.
