-- open HTML file in another window
if GetGlobalPersist('LastHTML') then lastHTML = GetGlobalPersist('LastHTML') else lastHTML = '' end
if lastHTML ~= 'PARTNUMBER' then
  os.execute('start cmd /k "cd C:/MPT Studio/db/tests/products/HTML/Products & PARTNUMBER.html & exit"')
  LastHTML = 'PARTNUMBER'
  SetGlobalPersist('LastHTML', LastHTML)
end

-- Get Operator Name and Serial Number
if GetPersist('OperatorName') then OperatorName = GetPersist('OperatorName') else OperatorName = 'OperatorName' end 
if GetPersist('SerialNumber') then SerialNumber = GetPersist('SerialNumber') else SerialNumber = 'SerialNumber' end
OperatorName = InputText('Enter Operator Name',OperatorName, 'Operator Name', '')
SetPersist('OperatorName',OperatorName)
SerialNumber = InputText('Enter Serial Number',SerialNumber, 'Serial Number', '')
SetPersist('SerialNumber',SerialNumber)

-- Generate report header
Report.Header('PCBA Part Number',ProductName())
Report.Header('Written by','Vladimir Shishkovsky')
Report.Header('from','FLEX For RAFAEL R&D')
Report.Header('POC on Rafael','FullSurname.FirstName`s FirstLetter.UnitNumber')
Report.Header('Machine Type',"MPT5000")
Report.Header('Customer', "RAFAEL")
Report.Header('Product Name',tostring("PRODUCT_DESCRIPTION"))
Report.Header('Product Part Number',tostring("PARTNUMBER"))
Report.Header('Wiring Diagram',tostring("DRAWING_PN")..' Rev.: '..tostring("DRAWING_REV"))
Report.Header('Test TRD',"PS-39-756948 Rev.: L")
Report.Header('Operator Name',tostring(OperatorName))
Report.Header('Serial Number',tostring(SerialNumber))

-- setup forlder for report file
require "lfs"
rep_new_path = lfs.currentdir()..'\\db\\tests\\results\\'..ProductName()
lfs.mkdir(rep_new_path)
SetReportLocation(rep_new_path)

-- setup report file name
date_stamp = os.date('%d%b%Y')
str_date_stamp = date_stamp.upper(date_stamp)
SetReportFileName(SerialNumber..'_'..str_date_stamp..'_'..ProductName())

-- display Operator Name and Serial Number
Report.Info(OperatorName)
Report.Info(SerialNumber)