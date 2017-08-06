"""Calc functions are defined here"""
from complexdecimal import ComplexDecimal
import constants
import random, math

def conj(n): return n.conj()
def Re(n): return n.re()
def Im(n): return n.im()

def round(n,p=0): return n.round(n,p)
def isPrime(n): 
    if n > ComplexDecimal(1000000): return None
    return n.isPrime()
def log(n,x=10):return n.log(x)
def phase(n):return n.phase()
def exp(n):return n.exp()
def floor(n):return n.floor()
def ceil(n):return n.ceil()
def ln(n):return n.ln()

def sin(n):return n.sin()
def cos(n):return n.cos()
def tan(n):return n.tan()
def asin(n):return n.asin()
def acos(n):return n.acos()
def atan(n):return n.atan()
def sqrt(n): return n.sqrt()

def sinh(n):return n.sinh()
def cosh(n):return n.cosh()
def tanh(n):return n.tanh()
def asinh(n):return n.asinh()
def acosh(n):return n.acosh()
def atanh(n):return n.atanh()

def radian(n):
    return n * ComplexDecimal(constants.constants["pi"]) / ComplexDecimal(180)
def degree(n):
    return n * ComplexDecimal(180) / ComplexDecimal(constants.constants["pi"])
    
def grad_to_rad(n):
    return n * ComplexDecimal(constants.constants["pi"]) / ComplexDecimal(200)
def rad_to_grad(n):
    return n * ComplexDecimal(200) / ComplexDecimal(constants.constants["pi"])

def factorial(n):
    if n.imaginary != 0:
        raise ArithmeticError("You cannot have imaginary factorial.")
    if n < ComplexDecimal(0): raise ArithmeticError("You cannot have negative factorial.")
    if n < ComplexDecimal(2): return ComplexDecimal(1)
    
    returned = ComplexDecimal(1)
    for i in range(2,int(n)+1):
        returned *= ComplexDecimal(i)
    return returned

def double_fact(n):
    if n.imaginary != 0:
        raise ArithmeticError("You cannot have imaginary factorial.")
    if n < ComplexDecimal(0): raise ArithmeticError("You cannot have negative factorial.")
    if n < ComplexDecimal(2): return ComplexDecimal(1)
    
    returned = ComplexDecimal(1)
    for i in range(int(n),1,-2):
        returned *= ComplexDecimal(i)
    return returned
    
def rand(a,b=ComplexDecimal(0)):
    if b<a: #Swap if b > a
        a,b = b,a
    a = int(a); b = int(b)
    return ComplexDecimal(random.randint(a,b))
    
def uniform(a,b=ComplexDecimal(0)):
    if b<a: #Swap if b > a
        a,b = b,a
    a = int(a); b = int(b)
    return ComplexDecimal(random.uniform(a,b))
    
def gcf(a, b):
    while b != ComplexDecimal(0):
        a, b = b, a%b
    return a
    
def lcm(a, b):
    return a*b / gcf(a,b)
    
def factors(a):
    if a > ComplexDecimal(1000000):
        return []
    f = []
    for i in range(1,int(math.ceil(math.sqrt(a))) ):
        if a % ComplexDecimal(i) == ComplexDecimal(0):
            f.append(ComplexDecimal(i))
            f.append(a / ComplexDecimal(i))
    return f

def nPr(n,r):
    return factorial(n) / factorial(n-r)
    
def nCr(n,r):
    return nPr(n,r) / factorial(r)