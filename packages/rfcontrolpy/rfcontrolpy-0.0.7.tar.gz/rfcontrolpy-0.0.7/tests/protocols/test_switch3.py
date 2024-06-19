# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import switch3

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestSwitch3(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = switch3.decode("01010101011001100101010101100110011001100101011002")
        self.assertDictEqual({"id": 25, "unit": 16, "state": False}, decoded)

    # def test_decode_2(self) -> None:
    #     decoded = switch3.decode('01100110011001100110010101010101010101010110010102')
    #     self.assertDictEqual({'unit': 0, 'id': 31, 'state': False}, decoded)
    #
    # def test_decode_3(self) -> None:
    #     decoded = switch3.decode('01010110010101100110011001100110010101100110011002')
    #     assert decoded == {'unit': 20, 'id': 2, 'state': True}

    def test_encode_1(self) -> None:
        encoded = switch3.encode(id=25, unit=16, state=False)
        self.assertEqual("01010101011001100101010101100110011001100101011002", encoded)

    # def test_encode_2(self) -> None:
    #     encoded = switch3.encode(message={'unit': 0, 'id': 31, 'state': False})
    #     self.assertEqual('01100110011001100110010101010101010101010110010102', encoded)
    #
    # def test_encode_3(self) -> None:
    #     encoded = switch3.encode(message={'unit': 20, 'id': 2, 'state': True})
    #     self.assertEqual('01010110010101100110011001100110010101100110011002', encoded)
