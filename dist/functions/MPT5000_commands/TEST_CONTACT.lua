-- Continuity Test
Report.Info("")
ContinuitySetup = {
  setup = {i = 100 mA, v = 5 V, tare = {mode = 'system'}},
  criteria = {r < 1 Ohm},
}
Continuity('Test Continuity', 'hcs', ContinuitySetup)