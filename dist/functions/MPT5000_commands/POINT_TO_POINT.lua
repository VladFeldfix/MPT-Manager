-- Point to point test
Report.Info("")
Report.Info("Testing contact from POINT1 to POINT2")
WaitForContinuity("Testing continuity POINT1 -> POINT2", "Contact Point: PROBE to Point: POINT1", PROBE, POINT2, 'msr', {i = 100 mA, delay = 100ms,  tare = {mode='fixed', data = {res = 2.20Ohm}}},1.6, 1000)
Beep(100)
ClearAllPoints()