-- Continuity Test
Report.Info("")
ContinuitySetup = {
  setup = {i = 1000 mA, v = 5 V, tare = {mode = 'system'}},
  criteria = {r < 1 Ohm},
  options = {use_star_mode = 1}
}
Continuity('Test Continuity', 'hcs', ContinuitySetup)