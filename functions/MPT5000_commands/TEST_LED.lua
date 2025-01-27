-- Test LED
Report.Info("")
Report.Info("#X Testing LED LEDNAME")
Diode(LEDNAME)
Report.Info("Visual tests")
SetHighAuxiliary(POINT1)
SetLowAuxiliary(POINT2)
SetPPSOn('hcs', {i = 0.01, v = 2.2})
Sleep(1)
LED = ConfirmationPrompt ('Confirm that LEDNAME Dimmer Lamp is COLOR', 'LED Test')
if not LED then Report.Fail('* LED LEDNAME Dimmer Lamp Failed') else Report.Pass('LED LEDNAME Dimmer Lamp Passed') end
SetPPSOff('hcs')
ClearAllPoints()