# Plano inicial — App Windows estilo Perssua

## Objetivo
Criar um aplicativo desktop para Windows que:
1. escute **sua voz** (microfone),
2. escute a **voz da outra pessoa** no computador (áudio do sistema),
3. transcreva em tempo real,
4. gere sugestões de resposta para **somente você ver**,
5. gere insights e follow-ups para conduzir a conversa.

---

## Arquitetura recomendada (MVP)

### 1) Captura de áudio
- **Microfone**: captura via WASAPI (dispositivo de entrada padrão).
- **Áudio da outra pessoa**: captura do áudio de saída do sistema via **WASAPI loopback**.
- Fluxos separados:
  - `speaker_you` (sua voz)
  - `speaker_other` (voz da outra pessoa)

### 2) Reconhecimento de fala (grátis)
Opções gratuitas (sem custo por minuto):
- **faster-whisper (local, open-source)**
  - Prós: boa qualidade, offline, sem custo recorrente.
  - Contras: usa CPU/GPU local.
- **whisper.cpp (local, open-source)**
  - Prós: leve, roda sem internet.
  - Contras: precisão depende do modelo e hardware.
- **Vosk (local, open-source)**
  - Prós: muito leve e rápido.
  - Contras: em geral menor qualidade para português comparado a Whisper.

**Recomendação MVP:** começar com **faster-whisper** (modelo `small` ou `medium`) e fallback para `base` em máquinas fracas.

### 3) Orquestração e contexto
Pipeline em tempo real:
1. receber chunks de áudio (ex.: 1–2s),
2. transcrever por canal,
3. identificar turno de fala (quem falou por último),
4. montar contexto recente (últimos 2–5 min + resumo),
5. enviar contexto para geração de:
   - resposta sugerida,
   - insight da conversa,
   - follow-up recomendado.

### 4) Geração de respostas (OpenAI)
- Camada de integração com API para:
  - `suggested_reply`
  - `insights`
  - `follow_up`
- Estratégia:
  - prompt curto para baixa latência,
  - janela de contexto + resumo incremental,
  - temperatura menor para objetividade.

### 5) Interface (somente você vê)
- Janela discreta com:
  - transcrição lado a lado (Você / Pessoa),
  - resposta sugerida principal,
  - 2–3 alternativas,
  - insights e follow-up.
- Atalhos:
  - pausar/retomar escuta,
  - “nova sugestão”,
  - copiar resposta.

---

## Stack técnica sugerida

### Opção A (rápida para MVP)
- **Tauri + React (UI)**
- **Rust backend** para captura de áudio (WASAPI)
- STT local via processo Python (`faster-whisper`) ou binário dedicado

### Opção B (mais simples para protótipo)
- **Electron + Node.js**
- captura via módulos nativos para WASAPI loopback
- STT local em Python separado

**Recomendação:** Tauri (menor consumo de RAM/CPU no Windows).

---

## Módulos do sistema

1. `audio-capture`
   - dispositivos, buffers, VAD (detecção de voz)
2. `stt-engine`
   - adaptador para faster-whisper / whisper.cpp / vosk
3. `conversation-state`
   - diarização básica por canal + resumo incremental
4. `llm-assistant`
   - chamadas OpenAI, templates de prompt
5. `ui-overlay`
   - painel privado para leitura rápida
6. `privacy-security`
   - controle local, retenção zero opcional, criptografia em disco

---

## Sobre “login do Codex”

Para um app de desktop em produção, o caminho robusto é usar autenticação própria do app e integrar com API da OpenAI no backend seguro do seu produto (evitando expor segredos no cliente). Para MVP local, pode iniciar com chave de API local via variáveis de ambiente e depois migrar para fluxo seguro com backend.

---

## Latência alvo (boa experiência)
- Captura + chunking: 200–500ms
- STT parcial: 500–1200ms
- Geração de sugestão: 800–1800ms
- **Total percebido:** ~1.5–3.5s

---

## Riscos e mitigação
- **Ruído/eco**: usar VAD + supressão de ruído.
- **Mistura de vozes**: separar canais (mic vs loopback) desde o início.
- **Uso de CPU alto**: escolher modelo STT dinâmico por hardware.
- **Privacidade**: modo local para STT e configuração clara de retenção.

---

## Plano de execução (2 semanas)

### Semana 1
- POC de captura dual (mic + loopback)
- STT local em tempo real (faster-whisper)
- UI mínima com transcrição ao vivo

### Semana 2
- Geração de sugestões + insights + follow-up
- atalhos de produtividade
- ajustes de latência e qualidade

---

## Próximo passo prático
1. Criar POC que só faz:
   - captura dual,
   - transcrição em 2 colunas,
   - botão “gerar resposta”.
2. Medir latência real na sua máquina.
3. Só depois evoluir para insights automáticos em tempo real.
