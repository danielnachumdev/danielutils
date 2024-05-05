from ..encoding import Encoding


class LossyEncoding(Encoding):
    encoding_type: Encoding.EncodingType = Encoding.EncodingType.LOSSY


___all___ = [
    'LossyEncoding',
]
