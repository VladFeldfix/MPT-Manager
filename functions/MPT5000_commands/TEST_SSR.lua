//TEST SSR
LoadHTML("SSRNAME Instructions.html")
PrintLn(CON + DSK,": TEST SSRNAME");
PrintLn(CON + DSK,"Test crocodile connection to SSR");
SetConductor(HC, Pass < 1 Ohm, I = 100 mA, V = 5 Volts);
Continuity(INPUT4, PROBE2);
Continuity(OUTPUT1, PROBE1);
PrintLn(CON + DSK,"TEST SSRNAME POWER ON");
SetPS(V = 5 Volts, I = 0.01 Amps);
PowerOn((INPUT3, OUTPUT2),(INPUT4));
Delay(1000);
PSV();
PSI(Min = 0.005 Amps, Max = 0.03 Amps);
If(FAILED){
    PrintLn("SSRNAME not working!");
    Abort();
}
SetReadVolts(MIN = 4 Volts, MAX = 6 Volts);
ReadVolts((PROBE1), (PROBE2)); // OUTPUT1 -> PROBE1, INPUT4 -> PROBE2
PowerOff();