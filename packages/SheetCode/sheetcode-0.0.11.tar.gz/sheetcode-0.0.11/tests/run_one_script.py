import os
import importlib
import sys

sys.path.append("src/SheetCode")

# Set global constants
os.environ["TEST_SHEETS_PATH"] = "sheets"
os.environ["TRACEABILITY_PATH"] = "traceability"
os.environ["RVT_FILEPATH"] = "../../../../DAA-000048 RVT/2A - Ongoing/DAA-000048_2A.xlsm"
os.environ["PARAMETERS_FILEPATH"] = "../Traceability/A-0000175109 1B App A_Traceability_RBC_9.4.0.xlsm"
os.environ["MODE"] = "Execution" # Specification or Execution


# Set folder where .py scripts are located
scriptsDirectory = "scripts"

scriptName = "Example"

script = importlib.import_module(f"{scriptsDirectory}.{scriptName}")
