-- Continuity Test
Report.Info("")
ContinuitySetup = {
  setup = {i = 1000 mA, v = 5 V, tare = {mode = 'system'}},
  criteria = {r < 1Ω},
}
Continuity('Test Continuity', 'hcs', ContinuitySetup)