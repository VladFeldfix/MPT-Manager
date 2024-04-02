-- Test button
Report.Info("")
Report.Info("Press BTNNAME")
WaitForContinuity("Wait for continuity", "Press BTNNAME", POINT1, POINT2, 'msr', {i = 100 mA, tare = {mode='system'}}, 1);
Report.Info("POINT1 -> POINT2")