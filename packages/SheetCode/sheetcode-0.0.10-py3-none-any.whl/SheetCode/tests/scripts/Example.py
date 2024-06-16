
from SheetCode import Sheet

sheet = Sheet("FCT", __file__)

sheet.Name = "Buttons and lights"
sheet.Version = "1A"
sheet.Description = ["This test sheets covers the buttons and lights of all colors",
                        "We will test each button and check that the expected lights are lit on"]

sheet.StartConditions = ["No button is pressed",
                         "No light is lit on"]

# *********************************
sheet.Case("Yellow light is managed")

sheet.Action("Press and maintain the yellow button")

sheet.ExpectedResult("The yellow lights turns on and remains on",
                        requirements = ["[SIMPLE_REQ_1]"],
                        parameters = ["parameters/yellow_light_enabled"])
sheet.ExpectedResult("The red light remains off",
                        requirements = ["[SIMPLE_REQ_2]"])

sheet.Action("Release the yellow button")

sheet.ExpectedResult("The yellow light turns off")

# *********************************
sheet.Case("Red light is not managed")

sheet.Action("Press and maintain the red button")

sheet.ExpectedResult("The red light turns DOES NOT turn on",
                        requirements = ["[SIMPLE_REQ_3]"],
                        parameters = ["parameters/red_light_enabled"])

sheet.Action("Release the red button")

sheet.ExpectedResult("The red light remains off")

# *********************************

sheet.Save(checkRequirementsTraceability = True, checkParametersTraceability = True)