-- Test switch
Report.Info("")
Report.Info("Testing switch SWNAME")
Report.Info("Set switch SWNAME to position POSITION")
WaitForContinuity("Wait for continuity", "Set switch SWNAME to position POSITION", POINT1, POINT2, 'msr', {i = 100 mA, tare = {mode='system'}}, 1);
Report.Info("POINT1 -> POINT2")