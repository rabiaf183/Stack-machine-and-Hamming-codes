import unittest #python builtin test library
from hamming_code import HammingCode
from hamming_code import HCResult #calling asserts error messages
class TestHammingCode(unittest.TestCase): #calling testcase function from unittest library 
    def test_instance(self): #defining test instance 
    
        hamming = HammingCode() #calling hamming class
    #we will unittest all ur inputs to perform encoding and deocoding
        
    def test_decode_valid(self): #for no errors in receieving message
        hamming = HammingCode()
        encoding= hamming.encode((1,0,1,1,0,1))
        decoding,Tag = hamming.decode((1,0,1,1,0,1,1,1,1,0,1))
        self.assertEqual(encoding,decoding)#checks if both the values are equal
        self.assertEqual(HCResult.VALID,Tag)
        
    def test_decode_corrected(self): #for 1 bit errors
        

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

    def test_encode(self):
    
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
        
    def test_decode_uncorrectable(self): #for more than 2 errors
       
        hamming = HammingCode()
        encoding= hamming.encode((0,1,1,0,1,1))
        decoding,Tag = hamming.decode((1,0,1,1,1,1,1,1,1,1,0))
        self.assertNotEqual(encoding,decoding)
        self.assertEqual(HCResult.UNCORRECTABLE,Tag)
 
        encoding= hamming.encode((0,1,1,0,1,1))
        decoding,Tag = hamming.decode((0,0,1,0,1,1,1,0,1,1,0))
        self.assertNotEqual(encoding,decoding)
        self.assertEqual(HCResult.UNCORRECTABLE,Tag)
        
    
if __name__=='__main__': #boierplate to only call script when we intend to
    unittest.main() #calling main test 