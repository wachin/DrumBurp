import unittest

from GUI import DBTheme


class TestThemeHelpers(unittest.TestCase):
    def test_normalise_theme_mode_defaults_to_auto(self):
        self.assertEqual(DBTheme.THEME_AUTO,
                         DBTheme.normalise_theme_mode("unknown"))

    def test_normalise_theme_mode_accepts_known_modes(self):
        self.assertEqual(DBTheme.THEME_DARK,
                         DBTheme.normalise_theme_mode("dark"))
        self.assertEqual(DBTheme.THEME_LIGHT,
                         DBTheme.normalise_theme_mode("LIGHT"))
        self.assertEqual(DBTheme.THEME_AUTO,
                         DBTheme.normalise_theme_mode(""))


if __name__ == "__main__":
    unittest.main()
