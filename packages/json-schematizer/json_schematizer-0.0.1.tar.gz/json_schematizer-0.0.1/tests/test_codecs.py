from src.json_schematizer import codecs


def test_encode_decode():
    input_object = {"foo": "bar"}
    encoded = codecs.encode(input_object)
    output_object = codecs.decode(encoded)
    assert output_object == input_object
