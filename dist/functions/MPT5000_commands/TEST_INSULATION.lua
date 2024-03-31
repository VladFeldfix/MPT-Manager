-- Isolation Test
Report.Info("")
IsolationSetup = {
  setup = {i = 1 uA, tare = {mode = 'system'}},
  criteria = {r > 100 kΩ},
  diagnose = {scan = 'linear'},
}
Isolation('Test Isolation', 'msr', IsolationSetup, 'all')