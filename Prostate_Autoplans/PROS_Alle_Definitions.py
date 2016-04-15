
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
colourComplementExternal = "192,192,192"


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

# DEFINE THE STANDARD PLANNING AND PRESCRIPTION PARAMETERS
defaultLinac = 'LW_Agility_VMAT' #standard linac beam model for dose planning
defaultDoseGrid = 0.25 #isotropic dose grid dimension
defaultPhotonEn = 6 #standard photon beam modality in units of MV



# IMPORTANT - MODIFY WITH CAUTION - STANDARD PROCEDURES FOR AUTOPLANNING WORKFLOW
# ===============================================================================

def CreateWallHvRectum(pm,exam):
# 7) rectal help volume
	#HV-Rectum
	try:
		pm.CreateRoi(Name=hvRect, Color="Red", Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[hvRect].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [rectum], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 1.0, 'Posterior': 1.0, 'Right': 1.0, 'Left': 1.0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [rectum], 'MarginSettings': { 'Type': "Contract", 'Superior': 0, 'Inferior': 0, 'Anterior': 1.0, 'Posterior': 1.0, 'Right': 1.0, 'Left': 1.0 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[hvRect].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to generate HV-Rectum. Continues...'
#procedure CreateWallHvRectum ends

def OverrideFiducialsDensity(pm,exam):
# 19) creation of density over-rides in concentric rings around a fiducial
	#fiducial number 1
	try:
		pm.CreateRoi(Name=fiducial1, Color=colourMarker1, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[fiducial1].SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [fiducial1], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [fiducial1], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.1, 'Inferior': 0.1, 'Anterior': 0.1, 'Posterior': 0.1, 'Right': 0.1, 'Left': 0.1 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[fiducial1].SetRoiMaterial(Material = patient.PatientModel.Materials[0])
		pm.RegionsOfInterest[fiducial1].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to generate Marker_1 override ROI. Continues...'
	try:
		pm.RegionsOfInterest[fiducial1].DeleteRoi()
	except Exception:
		print 'Could not delete fiducial1 ROI. Continues...'
	#
	#fiducial number 2
	try:
		pm.CreateRoi(Name=fiducial2, Color=colourMarker2, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[fiducial2].SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [fiducial2], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [fiducial2], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.1, 'Inferior': 0.1, 'Anterior': 0.1, 'Posterior': 0.1, 'Right': 0.1, 'Left': 0.1 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[fiducial2].SetRoiMaterial(Material = patient.PatientModel.Materials[0])
		pm.RegionsOfInterest[fiducial2].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to generate Marker_2 override ROI. Continues...'
	try:
		pm.RegionsOfInterest[fiducial2].DeleteRoi()
	except Exception:
		print 'Could not delete fiducial2 ROI. Continues...'
	#
	#fiducial number 3
	try:
		pm.CreateRoi(Name=fiducial3, Color=colourMarker3, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[fiducial3].SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [fiducial3], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [fiducial3], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.1, 'Inferior': 0.1, 'Anterior': 0.1, 'Posterior': 0.1, 'Right': 0.1, 'Left': 0.1 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[fiducial3].SetRoiMaterial(Material = patient.PatientModel.Materials[0])
		pm.RegionsOfInterest[fiducial3].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to generate Marker_3 override ROI. Continues...'
	try:
		pm.RegionsOfInterest[fiducial3].DeleteRoi()
	except Exception:
		print 'Could not delete fiducial3 ROI. Continues...'
	#
	#fiducial number 4
	try:
		pm.CreateRoi(Name=fiducial4, Color=colourMarker4, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[fiducial4].SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [fiducial4], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [fiducial4], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.1, 'Inferior': 0.1, 'Anterior': 0.1, 'Posterior': 0.1, 'Right': 0.1, 'Left': 0.1 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[fiducial4].SetRoiMaterial(Material = patient.PatientModel.Materials[0])
		pm.RegionsOfInterest[fiducial4].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to generate Marker_4 override ROI. Continues...'
	try:
		pm.RegionsOfInterest[fiducial4].DeleteRoi()
	except Exception:
		print 'Could not delete fiducial4 ROI. Continues...'
	#
	#fiducial number 5
	try:
		pm.CreateRoi(Name=fiducial5, Color=colourMarker5, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[fiducial5].SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [fiducial5], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [fiducial5], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.1, 'Inferior': 0.1, 'Anterior': 0.1, 'Posterior': 0.1, 'Right': 0.1, 'Left': 0.1 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[fiducial5].SetRoiMaterial(Material = patient.PatientModel.Materials[0])
		pm.RegionsOfInterest[fiducial5].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to generate Marker_5 override ROI. Continues...'
	try:
		pm.RegionsOfInterest[fiducial5].DeleteRoi()
	except Exception:
		print 'Could not delete fiducial5 ROI. Continues...'
	#
	#fiducial number 6
	try:
		pm.CreateRoi(Name=fiducial6, Color=colourMarker6, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[fiducial6].SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [fiducial6], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [fiducial6], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.1, 'Inferior': 0.1, 'Anterior': 0.1, 'Posterior': 0.1, 'Right': 0.1, 'Left': 0.1 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[fiducial6].SetRoiMaterial(Material = patient.PatientModel.Materials[0])
		pm.RegionsOfInterest[fiducial6].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to generate Marker_6 override ROI. Continues...'
	try:
		pm.RegionsOfInterest[fiducial6].DeleteRoi()
	except Exception:
		print 'Could not delete fiducial6 ROI. Continues...'
	#procedure OverrideFiducialsDensity ends

def CreateMarginPtvT(pm,exam):
# 1) create PTV-T
	#PTV-T
	try :
		pm.CreateRoi(Name=ptvT, Color=colourPtvT, Type="PTV", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[ptvT].SetMarginExpression(SourceRoiName=ctvT, MarginSettings={ 'Type': "Expand", 'Superior': 1.0, 'Inferior': 1.0, 'Anterior': 0.7, 'Posterior': 0.7, 'Right': 0.7, 'Left': 0.7 })
		pm.RegionsOfInterest[ptvT].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create PTV-T. Continues...'
#procedure CreateMarginPtvT ends

def CreateMarginPtvSV(pm,exam):
# 2) create PTV-SV
	#PTV-SV
	try :
		pm.CreateRoi(Name=ptvSV, Color=colourPtvSV, Type="PTV", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[ptvSV].SetMarginExpression(SourceRoiName=ctvSV, MarginSettings={ 'Type': "Expand", 'Superior': 1.0, 'Inferior': 1.0, 'Anterior': 0.7, 'Posterior': 0.7, 'Right': 0.7, 'Left': 0.7 })
		pm.RegionsOfInterest[ptvSV].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create PTV-SV. Continues...'
#procedure CreateMarginPtvTSV ends

def CreateMarginPtvE(pm,exam):
# 3) create PTV-E 
	#PTV-E
	try :
		pm.CreateRoi(Name=ptvE, Color=colourPtvE, Type="PTV", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[ptvE].SetMarginExpression(SourceRoiName=ctvE, MarginSettings={ 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.7, 'Posterior': 0.7, 'Right': 0.5, 'Left': 0.5 })
		pm.RegionsOfInterest[ptvE].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create PTV-E. Continues...'
#procedure CreateMarginPtvE ends

def CreateUnionPtvTSV(pm,exam):
# 4) union of PTV-T and PTV-SV
	#PTV-TSV
	try:
		pm.CreateRoi(Name=ptvTSV, Color=colourPtvTSV, Type="PTV", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[ptvTSV].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [ptvT], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[ptvTSV].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create PTV-TSV. Continues ...'
#procedure CreatedUnionPtvTSV

def CreateTransitionPtvTsvPtvE(pm,exam):
# 5) transition zone between PTV-TSV and PTV-E
	#PTV-E-(PTV-TSV+8mm)
	try :
		pm.CreateRoi(Name=transitionTSVtoE, Color=colourPtvE, Type="PTV", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[transitionTSVtoE].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvTSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[transitionTSVtoE].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create PTV-E-(PTV-TSV+8mm). Continues...'
#procedure CreateTransitionPtvTsvPtvE ends

def CreateComplementPtvTsvPtvE(pm,exam):
# 6) complementary zone of PTV-E without PTV-TSV
	#PTV-E-(PTV-TSV)
	try :
		pm.CreateRoi(Name=complementPtvEofTSV, Color=colourPtvE, Type="PTV", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[complementPtvEofTSV].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvTSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[complementPtvEofTSV].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create PTV-E-(PTV-TSV). Continues...'
#procedure CreateComplementPtvTsvPtvE

def CreateComplementBladderPtvT(pm,exam):
# 8) bladder complementary volume without PTV-T
	#OR; Blaere-(PTV-T+5mm)
	try :
		pm.CreateRoi(Name=complementBladderPtvT, Color=colourBladder, Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[complementBladderPtvT].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [bladder], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvT], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[complementBladderPtvT].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create OR; Blaere-(PTV-T+5mm). Continues...'
#procedure CreateComplementBladderPtvT ends

def CreateComplementBladderPtvTSV(pm,exam):
# 9) bladder complementary volume without PTV-TSV
	#OR; Blaere-(PTV-TSV+5mm)
	try :
		pm.CreateRoi(Name=complementBladderPtvTSV, Color=colourBladder, Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[complementBladderPtvTSV].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [bladder], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvTSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[complementBladderPtvTSV].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create OR; Blaere-(PTV-TSV+5mm). Continues...'
#procedure CreateComplementBladderPtvTSV ends

def CreateComplementBladderPtvE(pm,exam):
# 10) bladder complementary volume without PTV-E
	#OR; Blaere-(PTV-E+5mm)
	try :
		pm.CreateRoi(Name=complementBladderPtvE, Color=colourBladder, Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[complementBladderPtvE].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [bladder], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[complementBladderPtvE].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create OR; Blaere-(PTV-E+5mm). Continues...'
#procedure CreateComplementBladderPtvE

def CreateComplementRectumPtvT(pm,exam):
# 11) rectal complementary volume without PTV-T
	#OR; Rectum-(PTV-T+5mm)
	try :
		pm.CreateRoi(Name=complementRectumPtvT, Color=colourRectum, Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[complementRectumPtvT].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [rectum], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvT], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[complementRectumPtvT].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create OR; Rectum-(PTV-T+5mm). Continues...'
#procedure CreateComplementRectumPtvT

def CreateComplementRectumPtvTSV(pm,exam):
# 12) rectal complementary volume without PTV-TSV
	#OR; Rectum-(PTV-TSV+5mm)
	try :
		pm.CreateRoi(Name=complementRectumPtvTSV, Color=colourRectum, Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[complementRectumPtvTSV].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [rectum], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvTSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[complementRectumPtvTSV].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create OR; Rectum-(PTV-TSV+5mm). Continues...'
#procedure CreateComplementRectumPtvTSV ends

def CreateComplementRectumPtvE(pm,exam):
# 13) rectal complementary volume without PTV-E
	#OR; Rectum-(PTV-E+5mm)
	try :
		pm.CreateRoi(Name=complementRectumPtvE, Color="128,128,128", Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[complementRectumPtvE].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [rectum], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[complementRectumPtvE].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create OR; Rectum-(PTV-E+5mm). Continues...'
#procedure CreateComplementRectumPtvE ends

def CreateComplementBowelPtvTSV(pm,exam):
# 14) bowel complementary volume without PTV-TSV
	#OR; Tarm-(PTV-TSV+5mm)
	try :
		pm.CreateRoi(Name=complementBowelPtvTSV, Color=colourBowel, Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[complementBowelPtvTSV].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [bowel], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvTSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[complementBowelPtvTSV].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create OR; Tarm-(PTV-TSV+5mm). Continues...'
#procedure CreateComplementBowelPtvTSV ends

def CreateComplementBowelPtvE(pm,exam):
# 15) bowel complementary volume without PTV-E
		#OR; Tarm-(PTV-E+5mm)
		try :
			pm.CreateRoi(Name=complementBowelPtvE, Color=colourBowel, Type="Organ", TissueName=None, RoiMaterial=None)
			pm.RegionsOfInterest[complementBowelPtvE].SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [bowel], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
			pm.RegionsOfInterest[complementBowelPtvE].UpdateDerivedGeometry(Examination=exam)
		except Exception:
			print 'Failed to create OR; Tarm-(PTV-E+5mm). Continues...'
#procedure CreateComplementBowelPtvE ends

def CreateWallPtvT(pm,exam):
# 16) toroidal help volume around PTV-T
	#Wall;(PTV-T)+5mm
	try:
		pm.CreateRoi(Name=wallPtvT, Color="Gray", Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[wallPtvT].SetWallExpression(SourceRoiName=ptvT, OutwardDistance=0.5, InwardDistance=0)
		pm.RegionsOfInterest[wallPtvT].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create Wall;(PTV-T)+5mm. Continues ...'
#procedure CreateWallPtvT ends

def CreateWallPtvTSV(pm,exam):
# 17) toroidal help volume around PTV-TSV
	#Wall;(PTV-TSV)+5mm
	try:
		pm.CreateRoi(Name=wallPtvTSV, Color="Gray", Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[wallPtvTSV].SetWallExpression(SourceRoiName=ptvTSV, OutwardDistance=0.5, InwardDistance=0)
		pm.RegionsOfInterest[wallPtvTSV].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create Wall;(PTV-TSV)+5mm. Continues ...'
#procedure CreateWallPtvTSV ends

def CreateWallPtvE(pm,exam):
# 18) toroidal help volume around PTV-E
	#Wall;(PTV-E)+5mm
	try:
		pm.CreateRoi(Name=wallPtvE, Color="Gray", Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[wallPtvE].SetWallExpression(SourceRoiName=ptvE, OutwardDistance=0.5, InwardDistance=0)
		pm.RegionsOfInterest[wallPtvE].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create Wall;(PTV-E)+5mm. Continues ...'
#procedure CreateWallPtvE ends

def CreateComplementExternalPtvT(pm,exam):
# 20) external complementary volume without PTV-T
	#External-(PTV-T)
	try :
		pm.CreateRoi(Name=complementExternalPtvT, Color=colourComplementExternal, Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[complementExternalPtvT].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [external], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvT], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[complementExternalPtvT].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create External-(PTV-T). Continues...'
#procedure CreateComplementExternalPtvT ends

def CreateComplementExternalPtvTSV(pm,exam):
# 21) external complementary volume without PTV-TSV
	#External-(PTV-TSV)
	try :
		pm.CreateRoi(Name=complementExternalPtvTsv, Color=colourComplementExternal, Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[complementExternalPtvTsv].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [external], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvTSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[complementExternalPtvTsv].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create External-(PTV-TSV). Continues...'
#procedure CreateComplementExternalPtvTSV ends

def CreateComplementExternalPtvE(pm,exam):
# 22) external complementary volume without PTV-E
	#External-(PTV-E)
	try :
		pm.CreateRoi(Name=complementExternalPtvE, Color=colourComplementExternal, Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[complementExternalPtvE].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [external], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[complementExternalPtvE].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create External-(PTV-E). Continues...'
#procedure CreateComplementExternalPtvE ends


# Utility function to retrieve a unique plan name
def UniquePlanName(name, pat):
  for p in pat.TreatmentPlans:
    if name == p.Name:
      name = name + '_1'
      name = UniquePlanName(name, pat)
  return name

# Utility function that loads a plan and beam set into GUI
def LoadPlanAndBeamSet(patient, plan, beamset):
  # load plan
  planFilter = {"Name":plan.Name}
  planInfos = patient.QueryPlanInfo(Filter = planFilter)
  if len(planInfos) != 1:
    raise Exception('Failed plan query (nr of plan infos = {0})'.format(len(planInfos)))
  patient.LoadPlan(PlanInfo = {"Name": "^" + plan.Name + "$"})
  # load beam set  
  beamsetInfos = plan.QueryBeamSetInfo(Filter = {"Name":beamset.DicomPlanLabel})
  if len(beamsetInfos) != 1:
    raise Exception('Failed beam set query (nr of beam set infos = {0})'.format(len(beamsetInfos)))
  plan.LoadBeamSet(BeamSetInfo = beamsetInfos[0])
  # end LoadPlanAndBeamSet


