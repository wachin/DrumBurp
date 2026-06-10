import unittest
from unittest import mock

from i18n import i18n


class TestI18nHelpers(unittest.TestCase):
    def test_pick_translation_prefers_first_available_qm(self):
        qm_path = "translations\\drumburp_zh_TW.qm"

        def fake_exists(path):
            return path == qm_path

        with mock.patch.object(i18n, "_translation_path",
                               return_value=qm_path):
            with mock.patch("i18n.i18n.os.path.exists",
                            side_effect=fake_exists):
                language, path = i18n._pick_translation(["zh_TW"])

        self.assertEqual(("zh_TW", qm_path), (language, path))


if __name__ == "__main__":
    unittest.main()
