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

# DEFINE A SET OF PLANNING HELP STRUCTURES
complementPtvEofTSV = 'PTV-E-(PTV-TSV)'
complementBladderPtvT = 'OR; Blaere-(PTV-T+5mm)'
complementBladderPtvTSV = 'OR; Blaere-(PTV-TSV+5mm)'
complementBladderPtvE = 'OR; Blaere-(PTV-E+5mm)'
complementRectumPtvT = 'OR; Rectum-(PTV-T+5mm)'
complementRectumPtvTSV = 'OR; Rectum-(PTV-TSV+5mm)'
complementRectumPtvE = 'OR; Rectum-(PTV-E+5mm)'
complementBowelPtvTSV = 'OR; Tarm-(PTV-TSV+5mm)'
complementBowelPtvE = 'OR; Tarm-(PTV-E+5mm)'
wallPtvT = 'Wall;(PTV-T)+5mm'
wallPtvTSV = 'Wall;(PTV-TSV)+5mm'
wallPtvE = 'Wall;(PTV-E)+5mm'
transitionTSVtoE = 'PTV-E-(PTV-TSV+8mm)'
complementExternalPtvT = 'External-(PTV-T)'
complementExternalPtvTsv = 'External-(PTV-TSV)'
complementExternalPtvE = 'External-(PTV-E)'

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
colourComplementExternal = "192,192,192"


def InitialiseDensityConversionTable():
	# RESET current simulation modality to the REQUIRED HU-DENSITY MAPPING
	examination.EquipmentInfo.SetImagingSystemReference(ImagingSystemName = densityConversionTable)
#procedure InitialiseDensityConversionTable ends


def CreateExternalBodyContour():
	# EXTERNAL body contour will be created using threshold-based segmentation
	with CompositeAction('Create External (External)'):
		patient.PatientModel.CreateRoi(Name=external, Color="Orange", Type="External", TissueName=None, RoiMaterial=None)
		patient.PatientModel.RegionsOfInterest[external].CreateExternalGeometry(Examination=examination, ThresholdLevel=externalContourThreshold)
#procedure CreateExternalBodyContour ends 


def AutosegmentFemurAndBladder():
	# FEMORALS HEADS and BLADDER will be approximated using built-in MALE PELVIS Model Based Segmentation
	get_current("ActionVisibility:Internal") # needed due to that MBS actions not visible in evaluation version.
	patient.PatientModel.MBSAutoInitializer(MbsRois=[
		{ 'CaseType': "PelvicMale", 'ModelName': "Bladder", 'RoiName': bladder, 'RoiColor': colourBladder },
		{ 'CaseType': "PelvicMale", 'ModelName': "FemoralHead (Left)", 'RoiName': femHeadLeft, 'RoiColor': colourCaputFemori }, 
		{ 'CaseType': "PelvicMale", 'ModelName': "FemoralHead (Right)", 'RoiName': femHeadRight, 'RoiColor': colourCaputFemori }],
		CreateNewRois=True, Examination=examination, UseAtlasBasedInitialization=True)
	# adapt model based segmentation for bladder and femoral heads
	patient.PatientModel.AdaptMbsMeshes(Examination=examination, RoiNames=[bladder, femHeadLeft, femHeadRight], CustomStatistics=None, CustomSettings=None)
#procedure AutosegmentFemurAndBladder ends


#should we check intersection of required volumes with external = 100%?


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
	
	#
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


def CreateMarginPtvT():
# 1) create PTV-T
	with CompositeAction('Create PTV-T'):
		#PTV-T
		try :
			r1 = patient.PatientModel.CreateRoi(Name=ptvT, Color=colourPtvT, Type="PTV", TissueName=None, RoiMaterial=None)
			r1.SetMarginExpression(SourceRoiName=ctvT, MarginSettings={ 'Type': "Expand", 'Superior': 1.0, 'Inferior': 1.0, 'Anterior': 0.7, 'Posterior': 0.7, 'Right': 0.7, 'Left': 0.7 })
			r1.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create PTV-T. Continues...'
#procedure CreateMarginPtvT ends

def CreateMarginPtvSV():
# 2) create PTV-SV
	with CompositeAction('Create PTV-SV'):
		#PTV-SV
		try :
			r2 = patient.PatientModel.CreateRoi(Name=ptvSV, Color=colourPtvSV, Type="PTV", TissueName=None, RoiMaterial=None)
			r2.SetMarginExpression(SourceRoiName=ctvSV, MarginSettings={ 'Type': "Expand", 'Superior': 1.0, 'Inferior': 1.0, 'Anterior': 0.7, 'Posterior': 0.7, 'Right': 0.7, 'Left': 0.7 })
			r2.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create PTV-SV. Continues...'
#procedure CreateMarginPtvTSV ends

def CreateMarginPtvE():
# 3) create PTV-E 
	with CompositeAction('Create PTV-E'):
		#PTV-E
		try :
			r3 = patient.PatientModel.CreateRoi(Name=ptvE, Color=colourPtvE, Type="PTV", TissueName=None, RoiMaterial=None)
			r3.SetMarginExpression(SourceRoiName=ctvE, MarginSettings={ 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.7, 'Posterior': 0.7, 'Right': 0.5, 'Left': 0.5 })
			r3.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create PTV-E. Continues...'
#procedure CreateMarginPtvE ends

def CreateUnionPtvTSV():
# 4) union of PTV-T and PTV-SV
	with CompositeAction('ROI Algebra (PTV-TSV)'):
		#PTV-TSV
		try:
			r4 = patient.PatientModel.CreateRoi(Name=ptvTSV, Color=colourPtvTSV, Type="PTV", TissueName=None, RoiMaterial=None)
			r4.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [ptvT], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r4.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create PTV-TSV. Continues ...'
#procedure CreatedUnionPtvTSV

def CreateTransitionPtvTsvPtvE():
# 5) transition zone between PTV-TSV and PTV-E
	with CompositeAction('ROI Algebra PTV-E-(PTV-TSV+8mm)'):
		#PTV-E-(PTV-TSV+8mm)
		try :
			r5 = patient.PatientModel.CreateRoi(Name=transitionTSVtoE, Color=colourPtvE, Type="PTV", TissueName=None, RoiMaterial=None)
			r5.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvTSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r5.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create PTV-E-(PTV-TSV+8mm). Continues...'
#procedure CreateTransitionPtvTsvPtvE ends

def CreateComplementPtvTsvPtvE():
# 6) complementary zone of PTV-E without PTV-TSV
	with CompositeAction('ROI Algebra PTV-E-(PTV-TSV)'):
		#PTV-E-(PTV-TSV)
		try :
			r6 = patient.PatientModel.CreateRoi(Name=complementPtvEofTSV, Color=colourPtvE, Type="PTV", TissueName=None, RoiMaterial=None)
			r6.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvTSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r6.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create PTV-E-(PTV-TSV). Continues...'
#procedure CreateComplementPtvTsvPtvE

def CreateComplementBladderPtvT():
# 8) bladder complementary volume without PTV-T
	with CompositeAction('ROI Algebra Blaere-(PTV-T+5mm)'):
		#OR; Blaere-(PTV-T+5mm)
		try :
			r8 = patient.PatientModel.CreateRoi(Name=complementBladderPtvT, Color=colourBladder, Type="Organ", TissueName=None, RoiMaterial=None)
			r8.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [bladder], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvT], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r8.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create OR; Blaere-(PTV-T+5mm). Continues...'
#procedure CreateComplementBladderPtvT ends

def CreateComplementBladderPtvTSV():
# 9) bladder complementary volume without PTV-TSV
	with CompositeAction('ROI Algebra Blaere-(PTV-TSV+5mm)'):
		#OR; Blaere-(PTV-TSV+5mm)
		try :
			r9 = patient.PatientModel.CreateRoi(Name=complementBladderPtvTSV, Color=colourBladder, Type="Organ", TissueName=None, RoiMaterial=None)
			r9.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [bladder], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvTSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r9.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create OR; Blaere-(PTV-TSV+5mm). Continues...'
#procedure CreateComplementBladderPtvTSV ends

def CreateComplementBladderPtvE():
# 10) bladder complementary volume without PTV-E
	with CompositeAction('ROI Algebra Blaere-(PTV-E+5mm)'):
		#OR; Blaere-(PTV-E+5mm)
		try :
			r10 = patient.PatientModel.CreateRoi(Name=complementBladderPtvE, Color=colourBladder, Type="Organ", TissueName=None, RoiMaterial=None)
			r10.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [bladder], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r10.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create OR; Blaere-(PTV-E+5mm). Continues...'
#procedure CreateComplementBladderPtvE

def CreateComplementRectumPtvT():
# 11) rectal complementary volume without PTV-T
	with CompositeAction('ROI Algebra Rectum-(PTV-T+5mm)'):
		#OR; Rectum-(PTV-T+5mm)
		try :
			r11 = patient.PatientModel.CreateRoi(Name=complementRectumPtvT, Color=colourRectum, Type="Organ", TissueName=None, RoiMaterial=None)
			r11.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [rectum], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvT], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r11.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create OR; Rectum-(PTV-T+5mm). Continues...'
#procedure CreateComplementRectumPtvT

def CreateComplementRectumPtvTSV():
# 12) rectal complementary volume without PTV-TSV
	with CompositeAction('ROI Algebra Rectum-(PTV-TSV+5mm)'):
		#OR; Rectum-(PTV-TSV+5mm)
		try :
			r12	= patient.PatientModel.CreateRoi(Name=complementRectumPtvTSV, Color=colourRectum, Type="Organ", TissueName=None, RoiMaterial=None)
			r12.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [rectum], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvTSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r12.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create OR; Rectum-(PTV-TSV+5mm). Continues...'
#procedure CreateComplementRectumPtvTSV ends

def CreateComplementRectumPtvE():
# 13) rectal complementary volume without PTV-E
	with CompositeAction('ROI Algebra Rectum-(PTV-E+5mm)'):
		#OR; Rectum-(PTV-E+5mm)
		try :
			r13 = patient.PatientModel.CreateRoi(Name=complementRectumPtvE, Color="128,128,128", Type="Organ", TissueName=None, RoiMaterial=None)
			r13.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [rectum], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r13.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create OR; Rectum-(PTV-E+5mm). Continues...'
#procedure CreateComplementRectumPtvE ends

def CreateComplementBowelPtvTSV():
# 14) bowel complementary volume without PTV-TSV
	with CompositeAction('ROI Algebra Tarm-(PTV-TSV+5mm)'):
		#OR; Tarm-(PTV-TSV+5mm)
		try :
			r14	= patient.PatientModel.CreateRoi(Name=complementBowelPtvTSV, Color=colourBowel, Type="Organ", TissueName=None, RoiMaterial=None)
			r14.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [bowel], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvTSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r14.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create OR; Tarm-(PTV-TSV+5mm). Continues...'
#procedure CreateComplementBowelPtvTSV ends

def CreateComplementBowelPtvE():
# 15) bowel complementary volume without PTV-E
	with CompositeAction('ROI Algebra Tarm-(PTV-E+5mm)'):
		#OR; Tarm-(PTV-E+5mm)
		try :
			r15 = patient.PatientModel.CreateRoi(Name=complementBowelPtvE, Color=colourBowel, Type="Organ", TissueName=None, RoiMaterial=None)
			r15.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [bowel], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r15.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create OR; Tarm-(PTV-E+5mm). Continues...'
#procedure CreateComplementBowelPtvE ends

def CreateWallPtvT():
# 16) toroidal help volume around PTV-T
	with CompositeAction('Create Wall;(PTV-T)+5mm'):
		#Wall;(PTV-T)+5mm
		try:
			r16	= patient.PatientModel.CreateRoi(Name=wallPtvT, Color="Gray", Type="Organ", TissueName=None, RoiMaterial=None)
			r16.SetWallExpression(SourceRoiName=ptvT, OutwardDistance=0.5, InwardDistance=0)
			r16.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create Wall;(PTV-T)+5mm. Continues ...'
#procedure CreateWallPtvT ends

def CreateWallPtvTSV():
# 17) toroidal help volume around PTV-TSV
	with CompositeAction('Create Wall;(PTV-TSV)+5mm'):
		#Wall;(PTV-TSV)+5mm
		try:
			r17	= patient.PatientModel.CreateRoi(Name=wallPtvTSV, Color="Gray", Type="Organ", TissueName=None, RoiMaterial=None)
			r17.SetWallExpression(SourceRoiName=ptvTSV, OutwardDistance=0.5, InwardDistance=0)
			r17.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create Wall;(PTV-TSV)+5mm. Continues ...'
#procedure CreateWallPtvTSV ends

def CreateWallPtvE():
# 18) toroidal help volume around PTV-E
	with CompositeAction('Create Wall;(PTV-E)+5mm'):
		#Wall;(PTV-E)+5mm
		try:
			r18	= patient.PatientModel.CreateRoi(Name=wallPtvE, Color="Gray", Type="Organ", TissueName=None, RoiMaterial=None)
			r18.SetWallExpression(SourceRoiName=ptvE, OutwardDistance=0.5, InwardDistance=0)
			r18.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create Wall;(PTV-E)+5mm. Continues ...'
#procedure CreateWallPtvE ends

def CreateComplementExternalPtvT():
# 20) external complementary volume without PTV-T
	with CompositeAction('ROI Algebra External-(PTV-T)'):
		#External-(PTV-T)
		try :
			r20 = patient.PatientModel.CreateRoi(Name=complementExternalPtvT, Color=colourComplementExternal, Type="Organ", TissueName=None, RoiMaterial=None)
			r20.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [external], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvT], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r20.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create External-(PTV-T). Continues...'
#procedure CreateComplementExternalPtvT ends

def CreateComplementExternalPtvTSV():
# 21) external complementary volume without PTV-TSV
	with CompositeAction('ROI Algebra External-(PTV-TSV)'):
		#External-(PTV-TSV)
		try :
			r21 = patient.PatientModel.CreateRoi(Name=complementExternalPtvTsv, Color=colourComplementExternal, Type="Organ", TissueName=None, RoiMaterial=None)
			r21.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [external], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvTSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r21.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create External-(PTV-TSV). Continues...'
#procedure CreateComplementExternalPtvTSV ends

def CreateComplementExternalPtvE():
# 22) external complementary volume without PTV-E
	with CompositeAction('ROI Algebra External-(PTV-E)'):
		#External-(PTV-E)
		try :
			r22 = patient.PatientModel.CreateRoi(Name=complementExternalPtvE, Color=colourComplementExternal, Type="Organ", TissueName=None, RoiMaterial=None)
			r22.SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [external], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			r22.UpdateDerivedGeometry(Examination=examination)
		except Exception:
			print 'Failed to create External-(PTV-E). Continues...'
#procedure CreateComplementExternalPtvE ends


