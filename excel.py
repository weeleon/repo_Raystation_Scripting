import clr, sys
from connect import *

clr.AddReference("Office")
clr.AddReference("Microsoft.Office.Interop.Excel")

import Microsoft.Office.Interop.Excel as interop_excel

import System.Array


#open an excel worksheet
excel = interop_excel.ApplicationClass(Visible = True)
wbook = excel.Workbooks.Add(interop_excel.XlWBATemplate.xlWBATWorksheet)

wsheet = wbook.Worksheets[1]

def create_array(m,n):
	dims = System.Array.CreateInstance(System.Int32,2)
	dims[0] = m
	dims[1] = n
	return System.Array.CreateInstance(System.Object, dims)


# from connect get required handles
patient_db = get_current('PatientDB')

try:
	patient = get_current('Patient')
except:
	print 'There does not appear to be an active patient - exiting system'
	sys.exit()

	
# initialise patient header
patname_head = create_array(2,1)
patname_head[0,0] = patient.PatientName
patname_head[1,0] = patient.PatientID
# add patient header to worksheet
startcell = wsheet.Cells(1,1)
patname_range = wsheet.Range(startcell,startcell.Cells(patname_head.GetLength(0),patname_head.GetLength(1)))
patname_range.Value = patname_head
# initialise worksheet header
header_row = create_array(1,10)
header_row[0,0] = 'ROI'
header_row[0,1] = 'Volume (cc)'
header_row[0,2] = 'D99 (cGy)'
header_row[0,3] = 'D98 (cGy)'
header_row[0,4] = 'D95 (cGy)'
header_row[0,5] = 'Average (cGy)'
header_row[0,6] = 'D50 (cGy)'
header_row[0,7] = 'D2 (cGy)'
header_row[0,8] = 'D1 (cGy)'
header_row[0,9] = 'Plan.Name'
# add header to worksheet
startcell = wsheet.Cells(3,1)
header_range = wsheet.Range(startcell,startcell.Cells(header_row.GetLength(0),header_row.GetLength(1)))
header_range.Value = header_row


#loop over all plans in the patient root
p = 0
startrow = 4
while p < patient.TreatmentPlans.Count:
	#do something over all plans belonging to this patient
	plan = patient.TreatmentPlans[p]
	# --- do what?
	planName = plan.Name
	# initialise ROI list
	rois = plan.GetStructureSet()
	roi_names = [r.OfRoi.Name for r in rois.RoiGeometries if r.PrimaryShape != None]
	#generate data table
	data_table = create_array(len(roi_names),10)
	for i,r in enumerate(roi_names):
		volume = patient.PatientModel.StructureSets[0].RoiGeometries[r].GetRoiVolume()
		d99, d98, d95, d50, d2, d1 = plan.TreatmentCourse.TotalDose.GetDoseAtRelativeVolumes(RoiName = r, RelativeVolumes = [0.99,0.98,0.95,0.50,0.02,0.01])
		average = plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName = r, DoseType = 'Average')
		data_table[i,0] = r
		data_table[i,1] = volume
		data_table[i,2] = d99
		data_table[i,3] = d98
		data_table[i,4] = d95
		data_table[i,5] = average
		data_table[i,6] = d50
		data_table[i,7] = d2
		data_table[i,8] = d1
		data_table[i,9] = planName
	# add data table to the open worksheet
	startcell = wsheet.Cells(startrow,1)
	data_range = wsheet.Range(startcell,startcell.Cells(data_table.GetLength(0),data_table.GetLength(1)))
	data_range.Value = data_table
	startrow += len(roi_names)
	# increment counter
	p += 1




#final touch is to autofit all column widths
wsheet.Columns.AutoFit()

	




