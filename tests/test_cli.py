from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


def cli(*args):
    return subprocess.run([sys.executable, "line_loom.py", *args], text=True, capture_output=True)


class LineLoomTests(unittest.TestCase):
    def test_mixed_endings_preserve_bom_and_unterminated_last_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "mixed.txt"
            target = Path(tmp) / "normalized.txt"
            source.write_bytes(b"\xef\xbb\xbfalpha\r\nbeta\rgamma\nend")
            inspection = cli(source)
            self.assertEqual(inspection.returncode, 0, inspection.stderr)
            self.assertIn("Final line ending: no", inspection.stdout)
            result = cli(source, "--to", "crlf", "-o", target)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(target.read_bytes(), b"\xef\xbb\xbfalpha\r\nbeta\r\ngamma\r\nend")

    def test_existing_destination_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source.txt"
            target = Path(tmp) / "existing.txt"
            source.write_bytes(b"track\r\n")
            target.write_bytes(b"preserve")
            result = cli(source, "--to", "lf", "-o", target)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(target.read_bytes(), b"preserve")
