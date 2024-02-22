-- Test SSR
SetHighAuxiliary(INPUT3)
SetLow(AuxiliaryINPUT4)
SetPPSOn('hcs', {i = 0.02, v = 24})
Sleep(300)
SSRSetup = {i = 0.1, tare = {mode = 'fixed', data = {res = 2.5}}}
WaitForContinuity("Wait for continuity", "Testing SSR SSRNAME", OUTPUT1, OUTPUT2, 'msr', SSRSetup, 1)
ClearAllPoints()
SetPPSOff('hcs')