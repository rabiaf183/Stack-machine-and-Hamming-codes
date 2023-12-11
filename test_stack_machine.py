    #!/usr/bin/env python3

import unittest
import unittest.mock
from stack_machine import StackMachine
from stack_machine import SMState


class TestStackMachine(unittest.TestCase):
    def test_instance(self):
       
        my_stackmachine = StackMachine()
        result = isinstance(my_stackmachine,StackMachine)
        self.assertTrue(result)
        self.assertEqual(my_stackmachine.stack,[])

    def test_top (self):
        my_stackmachine = StackMachine()

        #NUMBER
        number1 = my_stackmachine.do((0, 0, 1, 1, 1, 1))
        topvalue = my_stackmachine.top()
        exp = (0, 0, 0, 0, 1, 1, 1, 1)
        self.assertEqual(exp,topvalue)

        # CHARACTER
        number1 = my_stackmachine.do((1, 0, 0, 1, 0, 0))
        topvalue = my_stackmachine.top()
        exp = 'A'
        self.assertEqual(exp, topvalue)



    def test_do(self):
        my_stackmachine = StackMachine()
        word_sequence =[(0,0,1,0,1,0),(0,1,0,0,0,1),(0,1,0,0,0,1), (0,1,0,1,1,0),(0,1,1,1,1,1),(0,0,0,1,0,0),(0,1,1,0,1,1),(0,0,0,1,0,0),(0,1,1,0,0,1),
        (0,0,0,1,1,0), (0,1,1,0,0,0),(1,0,0,0,1,0),(1,1,0,1,1,0),(1,0,1,0,0,0),(1,1,0,1,0,1),(0,0,0,1,0,1),(1,0,0,0,0,1),(0,1,0,0,0,0)]

        word_states = [SMState.RUNNING]*17
        word_states.append(SMState.STOPPED)

        states= []
        for code_word in word_sequence:
            state = my_stackmachine.do(code_word)
            states.append(state)


        self.assertEqual(word_states , states)
        self.assertEqual(my_stackmachine.stack , [])
    def test_add (self):
       
        my_stackmachine=StackMachine()
        
        number1 = my_stackmachine.do((0, 0, 0, 1, 0, 1))
        number2 = my_stackmachine.do((0, 0, 1, 1, 1, 1))
        add = my_stackmachine.do((0, 1, 0, 1, 0, 0))
        number2 = my_stackmachine.do((0, 0, 1, 1, 1, 1))
        add = my_stackmachine.do((0, 1, 0, 1, 0, 0))


        self.assertEqual(SMState.RUNNING, add)
        my_stackmachine.stack.clear()

    def test_sub (self):
        
        my_stackmachine=StackMachine()
        number1= my_stackmachine.do((0, 0, 1, 1, 1, 1))
        number2 = my_stackmachine.do((0, 0, 0, 1, 0, 0))
        sub =my_stackmachine.do((0, 1, 0, 1, 0, 1))
        self.assertEqual(SMState.RUNNING, sub)

    def test_mul (self):
        #Correct Input
        my_stackmachine=StackMachine()
        number1 = my_stackmachine.do((0, 0, 1, 1, 1, 1))
        number2= my_stackmachine.do((0, 0, 0, 1, 0, 0))
        mul = my_stackmachine.do((0, 1, 0, 1, 1, 0))
        self.assertEqual(SMState.RUNNING, mul)

    def test_div (self):
        #Correct Input
        my_stackmachine=StackMachine()
        number1= my_stackmachine.do((0, 0, 1, 1, 1, 1))
        number2= my_stackmachine.do((0, 0, 0, 1, 0, 0))
        div = my_stackmachine.do((0, 1, 0, 1, 1, 1))
        self.assertEqual(SMState.RUNNING, div)

        my_stackmachine.stack.clear()

        number1 = my_stackmachine.do((0, 0, 0, 0, 1, 1))
        number2 = my_stackmachine.do((1, 0, 0, 1, 0, 0))
        div = my_stackmachine.do((0, 1, 0, 1, 1, 1))
        self.assertEqual(SMState.ERROR, div)


        number1 = my_stackmachine.do((0, 0, 0, 0, 0, 0))
        number2 = my_stackmachine.do((0, 0, 0, 0, 1, 1))
        div = my_stackmachine.do((0, 1, 0, 1, 1, 1))
        self.assertEqual(SMState.ERROR, div)


        my_stackmachine.stack.clear()
    def test_exp (self):
        
        my_stackmachine =StackMachine()
        number1 = my_stackmachine.do((0, 0, 0, 0, 1, 1))
        number2 = my_stackmachine.do((0, 0, 0, 1, 0, 0))
        exp = my_stackmachine.do((0, 1, 1, 0, 0, 0))
        self.assertEqual(SMState.RUNNING, exp)

        my_stackmachine.stack.clear()

        number1 = my_stackmachine.do((0, 0, 0, 0, 1, 1))
        number2 = my_stackmachine.do((1, 0, 0, 0, 0, 0))
        exp = my_stackmachine.do((0, 1, 1, 0, 0, 0))
        self.assertEqual(SMState.ERROR, exp)

    def test_mod (self):
        
        my_stackmachine = StackMachine()
        number1 = my_stackmachine.do((0, 0, 0, 1, 1, 1))
        number2 = my_stackmachine.do((0, 0, 0, 1, 0, 1))
        mod = my_stackmachine .do((0, 1, 1, 0, 0, 1))
        self.assertEqual(SMState.RUNNING, mod)

        my_stackmachine.stack.clear()


        #Incorrect Input
        v1 = my_stackmachine.do((0, 0, 0, 1, 1, 1))
        v2 = my_stackmachine.do((1, 0, 0, 1, 0, 0))
        mod =my_stackmachine.do((0, 1, 1, 0, 0, 1))
        self.assertEqual(SMState.ERROR, mod)

    def test_shl (self):
        #Correct Input
        my_stackmachine = StackMachine()
        number1 = my_stackmachine.do((0, 0, 0, 1, 1, 1))
        number1 = my_stackmachine.do((0, 0, 0, 1, 0, 1))
        shl = my_stackmachine.do((0, 1, 1, 0, 1, 0))
        self.assertEqual(SMState.RUNNING, shl)

        my_stackmachine.stack.clear()

        #Incorrect Input
        number1 = my_stackmachine.do((0, 0, 0, 1, 1, 1))
        number2 = my_stackmachine.do((1, 0, 0, 1, 0, 0))
        shl = my_stackmachine.do((0, 1, 1, 0, 1, 0))
        self.assertEqual(SMState.ERROR, shl)
    def test_shr (self):
        #Correct Input
        machine = StackMachine()
        number1 = machine.do((0, 0, 1, 1, 1, 1))
        number2 = machine.do((0, 0, 0, 0, 1, 0))
        shr = machine.do((0, 1, 1, 0, 1, 1))
        self.assertEqual(SMState.RUNNING, shr)

        machine.stack.clear()

        #Incorrect Input
        number1 = machine.do((0, 0, 1, 1, 1, 1))
        number2 = machine.do((1, 0, 0, 1, 0, 0))
        shr = machine.do((0, 1, 1, 0, 1, 1))
        self.assertEqual(SMState.ERROR, shr)
    def test_hex(self):
       
        my_stackmachine = StackMachine()
        number1 =  my_stackmachine.do((1, 0, 0, 1, 0, 0))
        number2 =  my_stackmachine.do((1, 0, 0, 1, 0, 1))
        hexa =  my_stackmachine.do((0, 1, 1, 1, 0, 0))
        self.assertEqual(SMState.RUNNING, hexa)

        my_stackmachine.stack.clear()
    def test_fac(self):
        #Correct Input
        my_stackmachine = StackMachine()
        number1 = my_stackmachine.do((0, 0, 0, 1, 0, 0))
        fac = my_stackmachine.do((0, 1, 1, 1, 0, 1))
        self.assertEqual(SMState.RUNNING, fac)


    def test_Not(self):
        #Correct Input
        my_stackmachine = StackMachine()
        number1 = my_stackmachine.do((0, 0, 0, 1, 0, 1))
        notf = my_stackmachine.do((0, 1, 1, 1, 1, 0))
        self.assertEqual(SMState.RUNNING, notf)
    
    def test_duplicate(self):
        #Correct Input
        my_stackmachine = StackMachine()
        number1 = my_stackmachine.do((1, 0, 0, 1, 0, 0))
        dup = my_stackmachine.do((0, 1, 0, 0, 0, 1))
        self.assertEqual(SMState.RUNNING, dup)

    def test_Xor(self):
        #Correct Input
        machine = StackMachine()
        number1 = machine.do((0, 0, 1, 1, 1, 1))
        number2 = machine.do((0, 0, 0, 1, 0, 1))
        xor = machine.do((0, 1, 1, 1, 1, 1))
        self.assertEqual(SMState.RUNNING, xor)

    
    def test_swap(self):
        #Correct Input
        my_stackmachine = StackMachine()
        number1 = my_stackmachine.do((0, 0, 1, 1, 1, 1))
        number2 = my_stackmachine.do((0, 0, 0, 1, 0, 1))
        swp = my_stackmachine.do((0, 1, 0, 0, 1, 1))
        self.assertEqual(SMState.RUNNING, swp)

    def test_del(self):
        #Correct Input
        my_stackmachine = StackMachine()
        number1 = my_stackmachine.do((1, 0, 0, 1, 0, 0))
        delete = my_stackmachine.do((0, 1, 0, 0, 1, 0))
        self.assertEqual(SMState.RUNNING, delete)


   


if __name__ == '__main__':
                    unittest.main()
