
import tempfile
import unittest
from pathlib import Path

from dupfinder import find_duplicates, file_hash, format_size


class DupFinderTests(unittest.TestCase):

    def test_identical_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            (root / "first.txt").write_text("hello world")
            (root / "second.txt").write_text("hello world")

            duplicates, examined, errors = find_duplicates(root)

            self.assertEqual(len(duplicates), 1)
            self.assertEqual(len(duplicates[0]), 2)
            self.assertEqual(examined, 2)
            self.assertEqual(errors, 0)

    def test_different_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            (root / "first.txt").write_text("hello")
            (root / "second.txt").write_text("world")

            duplicates, examined, errors = find_duplicates(root)

            self.assertEqual(duplicates, [])
            self.assertEqual(examined, 2)
            self.assertEqual(errors, 0)

    def test_nested_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "folder"
            nested.mkdir()

            (root / "first.txt").write_text("duplicate")
            (nested / "second.txt").write_text("duplicate")

            duplicates, examined, errors = find_duplicates(root)

            self.assertEqual(len(duplicates), 1)
            self.assertEqual(examined, 2)

    def test_file_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.txt"
            path.write_text("hello")

            self.assertEqual(
                file_hash(path),
                file_hash(path)
            )

    def test_format_size(self):
        self.assertEqual(format_size(100), "100.0 B")
        self.assertEqual(format_size(1024), "1.0 KB")
        self.assertEqual(format_size(1048576), "1.0 MB")


if __name__ == "__main__":
    unittest.main()
