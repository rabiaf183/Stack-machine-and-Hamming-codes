import unittest
from hamming_code import HammingCode
from hamming_code import HCResult
class TestHammingCode(unittest.TestCase):
    def test_instance(self):
    
        hamming = HammingCode()
    
        
    def test_decode_valid(self):
        """ Essential: Test method decode() with VALID input """
        hamming = HammingCode()
        encoding= hamming.encode((1,0,1,1,0,1))
        decoding,Tag = hamming.decode((1,0,1,1,0,1,1,1,1,0,1))
        self.assertEqual(encoding,decoding)
        self.assertEqual(HCResult.VALID,Tag)
        
    def test_decode_corrected(self):
        """ Essential: Test method decode() with CORRECTED input """

        hamming = HammingCode()
        encoding= hamming.encode((0,0,0,0,0,0))
        decoding,Tag = hamming.decode((0,0,0,0,0,0,0,0,0,0,1))
        self.assertEqual(encoding,decoding)
        self.assertEqual(HCResult.CORRECTED,Tag)

        encoding= hamming.encode((0,1,1,0,1,1))
        decoding,Tag = hamming.decode((0,0,1,0,1,1,1,1,1,1,0))
        self.assertEqual(encoding,decoding)
        self.assertEqual(HCResult.CORRECTED,Tag)
        
        encoding= hamming.encode((1,1,1,1,1,0))
        decoding,Tag = hamming.decode((1,1,1,1,1,0,1,0,1,1,1))
        self.assertEqual(encoding,decoding)
        self.assertEqual(HCResult.CORRECTED,Tag)

        encoding= hamming.encode((1,0,1,1,0,1))
        decoding,Tag = hamming.decode((1,0,0,1,0,1,1,1,1,0,1))
        self.assertEqual(encoding,decoding)
        self.assertEqual(HCResult.CORRECTED,Tag)
        
    def test_decode_uncorrectable(self):
        """ Essential: Test method decode() with UNCORRECTABLE input """

        hamming = HammingCode()
        encoding= hamming.encode((0,1,1,0,1,1))
        decoding,Tag = hamming.decode((1,0,1,1,1,1,1,1,1,1,0))
        self.assertNotEqual(encoding,decoding)
        self.assertEqual(HCResult.UNCORRECTABLE,Tag)
 
        encoding= hamming.encode((0,1,1,0,1,1))
        decoding,Tag = hamming.decode((0,0,1,0,1,1,1,0,1,1,0))
        self.assertNotEqual(encoding,decoding)
        self.assertEqual(HCResult.UNCORRECTABLE,Tag)
        
    def test_encode(self):
        """ Essential: Test method encode() """
        hamming = HammingCode()
        encoding= hamming.encode((0,1,1,0,1,1))
        decoding= (0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0)
        self.assertEqual(encoding,decoding)

        encoding= hamming.encode((0,0,0,0,0,0))
        decoding= (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.assertEqual(encoding,decoding)

        encoding= hamming.encode((1,0,1,1,0,1))
        decoding= (1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1)
        self.assertEqual(encoding,decoding)

        encoding= hamming.encode((1,1,1,1,1,0))
        decoding= (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1)
        self.assertEqual(encoding,decoding)
if __name__=='__main__':
    unittest.main()