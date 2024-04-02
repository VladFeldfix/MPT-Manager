-- HiPot Test
Report.Info("")
HiPotSetup = {
  setup = {v = 500, dwell = 1s},
  criteria = {r > 100 MOhm},
}
Hipot('Test HiPot DC', 'hvdc', HiPotSetup, "all")