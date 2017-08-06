"""Equations
Can be multiplied by each other, or a number
Addition, subtraction etc..."""
import sys
sys.path.append("..")

from complexdecimal import ComplexDecimal
import re

class Polynomial(object):
    def __init__(self,*terms): #Array of terms or a string to phrase
        """Self.terms is an array
        index 0 is the constant, index 1 is the term with degree 1, etc...
        So 3x^2 + 2x + 1 would be [1,2,3]
        However when defining define in right to left order
        for example Polynomial(1,2,3) would be x^2 + 2x + 3, not 3x^2 + 2x + 1
        
        Functions:
            Add, subtract, divide, multiply, powers, etc...
            Factor
            GCD, GCF
            Intergal

            Pretty printing :D"""
        
        self.terms = []
        if type(terms[0]) == list: terms = terms[0]
        for i in terms:
            if type(i) != ComplexDecimal: self.terms.append(ComplexDecimal(i))
            else: self.terms.append(i)
        self.terms.reverse()
        
        #Define some things
        self.degree = len(self.terms)-1
        self.length = len(self.terms)
        self.names = [self.get_name_degree(), self.get_name_terms()]
        
        self.roots = self.get_roots()
        
        #Refine some function names
        self.eval = self.evaluate
    
    #NAMING THE POLYNOMIAL
    #--------------------------------------------------------
    def get_name_degree(self):
        try: return ["constant","linear","quadratic","cubic","quartic","quintic","sextic","septic","octic","nonic","decic"][self.degree]
        except: return "{}th degree polynomial".format(self.degree)
        
    def get_name_terms(self):
        try: return ["monomial","binomial","trinomial"][self.length-1]
        except: return "polynomial"
    
    #ROOTS STUFF
    #----------------------------------------------------------
    def get_root_sum(self): #Sum of roots
        return -self.terms[-2] / self.terms[-1]
        
    def get_root_product(self):
        return self.terms[0] / self.terms[-1]
    
    def get_roots(self):
        if self.degree == 0: return [self.terms[0]] #Constant
        elif self.degree == 1: #Linear equation
            return [-self.terms[0] / self.terms[1]]
        elif self.degree == 2: #Quadratic
            a,b,c = self.terms[2],self.terms[1],self.terms[0]
            dis = b*b - ComplexDecimal(4)*a*c
            root1 = (-b + dis.sqrt()) / ComplexDecimal(2) / a
            root2 = (-b - dis.sqrt()) / ComplexDecimal(2) / a
            return [root1, root2]
            
        r = ComplexDecimal(5) #Bad inital guess, but who's going to use this?
        for i in range(0,20):
            r = r- self.evaluate(r) / self.derv().evaluate(r)
        return [r]

    #OTHER STUFF
    #----------------------------------------------------------
    def evaluate(self,x):
        """Evaluate itself with varaible x"""
        index = final = ComplexDecimal(0)
        for i in self.terms:
            final += i * x**index
            index += ComplexDecimal(1)
        return final
    
    #CALCULUS SHIT
    #-----------------------------------------------------------
    def derv(self): #Derviative of self :D
        new_terms = []
        index = 0
        for i in self.terms:
            if index == 0: pass
            else:
                new_terms.append(i*ComplexDecimal(index))
            index += 1
        new_terms.reverse()
        return Polynomial(new_terms)
        
    #OPERATOR OVERRIDE
    #-----------------------------------------------------------

a = Polynomial(500,5,5,50) #The polyonimal x^3 + 2x^2 + 3x + 4
print a.names
print a.roots[0]

