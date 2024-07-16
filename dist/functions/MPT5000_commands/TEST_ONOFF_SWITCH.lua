-- Test ON-OFF switch
Report.Info("")
Report.Info("Testing switch SWNAME")
WaitForContinuity("Testing continuity POINT1 -> POINT2", "Set switch SWNAME to position ON", POINT1, POINT2, 'msr', {i = 100 mA, delay = 100ms,  tare = {mode='fixed', data = {res = 2.20Ohm}}},1.6, 1000)
WaitForNoContinuity("Testing isolation POINT1 -> POINT2", "Set switch SWNAME to position OFF", POINT1, POINT2, 'msr', {i = 100 mA, delay = 100ms,  tare = {mode='fixed', data = {res = 2.20Ohm}}},1.6, 1000)
ClearAllPoints()