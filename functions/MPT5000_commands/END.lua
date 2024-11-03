-- Test Result
Report.Info("")
if Failed() then
  SetResults.Add.Fail()
  Beep(100)
  Sleep(0.05)
  Beep(100)
  Sleep(0.05)
  Beep(100)
  Report.Fail("*Test Result: Failed")
else
  SetResults.Add.Pass()
  Beep(1000)
  Report.Pass("Test Result: Passed")
end