-- Test switch
Report.Info("")
Report.Info("Testing switch SWNAME")
WaitForContinuity("Testing continuity POINT1 -> POINT2", "Set switch SWNAME to position POSITION", POINT1, POINT2, 'msr', {i = 100 mA, tare = {mode='system'}}, 1);
ClearAllPoints()