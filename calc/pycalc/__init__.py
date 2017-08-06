"""The actual calculation class"""
from complexdecimal import ComplexDecimal
import constants, safe
from functions import *
import re, decimal, time, render
import threading, Queue
from multiprocessing import Process

def computeEquation(m,opt={ }):
    options = {}
    options["prec"] = opt.get("prec") or 28                 #DONE
    options["Emin"] = opt.get("Emin") or -999999999         #DONE
    options["Emax"] = opt.get("Emax") or 999999999          #DONE
    options["easter_egg"] = opt.get("easter_egg") or True   #DONE
    options["safe"] = opt.get("safe") or False              #DONE
    options["trig"] = opt.get("trig") or "RAD"              #DONE
    constant = opt.get("constants") or constants.constants
    
    #Remove any extra white space
    m = m.lstrip().rstrip()
    decimal.getcontext().Emax = options["Emax"]
    decimal.getcontext().Emin = options["Emin"]
    decimal.getcontext().prec = options["prec"]
    
    if options["easter_egg"] and m != "":
        #Answer the meaning of life
        m1 = m.lower()
        if "answer to the ultimate question of life the universe and everything".startswith(m1.strip(",")):
            return ComplexDecimal("42")
        elif "answer to life the universe and everything".startswith(m1.strip(",")):
            return ComplexDecimal("42")
        elif "the meaning of life the universe and everything".startswith(m1.strip(",")):
            return ComplexDecimal("42")
        #Blue moon
        elif m1 == "once in a blue moon":
            return ComplexDecimal("1.16699016") * ComplexDecimal("10")**ComplexDecimal("-8")
        #Misc
        elif m1 == "the number of horns on a unicorn":
            return ComplexDecimal("1")
        elif m1 in ["what is the loneliest number","the loneliest number","loneliest number"]:
            return ComplexDecimal("1")
        elif m1 == "my ass": 
            return ComplexDecimal("Inf")
        
    #Fix e notation
    p = re.compile('([:]?\d*\.\d+|\d+)e([-+]?)([-+]?\d*\.\d+|\d+)'); subst = "(\\1 * 10**\\2\\3)"
    m = re.sub(p, subst, m)
    p = re.compile('([:]?\d*\.\d+|\d+)E([-+]?)([-+]?\d*\.\d+|\d+)'); subst = "(\\1 * 10**\\2\\3)"
    m = re.sub(p, subst, m)
    
    #Replace the constants
    #a) [number]pi : for example
    #b) (something)pi : for example
    #c) varaibles bythemselves, ie pi+pi
    for c in constant:
        m = m.replace("){}".format(c), ") * {}".format(constant[c]))
        p = re.compile('([:]?\d*\.\d+|\d+){}'.format(c)); subst = "\\1 * " + constant[c]
        m = re.sub(p, subst, m)
        m = re.sub('\\b{}\\b'.format(c), constant[c], m)
    
    #Delete unsafe variables
    if options["safe"]:
        for i in safe.unsafe:
            m = m.replace(i,"")
    
    #Fix powers
    m = m.replace("^","**")
    
    #Fix logical operators
    m = m.replace("||"," or ")
    m = m.replace("&&"," and ")
    
    #Change functions into proper forms
    #----------------------------------------------------------------------------------
    #Change double factorials, ie 5!! -> double_fact(5)
    p = re.compile('(-?\d+)!!'); subst = "double_fact(\\1)"; m = re.sub(p, subst, m)
    p = re.compile('\(([^)\n]*?)\)!!'); m = re.sub(p,  "double_fact(\\1)", m)

    #Change factorials, ie 5! -> fact(5)
    p = re.compile('(-?\d+)!'); subst = "factorial(\\1)"; m = re.sub(p, subst, m)
    p = re.compile('\(([^)\n]*?)\)!'); m = re.sub(p,  "factorial(\\1)", m)
    
    #Change percents, ie 5% -> 0.05
    p = re.compile('(-?\d+)%'); subst = "(\\1 / 100)"; m = re.sub(p, subst, m)
    p = re.compile('\(([^)\n]*?)\)%'); m = re.sub(p,  "(\\1 / 100)", m)
    
    p = re.compile('(-?\d+)ppm'); subst = "(\\1 / 1000000)"; m = re.sub(p, subst, m)
    p = re.compile('\(([^)\n]*?)\)ppm'); m = re.sub(p,  "(\\1 / 1000000)", m)
    
    p = re.compile('(-?\d+)ppb'); subst = "(\\1 / 1000000000)"; m = re.sub(p, subst, m)
    p = re.compile('\(([^)\n]*?)\)ppb'); m = re.sub(p,  "(\\1 / 1000000000)", m)
    
    p = re.compile('(-?\d+)ppt'); subst = "(\\1 / 1000000000000)"; m = re.sub(p, subst, m)
    p = re.compile('\(([^)\n]*?)\)ppt'); m = re.sub(p,  "(\\1 / 1000000000000)", m)
    
    #Change absolute value
    m = re.sub("\|(.*?)\|","abs(\\1)",m)
    
    #Fix dates
    m = re.sub("Date\((.*?)\)",'Date("\\1")',m)
    
    #Change choice things like nPr and nCr
    #Regex: (Number)P(Number) = npr(a,b)
    m = re.sub("(-?\d+)P(-?\d+)","nPr(\\1,\\2)",m)
    m = re.sub("(-?\d+)C(-?\d+)","nCr(\\1,\\2)",m)
    
    #Fix trig modes
    if options["trig"] == "DEG":
        m = " "+m
        m = re.sub("asin\((.*?)\)","deg(asin(\\1))",m)
        m = re.sub("acos\((.*?)\)","deg(acos(\\1))",m)
        m = re.sub("atan\((.*?)\)","deg(atan(\\1))",m)
        m = re.sub("[^a]sin\((.*?)\)","sin(rad(\\1))",m)
        m = re.sub("[^a]cos\((.*?)\)","cos(rad(\\1))",m)
        m = re.sub("[^a]tan\((.*?)\)","tan(rad(\\1))",m)
        
        m = re.sub("asinh\((.*?)\)","deg(asinh(\\1))",m)
        m = re.sub("acosh\((.*?)\)","deg(acosh(\\1))",m)
        m = re.sub("atanh\((.*?)\)","deg(atanh(\\1))",m)
        m = re.sub("[^a]sinh\((.*?)\)","sinh(rad(\\1))",m)
        m = re.sub("[^a]cosh\((.*?)\)","cosh(rad(\\1))",m)
        m = re.sub("[^a]tanh\((.*?)\)","tanh(rad(\\1))",m)
    elif options["trig"] == "GRAD":
        m = " "+m
        m = re.sub("asin\((.*?)\)","rad_to_grad(asin(\\1))",m)
        m = re.sub("acos\((.*?)\)","rad_to_grad(acos(\\1))",m)
        m = re.sub("atan\((.*?)\)","rad_to_grad(atan(\\1))",m)
        m = re.sub("[^a]sin\((.*?)\)","sin(grad_to_rad(\\1))",m)
        m = re.sub("[^a]cos\((.*?)\)","cos(grad_to_rad(\\1))",m)
        m = re.sub("[^a]tan\((.*?)\)","tan(grad_to_rad(\\1))",m)
        
        m = re.sub("asinh\((.*?)\)","rad_to_grad(asinh(\\1))",m)
        m = re.sub("acosh\((.*?)\)","rad_to_grad(acosh(\\1))",m)
        m = re.sub("atanh\((.*?)\)","rad_to_grad(atanh(\\1))",m)
        m = re.sub("[^a]sinh\((.*?)\)","sinh(grad_to_rad(\\1))",m)
        m = re.sub("[^a]cosh\((.*?)\)","cosh(grad_to_rad(\\1))",m)
        m = re.sub("[^a]tanh\((.*?)\)","tanh(grad_to_rad(\\1))",m)
        
    #Converts all remaining numbers into numbers
    p = re.compile('([:]?\d*\.\d+|\d+)'); subst = "ComplexDecimal('\\1')"
    m = re.sub(p, subst, m)
    
    #Fix i
    m = m.replace(")i", ") * {}".format("ComplexDecimal(0,1)"))
    p = re.compile('([:]?\d*\.\d+|\d+)i'); subst = "\\1 * " + "ComplexDecimal(0,1)"
    m = re.sub(p, subst, m)
    m = re.sub('\\b{}\\b'.format("i"), "ComplexDecimal(0,1)", m)

    result = eval(m, {"__builtins__": None}, safe.safe_dict)
    return result
    
#print computeEquation("lcm(-1,55.587987)")
#print computeEquation("uniform(10)")

   
def phraseTextMath(string,opt={}):
    """Compute the thing with options and stuff errr"""
    options = {}
    options["prec"] = opt.get("prec") or 28
    options["Emin"] = opt.get("Emin") or -999999999
    options["Emax"] = opt.get("Emax") or 999999999
    options["easter_egg"] = opt.get("easter_egg") or True
    options["trig"] = opt.get("trig") or "RAD"
    options["safe"] = opt.get("safe") or False
    constant = opt.get("constants") or constants.constants
    
    options["display"] = opt.get("display") or "DEFAULT" #For other thing actually
    options["display_prec"] = opt.get("display_prec") or 10
    options["max_display_prec"] = opt.get("max_display_prec") or 100
    options["errors"] = opt.get("errors") or {
        "divide_zero":"\x02\x034Error: \x0fDivision by zero is undefined",
        "value_error":"\x02\x034Error: \x0fMath domain error",
        "arthm_error":"\x02\x034Error: \x0f[ERROR]",
        "other":"\x02\x034Error: \x0fInvalid input error"
    }
    
    if options["display_prec"] > options["max_display_prec"]:
        return "The max display precision is {}".format(options["max_display_prec"])    
    
    try:
        returned = computeEquation(string,options)   
        
    except ZeroDivisionError as e: return options["errors"]["divide_zero"].replace("[ERROR]",str(e))
    except ValueError as e: return options["errors"]["value_error"].replace("[ERROR]",str(e))
    except ArithmeticError as e: return options["errors"]["arthm_error"].replace("[ERROR]",str(e))
    except Exception as e: 
        print e
        return options["errors"]["other"].replace("[ERROR]",str(e))
    
    return render.render(returned,options) 
    
