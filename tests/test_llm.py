import unittest

from app.llm import _parse_output


class ParseOutputTests(unittest.TestCase):
    def test_parse_output_lines(self) -> None:
        raw = "Resposta curta\nInsight 1\nInsight 2\nFollow up"
        out = _parse_output(raw)
        self.assertEqual(out.suggested_reply, "Resposta curta")
        self.assertEqual(out.insights, ["Insight 1", "Insight 2"])
        self.assertEqual(out.follow_up, "Follow up")


if __name__ == "__main__":
    unittest.main()
