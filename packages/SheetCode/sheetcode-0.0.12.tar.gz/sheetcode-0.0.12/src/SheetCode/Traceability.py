import os
import pandas as pd
from tabulate import tabulate # need pip install tabulate
from termcolor import colored # need pip install termcolor
import warnings
import tempfile
import shutil

SheetReqs = pd.DataFrame(columns=['Coverage', 'Test sheet', 'Line'])
SheetParams = pd.DataFrame(columns=['Coverage', 'Test sheet', 'Line'])

def RequirementsFilepath():
    return os.path.join(os.environ["TRACEABILITY_PATH"], 'requirements.xlsx')

def ParametersFilepath():
    return os.path.join(os.environ["TRACEABILITY_PATH"], 'parameters.xlsx')

def Clear():
    if os.path.exists(RequirementsFilepath()):
        os.remove(RequirementsFilepath())    
    if os.path.exists(ParametersFilepath()):
        os.remove(ParametersFilepath())   

def AddRequirement(reqId, sheet, line):
    CheckRequirementSyntax(sheet, reqId)
    SheetReqs.loc[len(SheetReqs.index)] = [reqId, sheet, line]

def AddParameter(xpath, sheet, line):
    CheckParameterSyntax(sheet, xpath)
    SheetParams.loc[len(SheetParams.index)] = [xpath, sheet, line]

def CheckRvtCoverage(sheetName):
    _CheckCoverage(sheetName, SheetReqs, os.environ["RVT_FILEPATH"], "RVT", 3, "Req ID", "Req Text", "Test Sheet Name", None)

def CheckParametersCoverage(sheetName):
    _CheckCoverage(sheetName, SheetParams, os.environ["PARAMETERS_FILEPATH"], "Parameters", 1, "Xpath", None, "Project Test scenario", "Used by project")

def _CheckCoverage(testSheetName, sheetItems, referenceFilepath, referenceSheetName, headerRowIdx, itemIdColumnName, itemTextColumnName, testSheetColumnName, usedColumnName):
    # Check if file exists !
    if not os.path.exists(referenceFilepath): 
        print(colored(f"Can't find {os.path.basename(referenceFilepath)}. Coverage not evaluated for {testSheetName} !", "red", attrs=["bold"]))
        return
        
    # Try to open the file
    try:
        warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
        reference = pd.read_excel(referenceFilepath, sheet_name=referenceSheetName, header=headerRowIdx)
    except:
        print(colored(f"Can't open {os.path.basename(referenceFilepath)}, file is probably opened in Excel. Coverage not evaluated for {testSheetName} !", "red", attrs=["bold"]))
        return
    
    # Get RVT reqs allocated to this sheet
    referenceItems = reference[reference[testSheetColumnName].str.contains(testSheetName, na = False)]

    # Filter Used items (if applicable)
    if usedColumnName != None:
        referenceItems = referenceItems[referenceItems[usedColumnName].str.contains("Yes", na = False) | referenceItems[usedColumnName].str.contains("Always", na = False)]

    # Get Reqs covered by this sheet
    SheetItemsGrouped = sheetItems.groupby("Coverage")["Line"].agg(concatenate_lines).reset_index()

    # Evaluate coverage
    print(colored(f"Coverage against {os.path.basename(referenceFilepath)} for {testSheetName}", "white", attrs=["bold", "underline"]))
    print(f"{len(referenceItems)} items allocated to {testSheetName}")
    notInSheet = referenceItems[~referenceItems[itemIdColumnName].str.lower().isin(SheetItemsGrouped["Coverage"].str.lower())]
    if notInSheet.shape[0] > 0:
        print(colored(f"{notInSheet.shape[0]} items are expected to be covered by this sheet but aren't:", "red", attrs=["bold"]))
        if itemTextColumnName is None:
            # Params
            print(colored(tabulate(notInSheet[[itemIdColumnName]], headers='keys', tablefmt='simple', showindex=False, maxcolwidths=[250, 70]), "red"))
        else:
            # Reqs
            print(colored(tabulate(notInSheet[[itemIdColumnName, itemTextColumnName]], headers='keys', tablefmt='simple', showindex=False, maxcolwidths=[35, 70]), "red"))
    else:
        print(colored(f"All {len(referenceItems)} items covered in {testSheetName}", "green"))

    # Evaluate non-expected items
    notInReference = SheetItemsGrouped[~SheetItemsGrouped["Coverage"].str.lower().isin(referenceItems[itemIdColumnName].str.lower())]
    if notInReference.shape[0] > 0:
        print(colored(f"{notInReference.shape[0]} items appear in the test sheet but are not allocated to it:", "yellow", attrs=["bold"]))
        if itemTextColumnName is None:
            # Params
            print(colored(tabulate(notInReference, headers='keys', tablefmt='simple', showindex=False, maxcolwidths=[250, 40]), "yellow"))
        else:
            # Reqs
            print(colored(tabulate(notInReference, headers='keys', tablefmt='simple', showindex=False, maxcolwidths=[35, 40]), "yellow"))
    
def SaveRvtCoverage(): 
    if os.path.exists(RequirementsFilepath()):
        Reqs = pd.read_excel(RequirementsFilepath())
        # File exists, merge
        mergedReqs = pd.concat([Reqs, SheetReqs])
        mergedReqsGrouped = mergedReqs.groupby(["Coverage"]).agg({"Test sheet": lambda x: '\r\n'.join(map(str, pd.unique(x))), "Line": lambda x: '\r\n'.join(map(str, x))})
        mergedReqsGrouped.to_excel(RequirementsFilepath())
    else:
        # File not yet existing
        SheetReqs.to_excel(RequirementsFilepath())

def SaveParametersCoverage(): 
    if os.path.exists(ParametersFilepath()):
        Params = pd.read_excel(ParametersFilepath())
        # File exists, merge
        mergedParams = pd.concat([Params, SheetParams])
        mergedParamsGrouped = mergedParams.groupby(["Coverage"]).agg({"Test sheet": lambda x: '\r\n'.join(map(str, pd.unique(x))), "Line": lambda x: '\r\n'.join(map(str, x))})
        mergedParamsGrouped.to_excel(RequirementsFilepath())
    else:
        # File not yet existing
        SheetParams.to_excel(ParametersFilepath())

def concatenate_lines(series):
    return ", ".join(map(str, series))

def CheckRequirementSyntax(sheet, reqId):
    if reqId.count('[') == 0:
        raise Exception (f"Missing '[' in {reqId} in {sheet}")
    elif reqId.count('[') > 1:
        raise Exception (f"More than 1 '[' in {reqId} in {sheet}")
    if reqId.count(']') == 0:
        raise Exception (f"Missing ']' in {reqId} in {sheet}")
    elif reqId.count(']') > 1:
        raise Exception (f"More than ']' in {reqId} in {sheet}")
    
def CheckParameterSyntax(sheet, xpath):
    if xpath.count('/') == 0:
        raise Exception (f"No '/' in {xpath} in {sheet}")


    


    


