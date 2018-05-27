import numpy as np
import re
class PMACParser:
    def __init__(self):
        # The keys are the beginngings of the PMAC expressions
        self.looplevel=0
        self.pmacHandlerMap = {
            "Q" : self.variableHandler,
            "I" : self.variableHandler,
            "P" : self.variableHandler,
            "WHILE" : self.whileHandler,
            "ENDWHILE": self.endwhileHandler,
            "X(.+) Y(.+) Z(.+)": self.moveHandler,
            "X(.+) Y(.+) R(.+)": self.arcrHandler,
            "M32==1": self.laserOnHandler, 
            "M32==0": self.laserOffHandler,
            "Inc":    self.incHandler,
            "Abs":    self.absHandler,
            "Linear": self.linearHander, 
            "Circle": self.circleHandler,
            "IF":     self.ifHandler,
            "ELSE":   self.elseHandler,
            "HOMEZ":  self.homehandler
        }
    
    def convertLine(self, line):
        res=None
        res=""
        for key, callback in self.pmacHandlerMap.items():
            line = line.split(";")[0]
            if re.match(key,line):
                try:
                    res = self._lStr() + callback(line.strip()) + "\n"
                except TypeError:
                    print("Wrong type returned in line {}.".format(line))

        return res
        
    def loopLevelStr(self):
        return " "*4*self.looplevel
    def _lStr(self):
        return self.loopLevelStr()
    
    # Handler
    def variableHandler(self,line):
        return line.lower()

    def whileHandler(self,line):
        line= line.strip()
        res = (re.sub("WHILE\s*\(","while ",line).replace(")",":")).lower()
        self.looplevel= self.looplevel+1
        return res

    def endwhileHandler(self,line):
        self.looplevel= self.looplevel-1
        return ""

    def moveHandler(self,line):
        # Laser object has to exist already
        mv_commands= re.compile("X|\s[YZB]").split(line)
        x_cmd, y_cmd, z_cmd = mv_commands[1:4]
        return "L.move({0}, {1}, {2})".format(
            x_cmd.lower(), y_cmd.lower(), z_cmd.lower()
        )

    def laserOnHandler(self,line):
        return "L.toggle_on_off(True)"
    
    def laserOffHandler(self,line):
        return "L.toggle_on_off(False)"
    
    def linearHander(self, line):
        return "L.moveStyle=Mode.LINEAR"
    def circleHandler(self,line):
        return "L.moveStyle=Mode.CIRCLE"
    def incHandler(self,line):
        return "L.moveRel=True"
    def absHandler(self,line):
        return "L.moveRel=False"
    
    def ifHandler(self,line):
        # if nothing follows after the brackets, look for endif.
        # 
        return ""
    
    def elseHandler(self,line):
        return ""
    def homehandler(self,line):
        return "L.homing()" 
    def arcrHandler(self,line):
        # X(50) Y(50) R(50)
        mv_commands= re.compile("X|\s[YR]").split(line)
        x_cmd, y_cmd, r_cmd = mv_commands[1:4]
        return "L.arcMove({0}, {1}, {2})".format(
            x_cmd.lower(), y_cmd.lower(), r_cmd.lower()
        )

    