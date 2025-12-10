import unittest
from conf2yaml.parser import compile_to_value,ParseError
from conf2yaml.lexer import LexError
from conf2yaml.yaml_emit import emit_yaml

class TestLanguage(unittest.TestCase):
    def test_number_root(self):
        self.assertEqual(compile_to_value("42"),42)

    def test_list_root(self):
        self.assertEqual(compile_to_value("(list 1 2 3)"),[1,2,3])

    def test_nested_list(self):
        self.assertEqual(compile_to_value("(list 1 (list 2 3) 4)"),[1,[2,3],4])

    def test_comments(self):
        src="REM a\nlet x = 1 REM b\n(list !{x} 2) REM c\n"
        self.assertEqual(compile_to_value(src),[1,2])

    def test_let_and_ref_number(self):
        src="let a = 7\n(list !{a} 8)"
        self.assertEqual(compile_to_value(src),[7,8])

    def test_let_and_ref_list(self):
        src="let arr = (list 1 2)\n(list !{arr} 3)"
        self.assertEqual(compile_to_value(src),[[1,2],3])

    def test_ref_unknown(self):
        with self.assertRaises(ParseError):
            compile_to_value("(list !{x})")

    def test_invalid_identifier(self):
        with self.assertRaises(LexError):
            compile_to_value("let A = 1\n(list 1)")

    def test_missing_list_keyword(self):
        with self.assertRaises(ParseError):
            compile_to_value("( 1 2 )")

    def test_missing_rparen(self):
        with self.assertRaises(ParseError):
            compile_to_value("(list 1 2")

    def test_missing_equal(self):
        with self.assertRaises(ParseError):
            compile_to_value("let a 1\n(list 2)")

    def test_extra_tokens_after_root(self):
        with self.assertRaises(ParseError):
            compile_to_value("(list 1)\n(list 2)")

    def test_yaml_emit(self):
        self.assertEqual(
            emit_yaml([1,[2,3],4]).strip(),
            "- 1\n-\n  - 2\n  - 3\n- 4"
        )

if __name__=="__main__":
    unittest.main()
