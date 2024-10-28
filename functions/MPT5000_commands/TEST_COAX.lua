-- Test coax cable COAXNAME
Report.Info("")
Report.Info("Test coax cable COAXNAME")
Report.Info("Measuring DATA resistance")
Report.Info("DATA1 to DATA2")
Report.Info("for coax cable COAXNAME")
SetHigh(DATA1)
SetLow(DATA2)
DataRes = DoResistance('msr', {i = 1mA, delay = 100ms, tare = {mode = 'system'}})
Report.Info("DATA resistance DATA1 to DATA2 = "..DataRes.value_as_str)
ClearAllPoints()

Report.Info("Measuring BRAID resistance")
Report.Info("BRAID1 to BRAID2")
Report.Info("for coax cable COAXNAME")
SetHigh(BRAID1)
SetLow(BRAID2)
BraidRes = DoResistance('msr', {i = 1mA, delay = 100ms, tare = {mode = 'system'}})
Report.Info("BRAID resistance BRAID1 to BRAID2 = "..BraidRes.value_as_str)
ClearAllPoints()

Report.Info("Comparing DATA to BRAID")
if DataRes.value > BraidRes.value then
  Report.Pass('Passed! Signal resistance > braid resistance: ')
  Report.Info(DataRes.value_as_str.." > "..BraidRes.value_as_str)
else
  Report.Fail('* Failed! Signal resistance < braid resistance: ')
  Report.Info(DataRes.value_as_str.." < "..BraidRes.value_as_str)
  SetRessults.Add.Fail()
end