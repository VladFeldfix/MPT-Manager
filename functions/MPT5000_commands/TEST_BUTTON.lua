-- Test button
Report.Info("")
Report.Info("#X Testing button BTNNAME")
WaitForContinuity("Testing continuity POINT1 -> POINT2", "Press button BTNNAME", POINT1, POINT2, 'msr', {i = 100 mA,  tare = {mode='fixed', data = {res = 2 Ohm}}},1)
WaitForNoContinuity("Testing isolation POINT1 -> POINT2", "Release button BTNNAME", POINT1, POINT2, 'msr', {i = 100 mA,  tare = {mode='fixed', data = {res = 2 Ohm}}},10)
ClearAllPoints()