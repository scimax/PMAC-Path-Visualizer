import numpy as np
import re
class PMACParser:
    def __init__(self):
        # The keys are the beginngings of the PMAC expressions
        self.looplevel=0
        self.decrLoopLevel=False
        self.pmacHandlerMap = {
            "Q" : self.variableHandler,
            "I" : self.variableHandler,
            "P" : self.variableHandler,
            "WHILE" : self.whileHandler,
            "ENDWHILE": self.endwhileHandler,
            "X(.+) Y(.+) Z(.+)": self.moveHandler,
            "X(.+) Y(.+) R(.+)": self.arcrHandler,
#             "G1 X(.+) Y(.+) E(.+)": self.cmd,
            "M32==1": self.laserOnHandler, 
            "M32==0": self.laserOffHandler,
            "M49=":   self.variableHandler,
            "Inc":    self.incHandler,
            "Abs":    self.absHandler,
            "Linear": self.linearHander, 
            "Circle": self.circleHandler,
            "IF":     self.ifHandler,
            "ELSE":   self.elseHandler,
            "ENDIF":   self.endIfHandler,
            "HOMEZ":  self.homehandler
        }
        
    
    def convertLine(self, line):
        res=None
        res=""
        line = line.split(";")[0]
        for key, callback in self.pmacHandlerMap.items():
            if re.match(key,line):
                try:
                    res = self._lStr() + callback(line.strip()) + "\n"
                    if self.decrLoopLevel:
                        res=res[4:]
                        self.decrLoopLevel=False
                        
                except TypeError:
                    print("Wrong type returned in line {}.".format(line))

        return res
        
    def loopLevelStr(self):
        return " "*4*self.looplevel
    def _lStr(self):
        return self.loopLevelStr()
    
    # Handler
    def variableHandler(self,line):
        line=re.sub("M49=(.+)", "m49=int(round(\g<1>))", line)
        return line.lower()

    def whileHandler(self,line):
        line= line.strip()
        
        res = (re.sub(r"WHILE\s*\((.+)\)", "while \g<1> :",line)).lower()
        self.looplevel= self.looplevel+1
        return res

    def endwhileHandler(self,line):
        self.looplevel= self.looplevel-1
        return ""

    def moveHandler(self,line):
        # Laser object has to exist already
        mv_commands= re.compile("X|\s[YZB]").split(line)
        x_cmd, y_cmd, z_cmd = mv_commands[1:4]
        return "p211, p212, p213 = L.move({0}, {1}, {2})".format(
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
        if line.find("(B)")!=-1:
            return ""
        else:
            return "L.moveRel=True"
    def absHandler(self,line):
        return "L.moveRel=False"
    
    def ifHandler(self,line):
        # if nothing follows after the brackets, look for endif.
        # 
        s=line.strip()
        ind_cond_start=s.find("(")
        ind_cond_end= s.rfind(")")
        cond=s[ind_cond_start: ind_cond_end+1].replace("=", "==").lower()
        cond=cond.replace("!<", ">=")
        cond=cond.replace("!>", "<=")
        if ind_cond_end==len(s)-1:
        #     looplevel
            self.looplevel= self.looplevel+1
            return "if "+cond + ": "
        else:
            inline_cmd = self.convertLine(s[ind_cond_end+1:].strip())
            return ("if "+cond + ": " + inline_cmd.strip())
    
    def elseHandler(self,line):
        line=line.strip()
        if len(line)==4:
            self.decrLoopLevel = True
            return line.lower()+":"
        # TODO
        return ""
    
    def endIfHandler(self,line):
        self.looplevel= self.looplevel-1
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

    