import tempfile
from PMACParser import *
import os
from IPython.display import HTML, display
import tabulate as tb

class PMAC2Py:
    def __init__(self, filepath, DEBUG=False):
        self.filepath = filepath
        self.DEBUG=DEBUG
        self.pyfile = tempfile.mkstemp(dir=os.getcwd())[1]
        self.parser = PMACParser()
        
    def __call__(self):    
        self.initHeader()
        self.processFile()
        self.footer()
        
    def initHeader(self):        
        with open("inc/header.py","r") as h, open(self.pyfile,"w") as f_temp:
            f_temp.write(h.read())
            
    def processFile(self):
        with open(self.pyfile,"a") as f_temp, open(self.filepath, "r") as  pmc_file:
#             print([self.parser.convertLine(line) for line in pmc_file.readlines() ])
            f_temp.write(
                "".join(
                    [self.parser.convertLine(line) for line in pmc_file.readlines() ]
                    )
            )
        if self.DEBUG:
            with open(self.filepath, "r") as pmc_file:
                processed_list = [[line, self.parser.convertLine(line)] for line in pmc_file.readlines()]
                # for i,line in enumerate(pmac_str.split("\n")):
                #     print(i, "   ",  line, "   ", pmc.convertLine(line))
                tb.PRESERVE_WHITESPACE = True
                table_str=(tb.tabulate(
                    processed_list,
                    showindex="always",
                    headers=["PMC", "python"],
                ))
                print(table_str)
                
    def footer(self):
        with open("inc/footer.py") as footer, open(self.pyfile, "a") as f_temp:
            f_temp.write(footer.read())
        
            
            