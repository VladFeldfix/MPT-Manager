-- HiPot Test
Report.Info("")
HiPotSetupTRD = {
  setup = {v = 500 V, dwell = 1s},
  criteria = {r > 100 MOhm},
}
Hipot('Test HiPot DC', 'hvdc', HiPotSetup, 'all')