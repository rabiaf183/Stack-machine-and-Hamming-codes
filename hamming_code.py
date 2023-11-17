
#!/usr/bin/env python3

from enum import Enum
from typing import List, Tuple, Union


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class HCResult(Enum):
   
    VALID = 'OK'
    CORRECTED = 'FIXED'
    UNCORRECTABLE = 'ERROR'


class HammingCode:
    

    def __init__(self):
        
        self.total_bits = 10  # n
        self.data_bits = 6  # k
        self.parity_bits = 4  # r

        # Predefined non-systematic generator matrix G'
        self.gns = [[1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
                    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
                    [1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
                    [1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
                    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1]]

          # Steps for Converting non-systematic G' into systematic matrices G, H
      
        self.g = [row[:] for row in self.gns] # shallow copy of G bar 
        self.g = self.__convert_to_g(self.g)  # calling to convert in row echolon
        self.h = self.__derive_h(self.g) #call to derive H from G

    def subtract_rows(self, matrix, target_row, other_rows):
        cols = len(matrix[0]) #initialzing an integer of number of columns= G bar matrix column =10
        target_row -= 1 #because index numbers start from 0

        for other_row in other_rows: ##get every other row of G bar matrix to get all 0
          other_row -= 1 #because index numbers start from 0

          

          for i in range(cols):
            # print(matrix[source_row][i])
            matrix[other_row][i] = matrix[other_row][i] ^ matrix[target_row][i] #subtract target row from source row

        return matrix

    def __convert_to_g(self, gns: List):
        
        matrix = self.subtract_rows(gns, 1, [3, 5, 6]) #matrix, target row, source rows
        matrix = self.subtract_rows(matrix, 2, [1, 3, 6])
        matrix = self.subtract_rows(matrix, 3, [1, 5, 6])
        matrix = self.subtract_rows(matrix, 4, [1, 3])
        matrix = self.subtract_rows(matrix, 5, [2, 3])
        matrix = self.subtract_rows(matrix, 6, [1, 2, 5])
        return matrix
    def __derive_h(self, g: List):
    
      #derive parity check matrix from systematic G
        H = [] #empty matrix
        for row in g:
          H.append(row[6:])#copy 6 onwards column to convert 6*10 matrix to 6*4

        
        sys_H = []#create empty transpose matrix
        for i in range(len(H[0])): #len of H is 4 as 6 by 4 matrix
          sys_H.append([0]*len(H)) # an empty matrix of 0 of 4 by 6 is created

        #now transfer transpose values in sys_H
        for i in range(len(H)): #6
          for j in range(len(H[0])): #4
            sys_H[j][i] = H[i][j] #copy the contents of H into transposed matrix

        #create identity matrix
        I = [[1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]

        for row in range(len(sys_H)): #6 is the no of columns
          for value in I[row]: # 4 from identity matrix
            sys_H[row].append(value) # 4 columns will append to 4 by 6 sys_H matrix

        return sys_H
       
    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
    
        #add parity bit in g
            sys_g = [row[:] for row in self.g]# make a copy of G matrix
            for row in range(len(sys_g)): #calculate the parity bit and append to make g 6 by 11, len of g is 6
                parity_bit = sum(sys_g[row])%2
                sys_g[row].append(parity_bit)
                parity_cols = len(sys_g[0]) #10
                resultant_matrix = [0] * parity_cols #all 10 columns will be 0

            for col in range(len(sys_g[0])): #10
               for row in range(len(sys_g)): #6
                resultant_matrix[col] += sys_g[row][col] * source_word[row] 
        #take mod 2
            for i in range(len(resultant_matrix)):
             resultant_matrix[i] = resultant_matrix[i] % 2

            syndrom_matrix = tuple(resultant_matrix) #return an immutable tuple matrix
            return syndrom_matrix
    def decode(self, encoded_word: Tuple[int, ...]) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
       
        encoded_word = list(encoded_word)# convert tuple to list
        overall_parity = sum(encoded_word)%2 #calculate overall parity bit P5
        word_parity = encoded_word[len(encoded_word)-1] #save the last parity bit for comparision
        encoded_word = encoded_word[:len(encoded_word)-1] # exclude the last parity bit and save it 

        copy_h = [row[:] for row in self.h] #make a copy of systemtaic H

      
        #multiply source word with parity bit matrix
        res_rows = len(copy_h) #4
        resultant_matrix = [0] * res_rows # 4x1 and all will 0 

        for col in range(len(copy_h[0])): # 10
          for row in range(len(copy_h)): # 4
              resultant_matrix[row] += copy_h[row][col] * encoded_word[col]

        #take mod 2
        for i in range(len(resultant_matrix)):
          resultant_matrix[i] = resultant_matrix[i] % 2

        #check error
        if sum(resultant_matrix) == 0 and overall_parity == 0: #IF valid
          encoded_word.append(word_parity)
          encoded_word = tuple(encoded_word)
          return (encoded_word, HCResult.VALID)

        elif sum(resultant_matrix) == 0 and overall_parity == 1: #IF 1's in parity
          word_parity = int(not word_parity)
          encoded_word.append(word_parity)
          encoded_word = tuple(encoded_word)
          return (encoded_word, HCResult.CORRECTED)

        else:

          #flip hp for easy comparison
          #create empty matrix
          flip_copy_h = []
          for i in range(len(copy_h[0])):
            flip_copy_h.append([0]*len(copy_h))

    
          for i in range(len(copy_h)):
            for j in range(len(copy_h[0])):
              flip_copy_h[j][i] = copy_h[i][j]

          col = 0
          for row in flip_copy_h:
            if row == resultant_matrix and overall_parity == 1:
              encoded_word[col] = int(not encoded_word[col])
              encoded_word.append(word_parity)
              encoded_word = tuple(encoded_word)
              return (encoded_word, HCResult.CORRECTED)
            if row == resultant_matrix and overall_parity == 0:
              return (None, HCResult.UNCORRECTABLE)
            col += 1

          return (None, HCResult.UNCORRECTABLE)

