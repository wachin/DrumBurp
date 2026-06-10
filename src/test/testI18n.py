import os
import tempfile
import unittest
from unittest import mock

from i18n import i18n


class TestI18nHelpers(unittest.TestCase):
    def test_pick_translation_prefers_newer_ts(self):
        qm_path = os.path.join("translations", "drumburp_zh_TW.qm")
        ts_path = os.path.join("translations", "drumburp_zh_TW.ts")

        def fake_exists(path):
            return path in (qm_path, ts_path)

        def fake_getmtime(path):
            if path == qm_path:
                return 10
            if path == ts_path:
                return 20
            raise AssertionError(path)

        with mock.patch.object(i18n, "_translation_paths",
                               return_value=(qm_path, ts_path)):
            with mock.patch("i18n.i18n.os.path.exists",
                            side_effect=fake_exists):
                with mock.patch("i18n.i18n.os.path.getmtime",
                                side_effect=fake_getmtime):
                    language, kind, path = i18n._pick_translation(["zh_TW"])

        self.assertEqual(("zh_TW", "ts", ts_path), (language, kind, path))

    def test_ts_translator_reads_messages(self):
        with tempfile.NamedTemporaryFile("w", suffix=".ts",
                                         encoding="utf-8",
                                         delete=False) as ts_file:
            ts_file.write("""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="zh_TW">
  <context>
    <name>dbStartup</name>
    <message>
      <source>Welcome to DrumBurp</source>
      <translation>歡迎使用 DrumBurp</translation>
    </message>
  </context>
</TS>
""")
            ts_path = ts_file.name

        try:
            translator = i18n._TsTranslator(ts_path)
            self.assertEqual(
                "歡迎使用 DrumBurp",
                translator.translate("dbStartup", "Welcome to DrumBurp"))
        finally:
            os.unlink(ts_path)


if __name__ == "__main__":
    unittest.main()
