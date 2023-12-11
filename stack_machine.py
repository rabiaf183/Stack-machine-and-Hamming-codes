from enum import IntEnum
from typing import List, Tuple, Union
from ctypes import c_ubyte
import math


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class SMState(IntEnum):
    """
    Return codes for the stack machine
    """
    RUNNING = 1 
    STOPPED = 0 #if all operation has been perfomed
    ERROR = -1 #if not enough value in stack


class StackMachine:
    """
    Implements the 8-bit stack machine according to the specification
    """

    def __init__(self) -> None:
      
        self.overflow = False
        self.stack = []

    def is_empty(self) -> bool: #check if stack is empty
        return len(self.stack) == 0 #will retun true if stack is empty
    
    def convert_to_binary(self, number):
        binary = bin(number) #bin(5)=101
        return binary    

    def convert_to_integer(self, code_word):
        binary_word = ''.join([str(x) for x in code_word]) #(1,0,1)= 101
        binary_word = '0b' + binary_word #0b101
        binary_word = int(binary_word, 2) #base 2 = int 5
        return binary_word


    def convert_to_tuple(self, number):
        number = bin(number) #5-> 0b101
        output = str(number) #str 0b101
        output = output.replace('0b', '') #101
        output = list(output)#['1','0','1']
        for i in range(len(output)): 
            output[i] = int(output[i]) #converts to integer [1,0,1]
        output = tuple(output) #(1,0,1)
        return output 

    def convert_to_8b(self, small_tuple):
      #to convert the arbitary bits into tuple
        tuple_length = len(small_tuple) #(1,0,1) =3
        remaining_bits = 8-tuple_length #8-3 =5
        bits = [0]*remaining_bits #[0,0,0,0,0]
        bits = tuple(bits) #(0,0,0,0,0)
        tuple_8b = bits + small_tuple #(0,0,0,0,0,1,0,1)
        return tuple_8b 

    def top(self) -> Union[None, str, Tuple[int, int, int, int, int, int, int, int]]:

        if not self.is_empty():
            top_item = self.stack[-1]
            return top_item
        else:
            return None


    def do(self, code_word: Tuple[int, ...]) -> SMState:

        bit1 = code_word[0] #taking first two bits of codeword to identify the character or instruction
        bit2 = code_word[1]

        dict_instruction = {0b010000: "STP", 0b010001: "DUP", 0b010010: "DEL", 0b010011: "SWP", 0b010100: "ADD", 0b010101: "SUB", 0b010110: "MUL",
                            0b010111: "DIV", 0b011000: "EXP", 0b011001: "MOD", 0b011010: "SHL", 0b011011: "SHR",  0b011100: "HEX", 0b011101:  "FAC",
                            0b011110: "NOT", 0b011111: "XOR"}

        dict_character = {0b100000: "NOP",  0b100011: "NOP", 0b111110: "NOP",  0b111111: "NOP", 0b100001: "SPEAK",  0b100010: " ", 0b100100: "A", 0b100101: "B",
                          0b100110: "C",  0b100111: "D", 0b101000: "E", 0b101001: "F", 0b101010: "G",  0b101011: "H",  0b101100: "I",
                          0b101101: "J",  0b101110: "K", 0b101111: "L",  0b110000: "M",  0b110001: "N",  0b110010: "O", 0b110011: "P",
                          0b110100: "Q",  0b110101: "R", 0b110110: "S",  0b110111: "T",  0b111000: "U", 0b111001: "V",  0b111010: "W",
                          0b111011: "X",  0b111100: "Y",  0b111101: "Z"}

        if bit1 == 0 and bit2 == 0:  # operation for Operand
            code_word = self.convert_to_8b(code_word) #convert to 8b and append in stack 
            self.stack.append(code_word)
            self.overflow = False
            return SMState.RUNNING #returns the state running

        elif bit1 == 0 and bit2 == 1:  # operation for instruction
            binary = self.convert_to_integer(code_word) #convert the codeword in to 
            instruction = dict_instruction[binary]

            #############for characters conditions#################

        elif bit1 == 1:  # operation for CHARACTER
            binary = self.convert_to_integer(code_word)
            output = dict_character[binary]
            if output == 'NOP': #do nothing
                return SMState.RUNNIG
            elif output == 'SPEAK': # convert the stack value in to str and append the msg "" in it and returns state running
                number = self.stack.pop() 
                number= self.convert_to_integer(number)
                msg = ''
                for i in range(number): #till the length of number pop the elements from stack
                    word = self.stack.pop()
                    if isinstance(word, tuple): #if the poped word is tuple, convert to integer
                        word = self.convert_to_integer(word)
                        word = str(word) #then convert the integer to str
                    msg = word + msg #now append
                print(msg)
                return SMState.RUNNING
            else:
                self.stack.append(output) #if nothing from NOP or SPEAK then simply append
                return SMState.RUNNING

        else:
            return SMState.ERROR #if something else except the defined dictionary 
            ############end characters ####################
            #############For Instructions 01#############

        one_inst = ['DUP', 'DEL', 'NOT', 'FAC']

        if instruction == 'STP': #do nothing except stop the procesing 
            return SMState.STOPPED
        if instruction in one_inst:
            if len(self.stack) == 0: 
                print('stack is empty, cant perform any action')
                return SMState.ERROR
            
        else:
            if len(self.stack) < 2: #check if the stack has less than 2 operands
                print('Not enough operands')
                return SMState.ERROR
            else:
                number1 = self.stack.pop()
                number2 = self.stack.pop()

        if instruction == 'DUP':
            result = number1
            self.stack.append(result)#pop and append again to duplicate
            self.stack.append(result)
            return SMState.RUNNING

        elif instruction == 'SWP': #pop and append the number1 first and then number2 to swap value
            self.stack.append(number1)
            self.stack.append(number2)
            return SMState.RUNNING

        elif instruction == 'DEL': #pop and does not append
            return SMState.RUNNING
        
        elif instruction == 'SUB':
            number1 = self.convert_to_integer(number1)
            number2 = self.convert_to_integer(number2)
            if number1 > number2: #no negative value should be there
                self.overflow = True
                return SMState.STOPPED  # because cannot convert the negative answer to binary - so stop
            else:
                self.overflow = False
            result = number2 - number1
            result = self.convert_to_tuple(result)
            result = self.convert_to_8b(result)
            self.stack.append(result)
            return SMState.RUNNING

        elif instruction == 'ADD': #perform add after converting in integer and then check for overflow
            number1 = self.convert_to_integer(number1)
            number2 = self.convert_to_integer(number2)
            result = number1 + number2
            if result > 255:
                self.overflow = True
            else:
                self.overflow = False #if not then convert the integer in to tuple and make it to 8b
            result = self.convert_to_tuple(result)
            result = self.convert_to_8b(result)
            self.stack.append(result)
            return SMState.RUNNING

      

        elif instruction == 'MUL': #simple integer multiplication
            number1 = self.convert_to_integer(number1)
            number2 = self.convert_to_integer(number2)
            result = number2 * number1
            if result > 255:
                self.overflow = True #check for overflow
                return SMState.ERROR
            else:
                self.overflow = False
            result = self.convert_to_tuple(result)
            result = self.convert_to_8b(result)
            self.stack.append(result)
            return SMState.RUNNING

        elif instruction == 'DIV': #dinominator shouldn't be 0 to avoid infinity condition
            number1 = self.convert_to_integer(number1)
            number2 = self.convert_to_integer(number2)
            if number2 == 0:
                print("cannot divide by zero")
                return SMState.ERROR
        

            result = number1 / number2 #before_value/ after value
            result = self.convert_to_tuple(result)
            result = self.convert_to_8b(result)
            self.stack.append(result)
            self.overflow = False
            return SMState.RUNNING

        elif instruction == 'MOD':
            number1 = self.convert_to_integer(number1)
            number2 = self.convert_to_integer(number2)
            result = number2 % number1 #after value % before value
            result = self.convert_to_tuple(result)
            result = self.convert_to_8b(result)
            self.stack.append(result)
            self.overflow = False
            return SMState.RUNNING

        elif instruction == 'EXP':
            number1 = self.convert_to_integer(number1)
            number2 = self.convert_to_integer(number2)
            result = number2 ** number1 #after value ^ before value
            if result > 255:
                self.overflow = True
                return SMState.ERROR
            else:
                self.overflow = False
            result = self.convert_to_tuple(result)
            result = self.convert_to_8b(result)
            self.stack.append(result)
            return SMState.RUNNING

        elif instruction == 'SHR': #perform shift right operation to after value by the before value
            number1 = self.convert_to_integer(number1)
            number2 = self.convert_to_integer(number2)
            result = number2 >> number1
            result = self.convert_to_tuple(result)
            result = self.convert_to_8b(result)
            self.stack.append(result)
            self.overflow = False
            return SMState.RUNNING
        

        elif instruction == 'SHL': #**
            number1 = self.convert_to_integer(number1)
            number2 = self.convert_to_integer(number2)
            result = number2 << number1 #shift left operation
            if result > 255:
                self.overflow = True
            else:
                self.overflow = False
            result = self.convert_to_tuple(result)
            result = self.convert_to_8b(result)
            self.stack.append(result)
            return SMState.RUNNING

        elif instruction == 'FAC':
            number1 = self.convert_to_integer(number1)
            result = (math.factorial(number1)) #python defined function
            if result > 255:
                self.overflow = True
            else:
                self.overflow = False
            result = self.convert_to_tuple(result)
            result = self.convert_to_8b(result)
            self.stack.append(result)
            return SMState.RUNNING

        

        elif instruction == 'HEX': #***
            number1 = self.convert_to_integer(number1) #5
            number2 = self.convert_to_integer(number2) #9
            number1 = str(number1)
            number2 = str(number2)
            result = number1 + number2 #59
            result = int(result, 16) # convert into decimal 16 
            result = self.convert_to_tuple(result)
            result = self.convert_to_8b(result)
            self.stack.append(result)
            self.overflow = False
            return SMState.RUNNING

        elif instruction == 'XOR': #**
            result = []
            for x in range(len(number1)):
                result.append(number1[x] ^ number2[x])
            result = tuple(result)
            result = self.convert_to_8b(result)
            self.stack.append(result)
            self.overflow = False
            return SMState.RUNNING
      

        elif instruction == 'NOT': #**
            result = []
            for bit in number1:
                result.append(int(not bit))

            result = tuple(result)
            self.stack.append(result)
            self.overflow = False
            return SMState.RUNNING

        

   
