-- Point to point test
Report.Info("")
Report.Info("Testing contact from POINT1 to POINT2")
WaitForContinuity("Testing continuity POINT1 -> POINT2", "Contact Point: PROBE to Point: POINT1", PROBE, POINT2, 'msr', {i = 100 mA,  tare = {mode='fixed', data = {res = 2 Ohm}}},1)
Beep(100)
ClearAllPoints()