
# DEFINE THE CT DENSITY TABLE NAME
densityConversionTable = 'CTAWP65673:120kV'
oncentraConversionTable = 'OEB CT Table'


# DEFINE AN EXTERNAL CONTOUR THRESHOLD LEVEL FOR AUTOSEGMENTATION
externalContourThreshold = -150
factoryContourThreshold = -250


# DEFINE A MANDATORY SET OF INITIAL STRUCTURES
# ------ PLAN NEEDS TO HAVE THESE STRUCTURES DEFINED BEFORE EXECUTING THE AUTOPLAN SCRIPT
ctvT = 'CTV-T'
ctvSV = 'CTV-SV' #required in Type B and C plans
ctvE = 'CTV-E' #required in Type N plans
analCanal = 'OR; Anal Canal'
penileBulb = 'OR; Bulbus penis'
rectum = 'OR; Rectum'
bladder = 'OR; Blaere'
bowel = 'OR; Tarm' #only exists for N+ disease
testes = 'OR; Testis'
fiducial1 = 'S1' #does not exist for salvage cases
fiducial2 = 'S2' #does not exist for salvage cases
fiducial3 = 'S3' #does not exist for salvage cases
fiducial4 = 'S4' #may or may not exist for any prostate plan
fiducial5 = 'S5' #may or may not exist for any prostate plan
fiducial6 = 'S6' #may or may not exist for any prostate plan
external = 'External'
pelvicCouchModel = 'ContesseCouch-Pelvine'



# DEFINE A STANDARD SET OF ANATOMICAL STRUCTURE NAMES
external = 'External'
femHeadLeft = 'OR; Cap fem sin'
femHeadRight = 'OR; Cap fem dex'
ptvT = 'PTV-T'
ptvSV = 'PTV-SV'
ptvTSV = 'PTV-TSV'
ptvE = 'PTV-E'
ptvTSVE = 'PTV-(T+SV+E)'
ptvSVE = 'PTV-(SV+E)'
hvRect = 'HV-Rectum'
marker1 = 'Mark1'
marker2 = 'Mark2'
marker3 = 'Mark3'
marker4 = 'Mark4'
marker5 = 'Mark5'
marker6 = 'Mark6'

# DEFINE A STANDARD SET OF STRUCTURE COLOURS
# colour codes imported from Oncentra
#---- see for example colour charts at http://www.rapidtables.com/web/color/RGB_Color.htm
colourExternal = "255,173,91"
colourCtvT = "255,128,128"
colourCtvSV = "230,149,134"
colourCtvE = "255,81,81"
colourPtvT = "202,203,249"
colourPtvSV = "112,102,232"
colourPtvTSV = "202,203,249"
colourPtvE = "126,130,239"
colourAnalCanal = "0,204,0"
colourBladder = "0,172,128"
colourRectum = "0,102,51"
colourBulbusPenis = "128,255,128"
colourCaputFemori = "0,66,0"
colourBowel = "0,176,0"
colourTestes = "24,192,128"

colourMarker1 = "0,255,255"
colourMarker2 = "255,128,255"
colourMarker3 = "0,255,0"
colourMarker4 = "255,255,0"
colourMarker5 = "0,0,255"
colourMarker6 = "128,0,255"

colourComplementExternal = "192,192,192"
colourWallStructures = "0,200,255"


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

wall5mmPtvT = 'Wall; PTV-T+5mm'
wall8mmPtvT = 'Wall; PTV-T+8mm'
wall5mmPtvTSV = 'Wall; PTV-TSV+5mm'
wall8mmPtvTSV = 'Wall; PTV-TSV+8mm'
wall5mmPtvE = 'Wall; PTV-E+5mm'
wall8mmPtvE = 'Wall; PTV-E+8mm'

transitionTSVtoE = 'PTV-E-(PTV-TSV+8mm)'
transitionTtoSVE = 'PTV-(SV+E)-(PTV-T+8mm)'

complementExt5mmPtvT = 'Ext-(PTV-T+5mm)'
complementExt5mmPtvTSV = 'Ext-(PTV-TSV+5mm)'
complementExt5mmPtvE = 'Ext-(PTV-E+5mm)'
complementExt8mmPtvTSV = 'Ext-(PTV-TSV+8mm)'
complementExt8mmPtvE = 'Ext-(PTV-E+8mm)'


# DEFINE THE STANDARD PLANNING AND PRESCRIPTION PARAMETERS
defaultLinac = 'ElektaAgility_v1' #standard linac beam model for dose planning
defaultDoseGrid = 0.25 #isotropic dose grid dimension
defaultPhotonEn = 6 #standard photon beam modality in units of MV


# DEFINE THE STANDARD TEMPLATES AND OPTIMIZATION FUNCTIONS
defaultClinicalGoalsProstC = 'ProstC_Clinical_Goals_Template'
defaultClinicalGoalsProstA = 'ProstA_Clinical_Goals_Template'
defaultClinicalGoalsProstS = 'ProstS_Clinical_Goals_Template'
defaultClinicalGoalsProstBPr = 'ProstBPr_Clinical_Goals_Template'
defaultClinicalGoalsProstBBo = 'ProstBBo_Clinical_Goals_Template'
defaultClinicalGoalsProstB = 'ProstB_Clinical_Goals_Template'
defaultClinicalGoalsProstD = 'ProstD_Clinical_Goals_Template'
defaultClinicalGoalsProstE = 'ProstE_Clinical_Goals_Template'

defaultOptimVmatProstC = 'ProstC_VMAT_1arc_Optimization'
defaultOptimVmatProstA = 'ProstA_VMAT_1arc_Optimization'
defaultOptimVmatProstS = 'ProstS_VMAT_1arc_Optimization'
defaultOptimVmatProstBBo = 'ProstBBo_VMAT_1arc_Optimization'
defaultOptimVmatProstBPr = 'ProstBPr_VMAT_1arc_Optimization'
defaultOptimVmatProstD = 'ProstD_VMAT_2arc_Optimization'
defaultOptimVmatProstE = 'ProstE_VMAT_2arc_Optimization'



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

def OverrideFiducialsDensity(pm,exam,i):
# 19) creation of density over-rides in concentric rings around a fiducial
	#fiducial number 1
	try:
		coord = pm.StructureSets[exam.Name].PoiGeometries[fiducial1].Point
		# --- set a new empty roi at this coordinate position
		pm.CreateRoi(Name='Temp1', Color="Fuchsia", Type="Marker", TissueName=None, RoiMaterial=None)
		# --- draw a 3mm spherical roi around the nominated poi
		pm.RegionsOfInterest['Temp1'].CreateSphereGeometry( Radius=0.3, Examination=exam, Center={'x':coord.x, 'y':coord.y, 'z':coord.z} )
		# --- draw a 7mm-wide wall region around the temporary roi
		pm.CreateRoi(Name=marker1, Color=colourMarker1, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[marker1].SetWallExpression(SourceRoiName='Temp1', OutwardDistance=0.7, InwardDistance=0)
		pm.RegionsOfInterest[marker1].UpdateDerivedGeometry(Examination=exam)
		# --- reset the density override in this region to the newly created material (index from args)
		pm.RegionsOfInterest[marker1].SetRoiMaterial(Material = pm.Materials[i])
	except Exception:
		print 'Failed to generate Marker_1 override ROI. Continues...'
	#no further need for the temporary structure
	try:
		pm.RegionsOfInterest['Temp1'].DeleteRoi()
	except Exception:
		print 'Error cleaning up marker 1 source ROI. Continues...'
	#
	#fiducial number 2
	try:
		coord = pm.StructureSets[exam.Name].PoiGeometries[fiducial2].Point
		# --- set a new empty roi at this coordinate position
		pm.CreateRoi(Name='Temp2', Color="Fuchsia", Type="Marker", TissueName=None, RoiMaterial=None)
		# --- draw a 3mm spherical roi around the nominated poi
		pm.RegionsOfInterest['Temp2'].CreateSphereGeometry( Radius=0.3, Examination=exam, Center={'x':coord.x, 'y':coord.y, 'z':coord.z} )
		# --- draw a 7mm-wide wall region around the temporary roi
		pm.CreateRoi(Name=marker2, Color=colourMarker2, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[marker2].SetWallExpression(SourceRoiName='Temp2', OutwardDistance=0.7, InwardDistance=0)
		pm.RegionsOfInterest[marker2].UpdateDerivedGeometry(Examination=exam)
		# --- reset the density override in this region to the newly created material (index from args)
		pm.RegionsOfInterest[marker2].SetRoiMaterial(Material = pm.Materials[i])
	except Exception:
		print 'Failed to generate Marker_2 override ROI. Continues...'
	#no further need for the temporary structure
	try:
		pm.RegionsOfInterest['Temp2'].DeleteRoi()
	except Exception:
		print 'Error cleaning up marker 2 source ROI. Continues...'
	#
	#fiducial number 3
	try:
		coord = pm.StructureSets[exam.Name].PoiGeometries[fiducial3].Point
		# --- set a new empty roi at this coordinate position
		pm.CreateRoi(Name='Temp3', Color="Fuchsia", Type="Marker", TissueName=None, RoiMaterial=None)
		# --- draw a 3mm spherical roi around the nominated poi
		pm.RegionsOfInterest['Temp3'].CreateSphereGeometry( Radius=0.3, Examination=exam, Center={'x':coord.x, 'y':coord.y, 'z':coord.z} )
		# --- draw a 7mm-wide wall region around the temporary roi
		pm.CreateRoi(Name=marker3, Color=colourMarker3, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[marker3].SetWallExpression(SourceRoiName='Temp3', OutwardDistance=0.7, InwardDistance=0)
		pm.RegionsOfInterest[marker3].UpdateDerivedGeometry(Examination=exam)
		# --- reset the density override in this region to the newly created material (index from args)
		pm.RegionsOfInterest[marker3].SetRoiMaterial(Material = pm.Materials[i])
	except Exception:
		print 'Failed to generate Marker_3 override ROI. Continues...'
	#no further need for the temporary structure
	try:
		pm.RegionsOfInterest['Temp3'].DeleteRoi()
	except Exception:
		print 'Error cleaning up marker 3 source ROI. Continues...'
	#
	#fiducial number 4 - might not exist
	try:
		coord = pm.StructureSets[exam.Name].PoiGeometries[fiducial4].Point
		# --- set a new empty roi at this coordinate position
		pm.CreateRoi(Name='Temp4', Color="Fuchsia", Type="Marker", TissueName=None, RoiMaterial=None)
		# --- draw a 3mm spherical roi around the nominated poi
		pm.RegionsOfInterest['Temp4'].CreateSphereGeometry( Radius=0.3, Examination=exam, Center={'x':coord.x, 'y':coord.y, 'z':coord.z} )
		# --- draw a 7mm-wide wall region around the temporary roi
		pm.CreateRoi(Name=marker4, Color=colourMarker4, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[marker4].SetWallExpression(SourceRoiName='Temp4', OutwardDistance=0.7, InwardDistance=0)
		pm.RegionsOfInterest[marker4].UpdateDerivedGeometry(Examination=exam)
		# --- reset the density override in this region to the newly created material (index from args)
		pm.RegionsOfInterest[marker4].SetRoiMaterial(Material = pm.Materials[i])
	except Exception:
		print 'Failed to generate Marker_4 override ROI. Continues...'
	#no further need for the temporary structure
	try:
		pm.RegionsOfInterest['Temp4'].DeleteRoi()
	except Exception:
		print 'Error cleaning up marker 4 source ROI. Continues...'
	#
	#fiducial number 5 - might not exist
	try:
		coord = pm.StructureSets[exam.Name].PoiGeometries[fiducial5].Point
		# --- set a new empty roi at this coordinate position
		pm.CreateRoi(Name='Temp5', Color="Fuchsia", Type="Marker", TissueName=None, RoiMaterial=None)
		# --- draw a 3mm spherical roi around the nominated poi
		pm.RegionsOfInterest['Temp5'].CreateSphereGeometry( Radius=0.3, Examination=exam, Center={'x':coord.x, 'y':coord.y, 'z':coord.z} )
		# --- draw a 7mm-wide wall region around the temporary roi
		pm.CreateRoi(Name=marker5, Color=colourMarker5, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[marker5].SetWallExpression(SourceRoiName='Temp5', OutwardDistance=0.7, InwardDistance=0)
		pm.RegionsOfInterest[marker5].UpdateDerivedGeometry(Examination=exam)
		# --- reset the density override in this region to the newly created material (index from args)
		pm.RegionsOfInterest[marker5].SetRoiMaterial(Material = pm.Materials[i])
	except Exception:
		print 'Failed to generate Marker_5 override ROI. Continues...'
	#no further need for the temporary structure
	try:
		pm.RegionsOfInterest['Temp5'].DeleteRoi()
	except Exception:
		print 'Error cleaning up marker 5 source ROI. Continues...'
	#
	#fiducial number 6 - might not exist
	try:
		coord = pm.StructureSets[exam.Name].PoiGeometries[fiducial6].Point
		# --- set a new empty roi at this coordinate position
		pm.CreateRoi(Name='Temp6', Color="Fuchsia", Type="Marker", TissueName=None, RoiMaterial=None)
		# --- draw a 3mm spherical roi around the nominated poi
		pm.RegionsOfInterest['Temp6'].CreateSphereGeometry( Radius=0.3, Examination=exam, Center={'x':coord.x, 'y':coord.y, 'z':coord.z} )
		# --- draw a 7mm-wide wall region around the temporary roi
		pm.CreateRoi(Name=marker6, Color=colourMarker6, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[marker6].SetWallExpression(SourceRoiName='Temp6', OutwardDistance=0.7, InwardDistance=0)
		pm.RegionsOfInterest[marker6].UpdateDerivedGeometry(Examination=exam)
		# --- reset the density override in this region to the newly created material (index from args)
		pm.RegionsOfInterest[marker6].SetRoiMaterial(Material = pm.Materials[i])
	except Exception:
		print 'Failed to generate Marker_6 override ROI. Continues...'
	#no further need for the temporary structure
	try:
		pm.RegionsOfInterest['Temp6'].DeleteRoi()
	except Exception:
		print 'Error cleaning up marker 6 source ROI. Continues...'
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
#procedure CreateMarginPtvSV ends

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

def CreateUnionPtvTSVE(pm,exam):
# 4) union of all ptv's
	#PTV-TSVE
	try:
		pm.CreateRoi(Name=ptvTSVE, Color=colourPtvE, Type="PTV", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[ptvTSVE].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [ptvT,ptvSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[ptvTSVE].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create PTV-(T+SV+E). Continues ...'
#procedure CreatedUnionPtvTSV

def CreateUnionPtvSVE(pm,exam):
# 4) union of PTV-SV and PTV-E
	#PTV-SVE
	try:
		pm.CreateRoi(Name=ptvSVE, Color=colourPtvE, Type="PTV", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[ptvSVE].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [ptvSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[ptvSVE].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create PTV-(SV+E). Continues ...'
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

def CreateTransitionPtvTPtvSVE(pm,exam):
# 5) transition zone between PTV-SV and PTV-(SV+E)
	#PTV-(SV+E)-(PTV-T+8mm)
	try :
		pm.CreateRoi(Name=transitionTtoSVE, Color=colourPtvE, Type="PTV", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[transitionTtoSVE].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [ptvSVE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvT], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.8, 'Inferior': 0.8, 'Anterior': 0.8, 'Posterior': 0.8, 'Right': 0.8, 'Left': 0.8 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[transitionTtoSVE].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create PTV-(SV+E)-(PTV-T+8mm). Continues...'
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


# Utility function to locate the index position of 'matl' in the materials list 'mlist'
def IndexOfMaterial(mlist,matl):
	mindex = -1 # if the material is not found in the list then it return a negative value
	mi = 0
	for m in mlist:
		if m.Name == matl:
			mindex = mi
		mi = mi + 1
	return mindex


# Utility function to retrieve a unique plan name in a given case
def UniquePlanName(name, cas):
  for p in cas.TreatmentPlans:
    if name == p.Name:
      name = name + '_1'
      name = UniquePlanName(name, cas)
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




#CreateComplementBladderPtvT(patient.PatientModel,examination) #all prostate types
#CreateComplementRectumPtvT(patient.PatientModel,examination) #all prostate types
#CreateWallPtvT(patient.PatientModel,examination) #all prostate types
#CreateComplementExternalPtvT(patient.PatientModel,examination) #all prostate types

#CreateComplementBladderPtvTSV(patient.PatientModel,examination) #all prostate types except Type A
#CreateComplementRectumPtvTSV(patient.PatientModel,examination) #all prostate types except Type A
#CreateWallPtvTSV(patient.PatientModel,examination) #all prostate types except Type A
#CreateComplementExternalPtvTSV(patient.PatientModel,examination) #all prostate types except Type A

#CreateMarginPtvE(patient.PatientModel,examination) #only for Type N+
#CreateTransitionPtvTsvPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementPtvTsvPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementBladderPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementRectumPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementBowelPtvTSV(patient.PatientModel,examination) #only for Type N+
#CreateComplementBowelPtvE(patient.PatientModel,examination) #only for Type N+
#CreateWallPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementExternalPtvE(patient.PatientModel,examination) #only for Type N+
