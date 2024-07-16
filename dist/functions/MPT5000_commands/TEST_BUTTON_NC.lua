-- Test button NC
Report.Info("")
Report.Info("Testing button BTNNAME")
WaitForNoContinuity("Testing isolation POINT1 -> POINT2", "Press button BTNNAME", POINT1, POINT2, 'msr', {i = 100 mA, delay = 100ms,  tare = {mode='fixed', data = {res = 2.20Ohm}}},1.6, 1000)
WaitForContinuity("Testing continuity POINT1 -> POINT2", "Release button BTNNAME", POINT1, POINT2, 'msr', {i = 100 mA, delay = 100ms,  tare = {mode='fixed', data = {res = 2.20Ohm}}},1.6, 1000)
ClearAllPoints()