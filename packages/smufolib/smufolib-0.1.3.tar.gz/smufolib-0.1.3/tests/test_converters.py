"""Test converters module for SMufoLib."""

import unittest
from smufolib.converters import (
    convertMeasurement, toDecimal, toUniHex, toUniName, toKebab, toNumber)

# pylint: disable=missing-function-docstring, invalid-name


class Converters(unittest.TestCase):

    def test_convertMeasurement(self):
        self.assertEqual(convertMeasurement(
            125, convertTo='spaces', unitsPerEm=1000), 0.5)
        self.assertEqual(convertMeasurement(
            0.5, convertTo='units', unitsPerEm=1000), 125
        )

        with self.assertRaises(TypeError):
            convertMeasurement(
                (125,), convertTo='spaces', unitsPerEm=1000)
        with self.assertRaises(ValueError):
            convertMeasurement(
                125, convertTo='something else', unitsPerEm=1000)

    def test_toDecimal(self):
        for value in ('U+E00C', 'uE00C', 'uniE00C'):
            self.assertEqual(toDecimal(value), 57356)
            with self.assertRaises(ValueError):
                toDecimal(value[1:])
        with self.assertRaises(TypeError):
            toDecimal(57356)

    def test_toUniHex(self):
        self.assertEqual(toUniHex(57344), 'U+E000')
        with self.assertRaises(TypeError):
            toUniHex('57344')
        with self.assertRaises(ValueError):
            toUniHex(2000000)

    def test_toUniName(self):
        pass

    def test_toKebab(self):
        pass

    def test_toNumber(self):
        pass


# def testToUniHex():
#     for value in (57344, '57344'):
#         assert toUniHex(value) == 'U+E000'

#     with pytest.raises(ValueError):
#         toUniHex('23a45')


# def testToUniName():
#     for value in (57344, '57344', 'U+E000'):
#         assert toUniName(value, short=False) == 'uniE000'
#         assert toUniName(value, short=True) == 'uE000'

#     with pytest.raises(ValueError):
#         for value in ('U+ E000', 'U+E0G0'):
#             toUniName(value)

if __name__ == '__main__':
    unittest.main()
