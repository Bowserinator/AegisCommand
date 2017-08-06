#Convert unit a to b), aie 5 hours to seconds
#Also advanced convert), ie 5 kw/h to j/s^2
#TODO: FIx extra s like meters and stuff
#https://en.wikipedia.org/wiki/List_of_humorous_units_of_measurement
#https://en.wikipedia.org/wiki/Conversion_of_units_of_temperature
#https://en.wikipedia.org/wiki/Conversion_of_units#Energy.2C_work.2C_or_amount_of_heat

#Data to information entropy
#Temp to Newtons (temp newtons, not force newtons)
#IOVOID TEMP UNIT = 1/81 K

class InvalidUnits(Exception):
    pass

from decimal import Decimal
import decimal
decimal.getcontext().Emax = 999999999999999999999999999999999

PREFIXES = {
    "CAPS":["Y","Z","M"], #Caps sensetive prefeies
    'Y' : Decimal(10) ** Decimal(24),  'yotta' : Decimal(10) ** Decimal(24),
    'Z' : Decimal(10) ** Decimal(21),  'zetta' : Decimal(10) ** Decimal(21),
    'E' : Decimal(10) ** Decimal(18),  'exa' : Decimal(10) ** Decimal(18),
    'P' : Decimal(10) ** Decimal(15),  'peta' : Decimal(10) ** Decimal(15),
    'T' : Decimal(10) ** Decimal(12),  'tera' : Decimal(10) ** Decimal(12),
    'G' : Decimal(10) ** Decimal(9),   'giga' : Decimal(10) ** Decimal(9),
    'M' : Decimal(10) ** Decimal(6),   'mega' : Decimal(10) ** Decimal(6),
    'k' : Decimal(10) ** Decimal(3),   'kilo' : Decimal(10) ** Decimal(3),
    'h' : Decimal(10) ** Decimal(2),   'hecto' : Decimal(10) ** Decimal(2),
    'da' : Decimal(10) ** Decimal(1),  'deca' : Decimal(10) ** Decimal(1),
    'd' : Decimal(10) ** Decimal(-1),  'deci' : Decimal(10) ** Decimal(-1),
    'c' : Decimal(10) ** Decimal(-2),  'centi' : Decimal(10) ** Decimal(-2),
    'm' : Decimal(10) ** Decimal(-3),  'milli' : Decimal(10) ** Decimal(-3),
    'u' : Decimal(10) ** Decimal(-6),  'mirco' : Decimal(10) ** Decimal(-6),
    'n' : Decimal(10) ** Decimal(-9),  'nano' : Decimal(10) ** Decimal(-9),
    'p' : Decimal(10) ** Decimal(-12), 'pico' : Decimal(10) ** Decimal(-12),
    'f' : Decimal(10) ** Decimal(-15), 'femto' : Decimal(10) ** Decimal(-15),
    'a' : Decimal(10) ** Decimal(-18), 'atto' : Decimal(10) ** Decimal(-18),
    'z' : Decimal(10) ** Decimal(-21), 'zepto' : Decimal(10) ** Decimal(-21),
    'y' : Decimal(10) ** Decimal(-24), 'yocto' : Decimal(10) ** Decimal(-24),
    
    #Nonstandard
    "double": Decimal(2), "demi":Decimal(0.5), "myrio": Decimal(10000), "myria":Decimal(10000),
    "hella":Decimal(10) ** Decimal(27),
    
    #Binary prefexes
    "ki":Decimal(2)**Decimal(10), "kibi":Decimal(2)**Decimal(10),
    "mi":Decimal(2)**Decimal(20), "mebi":Decimal(2)**Decimal(20),
    "gi":Decimal(2)**Decimal(30), "gibi":Decimal(2)**Decimal(30),
    "ti":Decimal(2)**Decimal(40), "tebi":Decimal(2)**Decimal(40),
    "pi":Decimal(2)**Decimal(50), "pebi":Decimal(2)**Decimal(50),
    "ei":Decimal(2)**Decimal(60), "exbi":Decimal(2)**Decimal(60),
    "zi":Decimal(2)**Decimal(70), "zebi":Decimal(2)**Decimal(70),
    "yi":Decimal(2)**Decimal(80), "yobi":Decimal(2)**Decimal(80),
}

class Unit(object):
    def __init__(self,names,master_unit = "",multi = 1,def_divide=[],def_multi=[]):
        self.names = names
        self.def_divide = def_divide #Define it as division of other units, ie [kg,s,s] = kg/s^2
        self.def_multi = def_multi  #Define as product of other units
        self.master_unit = master_unit #master unit, ie meter, etc...
        self.multi = multi #multi of master unit

#Master unit is meter
#Multi = m * multi = unit

#https://en.wikipedia.org/wiki/Unit_of_length
#and https://en.wikipedia.org/wiki/List_of_unusual_units_of_measurement
#and https://en.wikipedia.org/wiki/List_of_humorous_units_of_measurement
#and http://home.clara.net/brianp/quickref.html
conversionDis = [
    Unit(["m","meter","metre","minecraft block","mc block"]),
    Unit(["Angstrom","A"],"meter",Decimal("10")**Decimal("-10")),
    Unit(["nautical mile"],"meter",Decimal("1852")),
    Unit(["yd","yard"],"meter",Decimal("0.9144")),
    Unit(["ft","feet","foot"],"meter",Decimal("0.3048")),
    Unit(["in","inch"],"meter",Decimal("0.0254")),
    Unit(["mi","mile"],"meter",Decimal("1609.34")),
    Unit(["line"],"meter",Decimal("0.002116666666666666666666666666667")),
    Unit(["light year","l.y","light-year"],"meter",Decimal("9460730472580800")),
    Unit(["AU","astronomical unit","astronomical-unit"],"meter",Decimal("149597870700")),
    Unit(["bhor radius"],"meter",Decimal("0.0000000000529177")),
    Unit(["parsec"],"meter",Decimal("30860000000000000")),
    Unit(["plank length","plank-length"],"meter",Decimal("0.00000000000000000000000000000000001616199")),
    
    #Useless russian units
    Unit(["verst"],"meter",Decimal("1066.8")),
    Unit(["tochka"],"meter",Decimal("0.000254")),
    Unit(["liniya"],"meter",Decimal("0.00254")),
    Unit(["dyuim"],"meter",Decimal("0.0254")),
    Unit(["vershok"],"meter",Decimal("0.04445")),
    Unit(["piad","chetvert"],"meter",Decimal("0.1778")),
    Unit(["fut"],"meter",Decimal("0.3048")),
    Unit(["arshin"],"meter",Decimal("0.7112")),
    Unit(["sazhen"],"meter",Decimal("2.1336")),
    Unit(["milia"],"meter",Decimal("7467.6")),
    
    #Inpractical units I decided to add anyways lol
    Unit(["thou"],"meter",Decimal("0.0254")/Decimal("1000")),
    Unit(["fathom"],"meter",Decimal("1.829")),
    Unit(["cana"],"meter",Decimal("1.5708")),
    Unit(["cubit"],"meter",Decimal("0.5186")),
    Unit(["li"],"meter",Decimal("500")),
    Unit(["barleycorn"],"meter",Decimal("0.0254")/Decimal("3")),
    Unit(["span"],"meter",Decimal("0.0254")*Decimal("9")),
    Unit(["rope"],"meter",Decimal("0.0254")*Decimal("240")),
    Unit(["rod","pole"],"meter",Decimal("0.0254")*Decimal("198")),
    Unit(["palm"],"meter",Decimal("0.0254")*Decimal("3")),
    Unit(["pace"],"meter",Decimal("0.0254")*Decimal("30")),
    Unit(["nail"],"meter",Decimal("0.0254")*Decimal("2.25")),
    Unit(["mil"],"meter",Decimal("0.0254")/Decimal("1000")),
    Unit(["line"],"meter",Decimal("0.0254")/Decimal("10")),
    Unit(["league"],"meter",Decimal("4828.02")),
    Unit(["furlong"],"meter",Decimal("201.168")),
    Unit(["ell"],"meter",Decimal("1.143")),
    Unit(["cable"],"meter",Decimal("219.45600")),
    Unit(["mickey"],"meter",Decimal("0.000127")),
    Unit(["football field"],"meter",Decimal("109.7")),
    Unit(["hair"],"meter",Decimal("0.00008")),
    Unit(["rack","U"],"meter",Decimal("0.04445")),
    Unit(["hand"],"meter",Decimal("0.1016")),
    Unit(["horse"],"meter",Decimal("2.4")),
    Unit(["car"],"meter",Decimal("4")),
    Unit(["sirometer"],"meter",Decimal("149597870700000000")),
    Unit(["light nanosecond","light-nanosecond","l.nm"],"meter",Decimal("0.299792458")),
    Unit(["potrzebie"],"meter",Decimal("0.002263348517438173216473")),
    Unit(["beard-second","beard second"],"meter",Decimal("0.00000001")),
    Unit(["altuve"],"meter",Decimal("1.65")),
    Unit(["smoot"],"meter",Decimal("1.7")),
    Unit(["sheppey"],"meter",Decimal("1400")),
    Unit(["wiffle"],"meter",Decimal("0.089")),
    Unit(["bloit"],"meter",Decimal("1072.89333333")),
    Unit(["bowsermeter","Bm"],"meter",Decimal("43252003274489856000")),
    Unit(["point"],"meter",Decimal("0.0254")/Decimal("72.272")),
    Unit(["shaku"],"meter",Decimal("0.3030303030")),
    Unit(["spat"],"meter",Decimal("1000000000000")),
    Unit(["twip"],"meter",Decimal("0.0254")/Decimal("1440")),
    Unit(["x unit","siegbahn"],"meter",Decimal("1.0021") * Decimal("10")**Decimal("-13")),
]

#https://en.wikipedia.org/wiki/Units_of_information
conversionData = [
    Unit(["bit","sniff"]),
    Unit(["crumb","quad","quarter","tayste","tydbit","seminibble","semi-nibble"],"bit",Decimal("2")),
    Unit(["triad","triade"],"bit",Decimal("3")),
    Unit(["nibble"],"bit",Decimal("4")),
    Unit(["byte","b"],"bit",Decimal("8")),
    Unit(["declet","decle","deckle","dyme"],"bit",Decimal("10")),
    Unit(["wyde","dobulet","plate","playte","chomp","chawmp","word"],"bit",Decimal("16")),
    Unit(["quadlet","dinner","dynner","gawble"],"bit",Decimal("32")),
    Unit(["octlet"],"bit",Decimal("64")),
    Unit(["hexlet","paragraph"],"bit",Decimal("128")),
]

conversionTime = [
    Unit(["second","s","sec"]),
    Unit(["plank-time","plank time"],"second",Decimal("5.39")*Decimal("10")**Decimal("-44")),
    Unit(["jiffy"],"second",Decimal("3")*Decimal("10")**Decimal("-24")),
    Unit(["wink"],"second",Decimal("3.33333333333333333333333333333333")*Decimal("10")**Decimal("-10")),
    Unit(["shake","svedberg"],"second",Decimal("1")*Decimal("10")**Decimal("-8")),
    Unit(["half a minute"],"second",Decimal("30") ),
    Unit(["minute","min"],"second",Decimal("60") ),
    Unit(["moment"],"second",Decimal("90") ),
    Unit(["ke"],"second",Decimal("864") ),
    Unit(["hour","h"],"second",Decimal("3600")),
    Unit(["day","d"],"second",Decimal("86400")),
    Unit(["pentand"],"second",Decimal("86400")*Decimal("5")),
    Unit(["week","sennight"],"second",Decimal("604800")),
    Unit(["fortnight"],"second",Decimal("604800")*Decimal("2")),
    Unit(["lunar month"],"second",Decimal("86400")*Decimal("29.5")),
    Unit(["month"],"second",Decimal("86400")*Decimal("30") + Decimal("36000")), #30 days 10 hours
    Unit(["quarter","season"],"second",Decimal("3")*(Decimal("86400")*Decimal("30") + Decimal("36000")) ), #30 days 10 hours
    
    Unit(["year","yr"],"second",Decimal("86400")*Decimal("365")),
    Unit(["tropical year"],"second",Decimal("86400")*Decimal("365.24219")),
    Unit(["gregorian year"],"second",Decimal("86400")*Decimal("365.2425")),
    Unit(["julian year"],"second",Decimal("86400")*Decimal("365.25")),
    Unit(["sidereal year"],"second",Decimal("86400")*Decimal("365.256363004")),
    Unit(["leap year"],"second",Decimal("86400")*Decimal("366")),
    
    Unit(["biennium"],"second",Decimal("86400")*Decimal("365")*Decimal("2")),
    Unit(["triennium"],"second",Decimal("86400")*Decimal("365")*Decimal("3")),
    Unit(["olympiad"],"second",Decimal("86400")*Decimal("365")*Decimal("4")),
    Unit(["lustrum"],"second",Decimal("86400")*Decimal("365")*Decimal("5")),
    Unit(["decade"],"second",Decimal("86400")*Decimal("365")*Decimal("10")),
    Unit(["indiction"],"second",Decimal("86400")*Decimal("365")*Decimal("15")),
    Unit(["jubilee"],"second",Decimal("86400")*Decimal("365")*Decimal("50")),
    Unit(["century"],"second",Decimal("86400")*Decimal("365")*Decimal("100")),
    Unit(["millennium","kiloannum"],"second",Decimal("86400")*Decimal("365")*Decimal("1000")),
    Unit(["megaannum"],"second",Decimal("86400")*Decimal("365")*Decimal("1000000")), #Might cause problems :(
    Unit(["galatic year"],"second",Decimal("86400")*Decimal("365")*Decimal("230000000")),
    Unit(["gigaannum"],"second",Decimal("86400")*Decimal("365")*Decimal("1000000000")), 
    Unit(["petaannum"],"second",Decimal("86400")*Decimal("365")*Decimal("1000000000000000")), 
    Unit(["eon"],"second",Decimal("3.154") * Decimal("10") ** Decimal("16") ),
    Unit(["friedman"],"second",(Decimal("86400")*Decimal("30") + Decimal("36000")) * Decimal('6')),
    
    Unit(["au time"],"second",Decimal("2.418884254")*Decimal("10")**Decimal("-17")),
    Unit(["helek"],"second",Decimal("3.333333333333333333333333333")),
    Unit(["sigma"],"second",Decimal("1")*Decimal("10")**Decimal("-6")),
    Unit(["zuckerman"],"second",Decimal("0.333333333333333333333333333333333333333")*Decimal("10")**Decimal("-6")),
    Unit(["octaeteris"],"second",Decimal("252.4608")*Decimal("10")**Decimal("6")),
]

conversionAngle = [
    Unit(["degree","deg"]),
    Unit(["turn","cycle","revolution","full circle","rotation"],"degree",Decimal("360")),
    Unit(["quadrant","right angle"],"degree",Decimal("90")),
    Unit(["sextant"],"degree",Decimal("60")),
    Unit(["hexacontade"],"degree",Decimal("6")),
    Unit(["binary degree"],"degree",Decimal("1.40625")),
    Unit(["radian","rad"],"degree",Decimal("180")/Decimal("3.14159265358979323")),
    Unit(["clock","clock position","sign"],"degree",Decimal("30")),
    Unit(["hour angle"],"degree",Decimal("15")),
    Unit(["point","wind"],"degree",Decimal("11.25")),
    Unit(["pechus"],"degree",Decimal("2.5")),
    Unit(["octant"],"degree",Decimal("45")),
    Unit(["diameter part"],"degree",Decimal("0.954929959")),
    Unit(["grad","gradian","grade","gon"],"degree",Decimal("0.9")),
    Unit(["minute of arc","minute arc","arc minute","arcminute"],"degree",Decimal("1")/Decimal("60")),
    Unit(["second of arc","second arc","arc second","arcsecond"],"degree",Decimal("1")/Decimal('3600')),
    Unit(["dms","degree minute second"])
]

#Mass AND WEIGHT CONVERSIONS (Because people are stupid)
conversionMass = [
    Unit(["g","gram","gramme"]), #Gram is base unit now because it doesn't have a multiplier
    Unit(["tonne","metric ton","ton (metric)"],"gram",Decimal("1000000")),
    Unit(["u","atomic mass unit","amu"],"gram",Decimal("1660")*Decimal("10")**Decimal("-27")),
    Unit(["ev","electron volt"],"gram",Decimal("1.7826619")*Decimal("10")**Decimal("-33")),
    Unit(["slug","sl"],"gram",Decimal("14600")),
    Unit(["pound","lb"],"gram",Decimal('453.6')),
    Unit(["plank mass"],"gram",Decimal("2.176")*Decimal("10")**Decimal("-5")),
    Unit(["solar mass"],"gram",Decimal("1.99")*Decimal("10")**Decimal("30")),
    Unit(["newton","n"],"gram",Decimal("9806.65")),
    Unit(["pdl","poundals"],"gram",Decimal("0.138255")*Decimal("9806.65")),
    Unit(["me","mass electron","electron mass"],"gram",Decimal("9.10938291")*Decimal("10")**Decimal("-28")),
    Unit(["mass neutron","neutron mass"],"gram",Decimal("1.675")*Decimal("10")**Decimal("-24")),
    Unit(["mass proton","proton mass"],"gram",Decimal("1.6727")*Decimal("10")**Decimal("-24")),
    Unit(["bag"],"gram",Decimal("60000")),
    Unit(["barge"],"gram",Decimal("20411656.65")),
    Unit(["carat","ct"],"gram",Decimal("0.2")),
    Unit(["clove"],"gram",Decimal("3628.73896")),
    Unit(["crith"],"gram",Decimal("0.0899349")),
    Unit(["dalton","da"],"gram",Decimal("1.660538921")*Decimal("10")**Decimal("-24")),
    Unit(["grave"],"gram",Decimal("1000")),
    Unit(["dram","apothecary"],"gram",Decimal("3.8879346")),
    Unit(["gamma"],"gram",Decimal("10")**Decimal("-6")),
    Unit(["grain"],"gram",Decimal("64.79891")*Decimal("0.001")),
    Unit(["hundred weight","cwt"],"gram",Decimal("1000")*Decimal("50.80234544")),
    Unit(["cental","sh cwt"],"gram",Decimal("1000")*Decimal("45.359237")),
    Unit(["kip"],"gram",Decimal("1000")*Decimal("453.59237")),
    Unit(["mark"],"gram",Decimal("248.8278144")),
    Unit(["mite"],"gram",Decimal("0.001")*Decimal("3.2399455")),
    Unit(["metric mite"],"gram",Decimal("0.001")*Decimal("50")),
    Unit(["ounce","oz"],"gram",Decimal("28")),
    Unit(["pennyweight","dwt","pwt"],"gram",Decimal("1.55517384")),
    Unit(["point"],"gram",Decimal("0.001")*Decimal("2")),
    Unit(["metric pound","livre","pfund"],"gram",Decimal("500")),
    Unit(["quarter"],"gram",Decimal("1000")*Decimal("12.70058636")),
    Unit(["quintal"],"gram",Decimal("1000")*Decimal("100")),
    Unit(["scurple","s ap"],"gram",Decimal("1.2950782")),
    Unit(["sheet"],"gram",Decimal("0.001")*Decimal("647.9891")),
    Unit(["stone","st"],"gram",Decimal("1000")*Decimal("6.35029318")),
    Unit(["weight"],"gram",Decimal("1000")*Decimal("6.35029318")*Decimal("14")),
    Unit(["load"],"gram",Decimal("1000")*Decimal("6.35029318")*Decimal("175")),
    Unit(["last"],"gram",Decimal("1000")*Decimal("1835")),
    Unit(["picul"],"gram",Decimal("1000")*Decimal("60.478982")),
    Unit(["kait","catty"],"gram",Decimal("604.78982")),
    Unit(["tael"],"gram",Decimal("604.78982")/Decimal("16")),
    Unit(["ton"],"gram",Decimal("1000")*Decimal("1016.0469088")),
    Unit(["wey"],"gram",Decimal("1000")*Decimal("114.30527724")),
]

#TODO: volume, area, density, frequency, speed, flow, acceleration, force, temp,
#pressure, torque, energy, power and action, viscoity, kinematic visocity, current, charge,
#dipole, voltage (EMF), resistance, capatiance, magnetic fluc, magnetic flux density, 
#indutance, information entropy
#luminace, luminance flux, illumance, radiation (exposure, source, absorbed, equaivelented dose)
#Encodings, ie decimal->binary, morse code, etc..
#Velocity: add warp factors
allUnits = conversionDis+conversionData+conversionTime+conversionAngle+conversionMass

def getUnit(name,units,doAgain=True):
    name = name.lower()
    for x in units:
        if name.lower() in x.names: return x
    if doAgain: #Do again without SI prefexies
        if prefixed(name,allUnits): name = name.replace(prefixed(name,allUnits),"",1)
        return getUnit(name,units,False)

#TODO CAPS
def prefixed(unit_str,allUnits):
    #allUnits = conversionDis+conversionData+conversionTime+conversionAngle+conversionMass
    for p in PREFIXES:
        for n in allUnits: 
            for name in n.names:
                if p in PREFIXES["CAPS"] and p+name.rstrip() == unit_str.rstrip(): return p.upper()
                elif (p+name).lower().rstrip() == unit_str.lower().rstrip(): 
                    return p.lower()
    return False

        
def getPrefix(unit,allUnits):
    if prefixed(unit,allUnits): 
        try: return PREFIXES[prefixed(unit,allUnits)]
        except: return PREFIXES[prefixed(unit,allUnits).upper()]
    return Decimal("1")
    
def getConvertType(unit,doAgain=True):
    unit = unit.lower().lstrip().rstrip()
    for u in conversionDis: 
        if unit.lower() in u.names: return "distance"
    for u in conversionData: 
        if unit.lower() in u.names: return "data"
    for u in conversionTime: 
        if unit.lower() in u.names: return "time"
    for u in conversionAngle: 
        if unit.lower() in u.names: return "angle"
    for u in conversionMass: 
        if unit.lower() in u.names: return "mass"
    if doAgain: #Do again without SI prefexies
        if prefixed(unit,allUnits): unit = unit.replace(str(prefixed(unit,allUnits)),"",1)
        return getConvertType(unit,False)
    
#Method to convert: 
def convert(value,unit1,unit2):
    convertType = getConvertType(unit1)
    if type(value) == float or type(value) == int:
        value = Decimal(value)
    try: float(value); value = Decimal(value)
    except: pass

    if convertType == "distance":
        return value * getPrefix(unit1,conversionDis) * getUnit(unit1,conversionDis).multi /  getUnit(unit2,conversionDis).multi / getPrefix(unit2,conversionDis)
    if convertType == "data":
        return value * getPrefix(unit1,conversionData) * getUnit(unit1,conversionData).multi /  getUnit(unit2,conversionData).multi / getPrefix(unit2,conversionData)
    if convertType == "time":
        print getPrefix(unit2,conversionAngle)
        return value * getPrefix(unit1,conversionTime) * getUnit(unit1,conversionTime).multi /  getUnit(unit2,conversionTime).multi / getPrefix(unit2,conversionTime)
    if convertType == "mass":
        return value * getPrefix(unit1,conversionMass) * getUnit(unit1,conversionMass).multi /  getUnit(unit2,conversionMass).multi / getPrefix(unit2,conversionMass)
    if convertType == "angle":
        if unit1.lower() == "dms": 
            unit1 = "degree"; value2 = value.replace('"',' ').replace("'"," ").replace("  "," ").split(" ")
            value = Decimal(value2[0]) 
            if len(value2) >= 2: value += Decimal(value2[1])/Decimal("60") 
            if len(value2) == 3: value += Decimal(value2[2])/Decimal("3600")
        if unit2.lower() == "dms": 
            returned = Decimal(value) * getPrefix(unit1,conversionAngle) * getUnit(unit1,conversionAngle).multi /  getUnit("degree",conversionAngle).multi 
            mnt,sec = divmod(returned*3600,60); deg,mnt = divmod(mnt,60)
            return str(deg) + "'" + str(mnt) + '"' + str(sec)
        return value * getPrefix(unit1,conversionAngle) * getUnit(unit1,conversionAngle).multi /  getUnit(unit2,conversionAngle).multi / getPrefix(unit2,conversionAngle)
    raise InvalidUnits("Invalid units found")

