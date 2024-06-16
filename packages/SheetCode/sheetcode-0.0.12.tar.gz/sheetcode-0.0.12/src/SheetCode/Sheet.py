import os
from openpyxl.workbook import Workbook # need pip install openpyxl
from pathlib import Path
from src.SheetCode import Traceability as Traceability

from termcolor import colored # need pip install termcolor
from src.SheetCode import Formatters as Formatters
from enum import Enum


class Sheet:
    global TsWorkbook
    global Ts

    # Attributes
    global Name
    global Reference
    global Version
    global Description
    global StartConditions
    global Logs

    # Sheet state
    class SheetStates(Enum):
        INIT = 1
        CASE = 2
        ACTION = 3
        EXPECTED_RESULT = 4
        RESULT = 5

    global SheetState

    class SheetStatistics:
        PassedCount = 0
        FailedCount = 0

    global Statistics

    global GlobalStatus

    CaseNr = 0
    ActionNr = 0
    ExpectedResultNr = 0
    LineNr = 0
       
    FIRST_CASE_LINE = 18

    class Log:
        global Type
        global Filename

        def __init__(self, type, filename):
            Type = type
            Filename = filename
    
    def __init__(self, prefix, name):
        """ Create a new test sheet with reference set to <prefix>_<name>
        The prefix is typically the identifier of the test specifcation (e.g. RBC_DV_RM for 'RBC Data Validation Route Map').
        The name is the name of the test sheet (e.g. RT_EXIT for 'Exit routes')"""
        self.Reference = f"{prefix}_{Path(name).stem}"
        mode = os.environ["MODE"]
        print(colored(f"Creating sheet '{self.Reference}' in '{mode}' mode", "blue"))

        self.Version = "<Undefined>"
        self.Description = "<Undefined>"
        self.StartConditions = "<Undefined>"
        self.Logs = []

        self.TsWorkbook = Workbook()
        self.Ts = self.TsWorkbook.active
        
        self.CaseNr = 0
        self.ActionNr = 0
        self.ExpectedResultNr = 0
        self.LineNr = self.FIRST_CASE_LINE

        self.GlobalStatus = None

        self.SheetState = self.SheetStates.INIT
        self.Statistics = self.SheetStatistics()
    
    def Case(self, text):
        """ Create a new 'Case' step in the test sheet with specified 'text'"""

        self._AllowSheetState(self.SheetState.CASE)
        
        self.CaseNr +=1
        textRange = f"C{self.LineNr}:H{self.LineNr}"
        Formatters.SetBorder(self.Ts, textRange, Formatters.BORDERS_ALL)
        self.Ts.merge_cells(textRange)
        Formatters.SetCell(self.Ts, f"B{self.LineNr}", chr(64 + self.CaseNr), Formatters.CASE_COLOR, Formatters.BORDERS_ALL)
        Formatters.SetCell(self.Ts, f"C{self.LineNr}", text, Formatters.CASE_COLOR, Formatters.BORDERS_ALL)
        self.LineNr +=1
        self.ActionNr = 0
    
    def Action(self, text):
        """ Create a new 'Action' step in the test sheet with specified 'text'"""

        self._AllowSheetState(self.SheetState.ACTION)

        self.ActionNr +=1
        Formatters.SetCell(self.Ts, f"B{self.LineNr}", self.ActionNr, None, Formatters.BORDERS_LEFT_RIGHT_TOP)
        Formatters.SetCell(self.Ts, f"C{self.LineNr}", text, None, Formatters.BORDERS_LEFT_RIGHT_TOP)
        self.ExpectedResultNr = 0
    
    def ExpectedResult(self, text, requirements: list = None, parameters:list = None): 
        """ Create a new 'Expected result' associated to the last 'Action' with specified 'text'
        Optionally, you can pass:
         - The 'requirements' argument containing a list of Req ID tags with syntax [xxxx]
         - The 'parameters' argument containing a list of Xpath tags with syntax <Xpath>
        Note: Make sure the syntax of the requirements & parameters is correct otherwise exceptions will be thrown """

        self._AllowSheetState(self.SheetState.EXPECTED_RESULT)
        
        self.ExpectedResultNr += 1
        # Format cells below action
        if self.Ts[f"B{self.LineNr}"].value is None:
            self.Ts[f"B{self.LineNr}"].border = Formatters.BORDERS_LEFT_RIGHT
            self.Ts[f"C{self.LineNr}"].border = Formatters.BORDERS_LEFT_RIGHT
        # Fill expected result
        Formatters.SetCell(self.Ts, f"D{self.LineNr}" , text, None, Formatters.BORDERS_LEFT_RIGHT_TOP)

        # Fill covers
        if requirements != None:
            Formatters.SetCell(self.Ts, f"H{self.LineNr}", '\n'.join(requirements), None, Formatters.BORDERS_ALL) 
        
        Formatters.SetBorder(self.Ts, f"D{self.LineNr}:H{self.LineNr}", Formatters.BORDERS_LEFT_RIGHT_TOP)
        self.LineNr +=1

        # Update traceability
        if parameters != None:
            for parameter in parameters:
                Traceability.AddParameter(parameter, self.Reference, self.LineNr)
        if requirements != None:
            for requirement in requirements:
                Traceability.AddRequirement(requirement, self.Reference, self.LineNr)
    
    def Result(self, isPassed: bool, comment: str = "") :
        """ Writes the result of the test, if MODE = 'Execution'
        The 'isPassed' argument is mandatory and shall be set to True if test is passed, False if not.
        Optionally, you can pass the 'comment' argument with a string providing details on the test result."""
        if os.environ["MODE"].lower() == "specification": return

        self._AllowSheetState(self.SheetState.RESULT)
        
        self.LineNr -=1
        
        if isPassed:
            Formatters.SetCell(self.Ts, f"E{self.LineNr}", "Passed", None, Formatters.BORDERS_ALL) 
            Formatters.SetFont(self.Ts, f"E{self.LineNr}", '0000AF00')

            print(colored(f"Line {self.LineNr}: Case {chr(64 + self.CaseNr)}, Action {self.ActionNr}, Expected Result {self.ExpectedResultNr} - Passed - {comment}", "green"))

            if self.GlobalStatus == None: self.GlobalStatus = True
            self.Statistics.PassedCount += 1

        else:
            Formatters.SetCell(self.Ts, f"E{self.LineNr}", "Failed", None, Formatters.BORDERS_ALL)  
            Formatters.SetFont(self.Ts, f"E{self.LineNr}", '00EF0000', bold = True)

            print(colored(f"Line {self.LineNr}: Case {chr(64 + self.CaseNr)}, Action {self.ActionNr}, Expected Result {self.ExpectedResultNr} - FAILED - {comment}","red"))

            self.GlobalStatus = False
            self.Statistics.FailedCount += 1

        Formatters.SetCell(self.Ts, f"F{self.LineNr}", comment, None, Formatters.BORDERS_ALL)
        Formatters.SetFont(self.Ts, f"F{self.LineNr}", size = 7) 
        
        self.LineNr +=1


    def Save(self, checkRequirementsTraceability = True, checkParametersTraceability = True):
        print(colored(f"Saving sheet '{self.Reference}'", "blue"))

        # Columns width
        self.Ts.column_dimensions['A'].width = 7
        self.Ts.column_dimensions['B'].width = 14
        self.Ts.column_dimensions['C'].width = 56
        self.Ts.column_dimensions['D'].width = 56
        self.Ts.column_dimensions['E'].width = 11
        self.Ts.column_dimensions['F'].width = 33
        self.Ts.column_dimensions['G'].width = 33
        self.Ts.column_dimensions['H'].width = 33
        
        # Content        
        Formatters.SetTitle(self.Ts, 1, self.Name)
        
        Formatters.SetCategory(self.Ts, 3, "Overview")
        
        Formatters.SetLongVariable(self.Ts, 5, "Name", self.Name)
        Formatters.SetLongVariable(self.Ts, 6, "Reference", self.Reference)
        Formatters.SetLongVariable(self.Ts, 7, "Version", self.Version)
        Formatters.SetLongVariable(self.Ts, 8, "Description", self.Description)
        
        Formatters.SetCategory(self.Ts, 11, "Start conditions")

        Formatters.SetCategoryValue(self.Ts, 13, self.StartConditions)
                
        Formatters.SetCategory(self.Ts, 15, "Test execution")
        
        Formatters.SetBoldCell(self.Ts, 'B17',"Step", Formatters.TABLE_COLOR, Formatters.BORDERS_ALL)
        Formatters.SetBoldCell(self.Ts, 'C17',"Action", Formatters.TABLE_COLOR, Formatters.BORDERS_ALL)
        Formatters.SetBoldCell(self.Ts, 'D17',"Expected result",Formatters.TABLE_COLOR, Formatters.BORDERS_ALL)
        Formatters.SetBoldCell(self.Ts, 'E17',"Status", Formatters.TABLE_COLOR, Formatters.BORDERS_ALL)
        Formatters.SetBoldCell(self.Ts, 'F17',"Comment", Formatters.TABLE_COLOR, Formatters.BORDERS_ALL)
        Formatters.SetBoldCell(self.Ts, 'G17',"Test case", Formatters.TABLE_COLOR, Formatters.BORDERS_ALL)
        Formatters.SetBoldCell(self.Ts, 'H17',"Covers", Formatters.TABLE_COLOR, Formatters.BORDERS_ALL)
        
        # Add top border of last step line
        Formatters.SetBorder(self.Ts, f"B{self.LineNr}:H{self.LineNr}", Formatters.BORDERS_TOP)


        # Add global status
        self.LineNr +=2
        Formatters.SetCategory(self.Ts, self.LineNr, "Global Status")
        Formatters.SetLongVariable(self.Ts, self.LineNr + 2, "Status", "Passed" if self.GlobalStatus else "Failed")
        Formatters.SetLongVariable(self.Ts, self.LineNr + 3, "Comment", f"Number of Passed : {self.Statistics.PassedCount}\nNumber of Failed : {self.Statistics.FailedCount}")

        # Check RVT and Parameters coverage (if requested)
        if checkRequirementsTraceability: Traceability.CheckRvtCoverage(self.Reference)
        if checkParametersTraceability: Traceability.CheckParametersCoverage(self.Reference)

        # Save coverage
        Traceability.SaveRvtCoverage()
        Traceability.SaveParametersCoverage()

        # Adjust zoom level
        self.Ts.sheet_view.zoomScale = 85
               
        testSheetsDirectory = os.environ["TEST_SHEETS_PATH"] 
        self.TsWorkbook.save(os.path.join(os. getcwd(), testSheetsDirectory, f"{self.Reference}_{self.Version}.xlsx"))

    def _AllowSheetState(self, newState):
        # Forbidden transitions
        if self.SheetState == self.SheetStates.INIT and newState != self.SheetStates.CASE:
            raise Exception("a 'Case' must be created first.")
        elif self.SheetState == self.SheetStates.CASE and newState == self.SheetStates.CASE:
            raise Exception("a 'Case' must not be empty. You must have called 'Case' twice in a row.")
        elif self.SheetState == self.SheetStates.ACTION and newState == self.SheetStates.ACTION:
            raise Exception("a 'Action' must have at least one 'Expected Result'")
        elif self.SheetState == self.SheetStates.EXPECTED_RESULT and newState != self.SheetStates.RESULT and os.environ["MODE"].lower() == "execution":
            raise Exception("an 'Expected Result' must have a 'Result' in Execution mode")
        elif self.SheetState == self.SheetStates.RESULT and newState == self.SheetStates.RESULT:
            raise Exception("There must be only one 'Result' per 'Expected Result'. You must have called 'Result' twice in a row.")    
        
        if not(newState == self.SheetStates.RESULT and not os.environ["MODE"].lower() == "execution"):
            self.SheetState = newState



        
