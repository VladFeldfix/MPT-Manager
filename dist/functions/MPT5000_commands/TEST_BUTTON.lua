-- Test button
Report.Info("")
Report.Info("Testing button BTNNAME")
WaitForContinuity("Testing continuity POINT1 -> POINT2", "Press button BTNNAME", POINT1, POINT2, 'msr', {i = 100 mA, tare = {mode='system'}}, 1);
WaitForNoContinuity("Testing isolation POINT1 -> POINT2", "Release button BTNNAME", POINT1, POINT2, 'msr', {i = 100 mA, tare = {mode='system'}}, 1);
ClearAllPoints()