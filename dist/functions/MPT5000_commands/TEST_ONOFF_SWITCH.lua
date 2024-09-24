-- Test ON-OFF switch
Report.Info("")
Report.Info("Testing switch SWNAME")
WaitForContinuity("Testing continuity POINT1 -> POINT2", "Set switch SWNAME to position ON", POINT1, POINT2, 'msr', {i = 100 mA,  tare = {mode='fixed', data = {res = 2 Ohm}}},1)
WaitForNoContinuity("Testing isolation POINT1 -> POINT2", "Set switch SWNAME to position OFF", POINT1, POINT2, 'msr', {i = 100 mA,  tare = {mode='fixed', data = {res = 2 Ohm}}},10)
ClearAllPoints()