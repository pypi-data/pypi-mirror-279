import os
import importlib
from pathlib import Path
import Traceability

# Set global variables
os.environ["TEST_SHEETS_PATH"] = "sheets"
os.environ["TRACEABILITY_PATH"] = "traceability"
os.environ["MODE"] = "Specification" # Specification or Execution

Traceability.Clear()

# Set folder  where .py scripts are located
scriptsDirectory = "scripts"

scriptFilePaths = os.listdir(scriptsDirectory)
for scriptFilepath in scriptFilePaths:
    script = importlib.import_module(f"{scriptsDirectory}.{Path(scriptFilepath).stem}")

