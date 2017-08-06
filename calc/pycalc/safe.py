"""Safety script to delete unsafe variables in the code
Kinda useless but I guess some people would find it better to have it"""

unsafe = [
    "__import__",
    "import",
    "decode",
    "encode",
    "eval",
    "exec",
    "open",
    "sys",
    "os",
    "file",
    "imp",
    "class",
    "assert",
    "def",
    "del",
    "global",
    "raise",
    "with",
    "while",
    "return",
    "yeild",
    "from",
    "pass",
    "lambda",
    "nonlocal"
]

from functions import *
from complexdecimal import ComplexDecimal
from date import Date
"""Define list of allowed functions in calc"""

safe_dict = {}
safe_dict["sin"] = sin
safe_dict["cos"] = cos
safe_dict["tan"] = tan
safe_dict["asin"] = asin
safe_dict["acos"] = acos
safe_dict["atan"] = atan

safe_dict["sinh"] = sinh
safe_dict["cosh"] = cosh
safe_dict["tanh"] = tanh
safe_dict["asinh"] = asinh
safe_dict["acosh"] = acosh
safe_dict["atanh"] = atanh

safe_dict["sqrt"] = sqrt
safe_dict["abs"] = abs
safe_dict["log"] = log
safe_dict["fact"] = factorial
safe_dict["factorial"] = factorial
safe_dict["double_fact"] = double_fact
safe_dict["ceil"] = ceil
safe_dict["floor"] = floor
safe_dict["exp"] = exp
safe_dict["ln"] = ln

safe_dict["deg"] = degree
safe_dict["rad"] = radian
safe_dict["degrees"] = degree
safe_dict["radians"] = radian
safe_dict["grad_to_rad"] = grad_to_rad
safe_dict["rad_to_grad"] = rad_to_grad

safe_dict["isPrime"] = isPrime
safe_dict["nCr"] = nCr
safe_dict["nPr"] = nPr


safe_dict["round"] = round
safe_dict["Re"] = Re
safe_dict["Im"] = Im
safe_dict["conj"] = conj

safe_dict["random"] = rand
safe_dict["uniform"] = uniform

safe_dict["gcf"] = gcf
safe_dict["gcd"] = gcf
safe_dict["hcf"] = gcf
safe_dict["lcm"] = lcm
safe_dict["factor"] = factors

safe_dict["ComplexDecimal"] = ComplexDecimal
safe_dict["Date"] = Date
safe_dict["Time"] = Date