-- Test button NC
buttonSetup = {i = 0.1, tare = {mode = 'fixed', data = {res = 2.5}}}
WaitForNoContinuity("Press button BTNNAME", POINT1, POINT2, 'msr', buttonSetup, 1);
WaitForContinuity("Release button BTNNAME", POINT1, POINT2, 'msr', buttonSetup, 1);