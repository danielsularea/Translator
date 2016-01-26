
import unittest
from translate import Translator


class TestTranslator(unittest.TestCase):

    client_id = "<CLIENT_ID>"
    client_secret = "<CLIENT_SECRET>"

    def setUp(self):
        self.t = Translator(self.client_id, self.client_secret)

    def test_get_access_token(self):
        self.assertNotEqual(self.t.get_access_token(), "", "The access token is empty!")

    def test_translate(self):
        translated = self.t.translate("day", "en", "it")
        self.assertEqual(translated.lower(), "giorno", "The translated word is incorrect!")

        translated = self.t.translate("summer", "en", "ro")
        self.assertEqual(translated.lower(), "vara", "The translated word is incorrect!")


if __name__ == "__main__":
    unittest.main()