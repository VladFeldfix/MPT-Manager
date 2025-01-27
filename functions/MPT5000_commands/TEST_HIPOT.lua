-- HiPot Test
Report.Info("")
HiPotSetup = {
  setup = {v = 500 V, dwell = 1s},
  criteria = {r > 100 MOhm},
}
if Failed() then
else
Hipot('#X Test HiPot DC', 'hvdc', HiPotSetup, 'all')
end