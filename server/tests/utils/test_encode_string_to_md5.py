from src.utils import encode_string_to_md5


class TestEncodeStringToMD5:

    def test_is_encoding_valid(self):
        """
        md5 string was generated in online service by hand
        """
        string = 'haslo'
        md5_string = '207023ccb44feb4d7dadca005ce29a64'
        assert encode_string_to_md5(string) == md5_string
