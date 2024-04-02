-- Test ON-OFF switch
Report.Info("")
Report.Info("Testing switch SWNAME")
Report.Info("Set switch SWNAME to position ON")
WaitForContinuity("Wait for continuity", "Set switch SWNAME to position ON", POINT1, POINT2, 'msr', {i = 100 mA, tare = {mode='system'}}, 1);
Report.Info("POINT1 -> POINT2")
Report.Info("Set switch SWNAME to position OFF")
WaitForNoContinuity("Wait for no continuity", "Set switch SWNAME to position OFF", POINT1, POINT2, 'msr', {i = 100 mA, tare = {mode='system'}}, 1);
Report.Info("POINT1 -> POINT2")