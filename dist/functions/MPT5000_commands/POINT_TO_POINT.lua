-- Point to point test
Report.Info("")
WaitForContinuity("Wait for continuity", "Contact Point: PROBE to Point: POINT1", PROBE, POINT2, 'msr', {i = 100 mA, tare = {mode='system'}}, 1);
Report.Info("POINT1 -> POINT2")
Beep(100)