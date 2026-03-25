import unittest

from app.conversation import ConversationState


class ConversationStateTests(unittest.TestCase):
    def test_build_prompt_contains_recent_turns(self) -> None:
        state = ConversationState()
        state.add_turn("Pessoa", "Oi, você pode me ajudar?")
        state.add_turn("Você", "Claro, vamos lá.")

        prompt = state.build_prompt()

        self.assertIn("[Pessoa] Oi, você pode me ajudar?", prompt)
        self.assertIn("[Você] Claro, vamos lá.", prompt)
        self.assertIn("Resposta sugerida", prompt)


if __name__ == "__main__":
    unittest.main()
