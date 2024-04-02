-- Test button NC
Report.Info("")
Report.Info("Press BTNNAME")
WaitForNoContinuity("Wait for no continuity", "Press BTNNAME", POINT1, POINT2, 'msr', {i = 100 mA, tare = {mode='system'}}, 1);
Report.Info("POINT1 -> POINT2")