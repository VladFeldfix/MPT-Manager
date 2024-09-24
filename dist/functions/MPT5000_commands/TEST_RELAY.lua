-- Test relay
SetHighAuxiliary(INPUT_PLUS)
SetLowAuxiliary(INPUT_MINUS)
SetPPSOn('hcs', {i = 0.02, v = 24})
WaitForContinuity("Wait for continuity between OUTPUT_PLUS - OUTPUT_MINUS", "Testing relay RELAYNAME", OUTPUT_PLUS, OUTPUT_MINUS, 'msr', {i = 100 mA, delay = 100 ms,  tare = {mode='fixed', data = {res = 2 Ohm}}}, 1)
SetPPSOff('hcs')
ClearAllPoints()