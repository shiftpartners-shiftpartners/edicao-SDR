import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from transcribe_local import transcribe


class TranscriptionContractTest(unittest.TestCase):
    def test_local_model_and_lazy_segments(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "synthetic.wav"
            source.write_bytes(b"fixture; engine mocked")
            engine = Mock()
            engine.transcribe.return_value = (iter([SimpleNamespace(start=0, end=1, text="Teste", words=[])]),
                                               SimpleNamespace(language="pt"))
            factory = Mock(return_value=engine)
            result = transcribe(source, Path(tmp), factory)
            factory.assert_called_once_with(tmp, device="cpu", compute_type="int8", local_files_only=True)
            self.assertEqual(len(result["segments"]), 1)
            self.assertTrue(result["review_required"])
