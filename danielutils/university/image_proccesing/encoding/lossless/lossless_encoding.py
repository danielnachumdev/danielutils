from ..encoding import Encoding


class LosslessEncoding(Encoding):
    encoding_type: Encoding.EncodingType = Encoding.EncodingType.LOSSLESS


___all___ = [
    'LosslessEncoding',
]
