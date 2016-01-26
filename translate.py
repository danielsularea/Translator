
import requests
import xml.etree.ElementTree as etree


class Translator:
    """
    Translates strings or string resource files from a source to a dest language.
    """
    URI = "http://api.microsofttranslator.com/V2/Http.svc/Translate"

    def __init__(self, client_id, client_secret,
                 scope="http://api.microsofttranslator.com",
                 grant_type="client_credentials"):
        """ Sets the important variables
        :param client_id:
        :param client_secret:
        :param scope:
        :param grant_type:
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.grant_type = grant_type

    def get_access_token(self):
        uri = "https://datamarket.accesscontrol.windows.net/v2/OAuth2-13"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.scope,
            "grant_type": self.grant_type
        }

        r = requests.post(uri, data=params).json()
        return r['access_token']

    def translate(self, text, from_lang, to_lang):
        params = {"from": from_lang, "to": to_lang, "text": text, "contentType": "text/plain"}

        auth_token = "Bearer" + " " + self.get_access_token()
        headers = {"Authorization": auth_token}

        r = requests.get(self.URI, params=params, headers=headers)
        r.encoding = "UTF-8"
        x = etree.fromstring(r.text)
        return x.text

    def translate_file(self, file_name, from_lang, to_lang):
        """
        Translates a typical string resource android file. Supports `string` and `string-array`
        :param file_name:
        :param from_lang:
        :param to_lang:
        :return:
        """
        tree = etree.parse(file_name)
        root = tree.getroot()

        for elem in root:
            if elem.tag == "string":
                word = self.translate(elem.text, from_lang, to_lang)

                # update element text
                elem.text = word

            elif elem.tag == "string-array":
                for item in elem:
                    word = self.translate(item.text, from_lang, to_lang)
                    item.text = word

        tree.write("strings2.xml", encoding="utf-8")

