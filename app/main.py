from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from app.conversation import ConversationState
from app.llm import OpenAILLM


class AssistantApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Perssua Assistant MVP")
        self.root.geometry("980x620")

        self.state = ConversationState()
        self.llm = OpenAILLM()

        self._build_ui()

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        cols = ttk.Frame(main)
        cols.pack(fill=tk.BOTH, expand=True)

        left = ttk.LabelFrame(cols, text="Você")
        right = ttk.LabelFrame(cols, text="Pessoa")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0))

        self.you_text = tk.Text(left, wrap=tk.WORD, height=15)
        self.other_text = tk.Text(right, wrap=tk.WORD, height=15)
        self.you_text.pack(fill=tk.BOTH, expand=True)
        self.other_text.pack(fill=tk.BOTH, expand=True)

        input_row = ttk.Frame(main)
        input_row.pack(fill=tk.X, pady=8)

        self.entry = ttk.Entry(input_row)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.speaker_var = tk.StringVar(value="Você")
        speaker_box = ttk.Combobox(input_row, textvariable=self.speaker_var, values=["Você", "Pessoa"], width=10)
        speaker_box.pack(side=tk.LEFT, padx=6)
        ttk.Button(input_row, text="Adicionar fala", command=self.add_turn).pack(side=tk.LEFT)
        ttk.Button(input_row, text="Rodar demo", command=self.run_demo).pack(side=tk.LEFT, padx=6)

        out = ttk.LabelFrame(main, text="Sugestões privadas")
        out.pack(fill=tk.BOTH, expand=True)
        self.output_text = tk.Text(out, wrap=tk.WORD, height=14)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        actions = ttk.Frame(main)
        actions.pack(fill=tk.X, pady=8)
        ttk.Button(actions, text="Gerar resposta + insights", command=self.generate).pack(side=tk.LEFT)

    def add_turn(self) -> None:
        txt = self.entry.get().strip()
        if not txt:
            return
        speaker = self.speaker_var.get().strip() or "Você"
        self.state.add_turn(speaker, txt)

        box = self.you_text if speaker == "Você" else self.other_text
        box.insert(tk.END, f"{txt}\n")
        box.see(tk.END)
        self.entry.delete(0, tk.END)

    def run_demo(self) -> None:
        script = [
            ("Pessoa", "Tenho uma dúvida sobre o prazo do projeto."),
            ("Você", "Perfeito, posso te atualizar agora."),
            ("Pessoa", "Conseguimos fechar hoje?"),
        ]
        for speaker, txt in script:
            self.state.add_turn(speaker, txt)
            box = self.you_text if speaker == "Você" else self.other_text
            box.insert(tk.END, f"{txt}\n")

    def generate(self) -> None:
        prompt = self.state.build_prompt()
        result = self.llm.generate(prompt)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(
            tk.END,
            "Resposta sugerida:\n"
            f"{result.suggested_reply}\n\n"
            "Insights:\n"
            f"- {result.insights[0]}\n"
            f"- {result.insights[1] if len(result.insights) > 1 else ''}\n\n"
            "Follow-up:\n"
            f"{result.follow_up}\n",
        )


def main() -> None:
    root = tk.Tk()
    AssistantApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
