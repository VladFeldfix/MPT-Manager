-- Test Result
Report.Info("")
if Failed() then
  SetResults.Add.Fail()
  Report.Info("Test Result: Failed")
else
  SetResults.Add.Pass()
  Report.Info("Test Result: Passed")
end

-- Created with MPT-Manager SOFTWARE_REV on TODAY