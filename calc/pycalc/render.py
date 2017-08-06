"""Renders different object types neatly. Current progress:
-Arrays 
-Dictionaries
-Tuples
"""

from complexdecimal import ComplexDecimal
from date import Date
import fractions

def render(thing, options):
    if type(thing) == ComplexDecimal:
        return renderDec(thing, options)
    elif type(thing) in [list,tuple]:
        return "[ " + ", ".join([renderDec(x,options) for x in thing]) + " ]"
    elif type(thing) == dict:
        returned = "{ "
        for key in thing:
            returned += "'"+key+"'" + " : " + renderDec(thing[key],options) + ", "
        return returned + " }"
    return renderDec(thing, options)
    
def renderDec(thing, options): #DISPLAY OPTIONS: SCI, DEFAULT, FRACT
    if type(thing) == Date: return str(thing)
    if type(thing) == ComplexDecimal:
        if options["display"] == "DEFAULT": return str(thing)
        if options["display"] == "FRACT": 
            if thing.imaginary == 0:
                return str(fractions.Fraction(thing.real))
            elif thing.real == 0:
                str(fractions.Fraction(thing.imaginary)) + "i"
            return (str(fractions.Fraction(thing.real)) + " + " + str(fractions.Fraction(thing.imaginary)) + "i").replace("+ -","- ")
        if options["display"] == "SCI": 
            if thing.imaginary == 0:
                return format(thing.real, '.{}f'.format(options["display_prec"]))
            elif thing.real == 0:
                return format(thing.imaginary, '.{}f'.format(options["display_prec"])) + "i"
            return (format(thing.real, '.{}f'.format(options["display_prec"])) + " + " + format(thing.imaginary, '.{}f'.format(options["display_prec"])) + "i" + "i").replace("+ -","- ")
    return str(thing)
    
