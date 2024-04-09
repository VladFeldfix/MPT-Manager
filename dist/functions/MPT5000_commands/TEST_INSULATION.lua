-- Isolation Test
Report.Info("")
IsolationSetup = {
  setup = {i = 10 uA, tare = {mode = 'system'}},
  criteria = {r > 100 Ohm},
  diagnose = {},
}
Isolation('Test Isolation', 'msr', IsolationSetup, 'all')