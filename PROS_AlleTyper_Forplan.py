import math
from connect import *
import time
import sys
clr.AddReference("PresentationFramework")
from System.Windows import *

# DEFINE THE CT DENSITY TABLE NAME
densityConversionTable = 'HR_OEB HUsetting'

# DEFINE AN EXTERNAL CONTOUR THRESHOLD LEVEL FOR AUTOSEGMENTATION
externalContourThreshold = -150

# DEFINE A MANDATORY SET OF INITAL STRUCTURES
# ------ PLAN NEEDS TO HAVE THESE STRUCTURES DEFINED BEFORE EXECUTING THE SCRIPT
ctvT = 'CTV-T'
ctvSV = 'CTV-SV' #required in Type B and C plans
ctvE = 'CTV-E' #required in Type N plans
analCanal = 'OR; Anal Canal'
penileBulb = 'OR; Bulbus penis'
rectum = 'OR; Rectum'
bowel = 'OR; Tarm' #only exists for N+ disease
testes = 'OR; Testes'
fiducial1 = 'Stift1' #does not exist for salvage cases
fiducial2 = 'Stift2' #does not exist for salvage cases
fiducial3 = 'Stift3' #does not exist for salvage cases
fiducial4 = 'Stift4' #may or may not exist for any prostate plan
fiducial5 = 'Stift5' #may or may not exist for any prostate plan
fiducial6 = 'Stift6' #may or may not exist for any prostate plan

# DEFINE A STANDARD SET OF ANATOMICAL STRUCTURE NAMES
external = 'External'
femHeadLeft = 'OR; Cap fem dex'
femHeadRight = 'OR; Cap fem sin'
bladder = 'OR; Blaere'
ptvT = 'PTV-T'
ptvSV = 'PTV-SV'
ptvTSV = 'PTV-TSV'
ptvE = 'PTV-E'
hvRect = 'HV-Rectum'
marker1 = 'Mark_1'
marker2 = 'Mark_2'
marker3 = 'Mark_3'
marker4 = 'Mark_4'
marker5 = 'Mark_5'
marker6 = 'Mark_6'

# DEFINE A STANDARD SET OF STRUCTURE COLOURS
#---- see for example colour charts at http://www.rapidtables.com/web/color/RGB_Color.htm
colourBladder = "0,153,0"
colourRectum = "0,102,0"
colourBowel = "0,204,0"
colourCaputFemori = "0,51,0"
colourPtvT = "178,102,255"
colourPtvSV = "204,153,255"
colourPtvTSV = "153,51,255"
colourPtvE = "229,204,255"
colourMarker1 = "0,51,25"
colourMarker2 = "255,128,0"
colourMarker3 = "255,153,255"
colourMarker4 = "204,255,153"
colourMarker5 = "0,102,102"
colourMarker6 = "102,0,102"


def CreateWallHvRectum():
# 7) rectal help volume
	with CompositeAction('ROI Algebra (HV-Rectum)'):
		#HV-Rectum
		try:
			r7 = patient.PatientModel.CreateRoi(Name=hvRect, Color="Red", Type="Organ", TissueName=None, RoiMaterial=None)
			r7.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [rectum], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 1.0, 'Posterior': 1.0, 'Right': 1.0, 'Left': 1.0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [rectum], 'MarginSettings': { 'Type': "Contract", 'Superior': 0, 'Inferior': 0, 'Anterior': 1.0, 'Posterior': 1.0, 'Right': 1.0, 'Left': 1.0 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r7.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to generate HV-Rectum. Continues...'
#procedure CreateWallHvRectum ends

def OverrideFiducialsDensity():
# 19) creation of density over-rides in concentric rings around a fiducial
	# --- IMPORTANT : CREATE NEW MATERIAL BASED ON ATOMIC COMPOSITIONS OF STANDARD MUSCLE -> copy as SoftTissue with density override 1.060 g/ccm
	#standard muscle is "db.TemplateMaterials[0].Materials[14]"
	patient.PatientModel.CreateMaterial(BaseOnMaterial=db.TemplateMaterials[0].Materials[14], Name = "SoftTissue", MassDensityOverride = 1.060)
	#fiducial number 1
	with CompositeAction('ROI Algebra (Stift1)'):
		try:
			r19 = patient.PatientModel.CreateRoi(Name=marker1, Color=colourMarker1, Type="Marker", TissueName=None, RoiMaterial=None)
			r19.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [fiducial1], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [fiducial1], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.1, 'Inferior': 0.1, 'Anterior': 0.1, 'Posterior': 0.1, 'Right': 0.1, 'Left': 0.1 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r19.SetRoiMaterial(Material = patient.PatientModel.Materials[0])
			r19.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to generate Marker_1 override ROI. Continues...'
	#end of composite action
	try:
		patient.PatientModel.RegionsOfInterest[fiducial1].DeleteRoi()
	except Exception:
		print 'Could not delete fiducial1 ROI. Continues...'
	#fiducial number 2
	with CompositeAction('ROI Algebra (Stift2)'):
		try:
			r19 = patient.PatientModel.CreateRoi(Name=marker2, Color=colourMarker2, Type="Marker", TissueName=None, RoiMaterial=None)
			r19.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [fiducial2], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [fiducial2], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.1, 'Inferior': 0.1, 'Anterior': 0.1, 'Posterior': 0.1, 'Right': 0.1, 'Left': 0.1 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r19.SetRoiMaterial(Material = patient.PatientModel.Materials[0])
			r19.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to generate Marker_2 override ROI. Continues...'
	#end of composite action
	try:
		patient.PatientModel.RegionsOfInterest[fiducial2].DeleteRoi()
	except Exception:
		print 'Could not delete fiducial2 ROI. Continues...'
	#fiducial number 3
	with CompositeAction('ROI Algebra (Stift3)'):
		try:
			r19 = patient.PatientModel.CreateRoi(Name=marker3, Color=colourMarker3, Type="Marker", TissueName=None, RoiMaterial=None)
			r19.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [fiducial3], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [fiducial3], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.1, 'Inferior': 0.1, 'Anterior': 0.1, 'Posterior': 0.1, 'Right': 0.1, 'Left': 0.1 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r19.SetRoiMaterial(Material = patient.PatientModel.Materials[0])
			r19.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to generate Marker_3 override ROI. Continues...'
	#end of composite action
	try:
		patient.PatientModel.RegionsOfInterest[fiducial3].DeleteRoi()
	except Exception:
		print 'Could not delete fiducial3 ROI. Continues...'
	#fiducial number 4
	with CompositeAction('ROI Algebra (Stift4)'):
		try:
			r19 = patient.PatientModel.CreateRoi(Name=marker4, Color=colourMarker4, Type="Marker", TissueName=None, RoiMaterial=None)
			r19.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [fiducial4], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [fiducial4], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.1, 'Inferior': 0.1, 'Anterior': 0.1, 'Posterior': 0.1, 'Right': 0.1, 'Left': 0.1 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r19.SetRoiMaterial(Material = patient.PatientModel.Materials[0])
			r19.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to generate Marker_4 override ROI. Continues...'
	#end of composite action
	try:
		patient.PatientModel.RegionsOfInterest[fiducial4].DeleteRoi()
	except Exception:
		print 'Could not delete fiducial4 ROI. Continues...'
	#fiducial number 5
	with CompositeAction('ROI Algebra (Stift5)'):
		try:
			r19 = patient.PatientModel.CreateRoi(Name=marker5, Color=colourMarker5, Type="Marker", TissueName=None, RoiMaterial=None)
			r19.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [fiducial5], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [fiducial5], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.1, 'Inferior': 0.1, 'Anterior': 0.1, 'Posterior': 0.1, 'Right': 0.1, 'Left': 0.1 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r19.SetRoiMaterial(Material = patient.PatientModel.Materials[0])
			r19.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to generate Marker_5 override ROI. Continues...'
	#end of composite action
	try:
		patient.PatientModel.RegionsOfInterest[fiducial5].DeleteRoi()
	except Exception:
		print 'Could not delete fiducial5 ROI. Continues...'
	#fiducial number 6
	with CompositeAction('ROI Algebra (Stift6)'):
		try:
			r19 = patient.PatientModel.CreateRoi(Name=marker6, Color=colourMarker6, Type="Marker", TissueName=None, RoiMaterial=None)
			r19.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [fiducial6], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [fiducial6], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.1, 'Inferior': 0.1, 'Anterior': 0.1, 'Posterior': 0.1, 'Right': 0.1, 'Left': 0.1 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r19.SetRoiMaterial(Material = patient.PatientModel.Materials[0])
			r19.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to generate Marker_6 override ROI. Continues...'
	#end of composite action
	try:
		patient.PatientModel.RegionsOfInterest[fiducial6].DeleteRoi()
	except Exception:
		print 'Could not delete fiducial6 ROI. Continues...'
#procedure OverrideFiducialsDensity ends



#### ALL-PROSTATES PLAN PREPARATION : CONTOURING COMPLETION SCRIPT BEGINS HERE

# Define null filter
filter = {}

# Get handle to patient db
db = get_current('PatientDB')

# Define patient and examination handles
patient = get_current('Patient')
examination = get_current('Examination')

# RESET current simulation modality to the REQUIRED HU-DENSITY MAPPING
examination.EquipmentInfo.SetImagingSystemReference(ImagingSystemName = densityConversionTable)
#patient.Save()

# EXTERNAL body contour will be created using threshold-based segmentation
with CompositeAction('Create External (External)'):
	patient.PatientModel.CreateRoi(Name=external, Color="Orange", Type="External", TissueName=None, RoiMaterial=None)
	patient.PatientModel.RegionsOfInterest[external].CreateExternalGeometry(Examination=examination, ThresholdLevel=externalContourThreshold)
	# CompositeAction ends 

# FEMORALS HEADS and BLADDER will be approximated using built-in MALE PELVIS Model Based Segmentation
get_current("ActionVisibility:Internal") # needed due to that MBS actions not visible in evaluation version.
patient.PatientModel.MBSAutoInitializer(MbsRois=[
	{ 'CaseType': "PelvicMale", 'ModelName': "Bladder", 'RoiName': bladder, 'RoiColor': colourBladder },
	{ 'CaseType': "PelvicMale", 'ModelName': "FemoralHead (Left)", 'RoiName': femHeadLeft, 'RoiColor': colourCaputFemori }, 
	{ 'CaseType': "PelvicMale", 'ModelName': "FemoralHead (Right)", 'RoiName': femHeadRight, 'RoiColor': colourCaputFemori }],
	CreateNewRois=True, Examination=examination, UseAtlasBasedInitialization=True)
# adapt model based segmentation for bladder and femoral heads
patient.PatientModel.AdaptMbsMeshes(Examination=examination, RoiNames=[bladder, femHeadLeft, femHeadRight], CustomStatistics=None, CustomSettings=None)
#patient.Save()


# GROW DENSITY OVERRIDE REGION AROUND IMPLANTED GOLD MARKERS
OverrideFiducialsDensity()

# GROW RECTAL HELP VOLUME FOR IGRT
CreateWallHvRectum()

# PLAN PREPARATION COMPLETE - save the active plan and manually check/edit plan before inverse planning
patient.Save()





 

