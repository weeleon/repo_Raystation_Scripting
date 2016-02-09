from connect import *

import clr #.NET common Language runtime
# add references to Windows Forms and Drawing libraries
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
# import classes from the libraries
from System.Drawing import Point
from System.Windows.Forms import Application, Button, Form, Label, TextBox, CheckBox, ComboBox, RadioButton

class MyForm(Form):
	# new class inherits from Form
	def __init__(self):
		self.patient = patient
		self.Text = 'My Form' #title of the new format
		self.AutoSize = True
		labelX1 = Label()
		labelX2 = Label()
		labelX1.Text = 'What is'
		labelX2.Text = 'this?'
		labelX1.Location = Point(15,28)
		labelX2.Location = Point(120,28)
		labelX1.Width = 50
		labelX2.Width = 50
		labelX1.Height = 20
		labelX2.Height = 40
		self.Controls.Add(labelX1)
		self.Controls.Add(labelX2)
		# create a textbox property of the form
		self.textbox1 = TextBox()
		self.textbox1.Location = Point(50,200)
		self.textbox1.Width = 120
		self.textbox1.Height = 50
		self.Controls.Add(self.textbox1)
		# implement an interaction button
		self.button1 = Button()
		self.button1.Text = "Auto-fill current patient name"
		self.button1.Location = Point(50, 120)
		self.button1.Width = 150
		self.button1.Height = 45
		self.Controls.Add(self.button1)
		self.button1.Click += self.button1_clicked
		# add checklist question
		self.question1 = Label()
		self.question1.Text = "Which actions have you finished so far?"
		self.question1.Location = Point(15,280)
		self.question1.AutoSize = True
		self.Controls.Add(self.question1)
		# first checkbox
		self.check1 = CheckBox()
		self.check1.Text = "Patient modelling"
		self.check1.Location = Point(20,310)
		self.check1.AutoSize = True
		self.check1.Checked = False
		self.Controls.Add(self.check1)
		self.check1.CheckedChanged += self.checkedChanged
		# second checkbox
		self.check2 = CheckBox()
		self.check2.Text = "Plan design"
		self.check2.Location = Point(20,340)
		self.check2.AutoSize = True
		self.check2.Checked = False
		self.Controls.Add(self.check2)
		self.check2.CheckedChanged += self.checkedChanged
		# add checklist response message
		self.response1 = Label()
		self.response1.Text = "-"
		self.response1.Location = Point(160,340)
		self.response1.AutoSize = True
		self.Controls.Add(self.response1)
		# generate combobox
		self.question2 = Label()
		self.question2.Text = "Select an ROI"
		self.question2.Location = Point(320,310)
		self.question2.AutoSize = True
		self.Controls.Add(self.question2)
		rois = [r.Name for r in patient.PatientModel.RegionsOfInterest]
		self.combobox = ComboBox()
		self.combobox.Location = Point(320,340)
		self.combobox.DataSource = rois
		self.Controls.Add(self.combobox)
		self.combobox.SelectionChangeCommitted += self.comboSelection
		# generate combobox response
		self.response2 = Label()
		self.response2.Text = ""
		self.response2.Location = Point(320,380)
		self.response2.AutoSize = True
		self.Controls.Add(self.response2)

	# sub action based on clicking the button
	def button1_clicked(self, sender, event):
		#sender and event are dummy for the moment
		self.textbox1.Text = patient.PatientName
	
	# sub action based on status of the checkboxes
	def checkedChanged(self, sender, event):
		if (self.check1.Checked == True) & (self.check2.Checked == True) :
			self.response1.Text = "Ready to plan"
		else:
			self.response1.Text = "-"
	
	# sub action based on combo selection committed
	def comboSelection(self, sender, event):
		selectedRoi = self.combobox.SelectedItem
		roiVolume = patient.PatientModel.StructureSets['CT 1'].RoiGeometries[selectedRoi].GetRoiVolume()
		self.response2.Text = "The volume of the selected ROI "+format(roiVolume)+" cm^3."
		
	



		
#patient_db = get_current('PatientDB')
#myPath = r'S:/Patients'
#patient = get_current("Patient")
#examination = get_current("Examination")

# grab name of current patient
# catch and throw an exception if there is no active patient
try:
	patient = get_current("Patient")
except SystemError:
	raise IOError("No patient currently loaded.")

form = MyForm()
Application.Run(form)







