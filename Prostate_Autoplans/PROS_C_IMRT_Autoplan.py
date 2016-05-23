import math
from connect import *
import time
import sys
clr.AddReference("PresentationFramework")
from System.Windows import *

from PROS_Alle_Definitions import *

#### PROSTATE TYPE C AUTO-PLAN
#### 78Gy/39F Normo-fractionated prescribed to PTV-T and PTV-SV
#### As a 7-field IMRT beam distribution

defaultPrescDose = 7800 #the absolute prescribed dose in cGy
defaultFractions = 39 #standard number of fractions

# NOTE A TEMPLATE BEAMSET IS NOT DEFINED THROUGH A FUNCTION CALL TO APPLY A TEMPLATE
# but rather each field in the beamset has been explicitly defined using
# the 'CreatePhotonBeam' method acting on a BeamSet instance - see lines in script

# Define null filter
filter = {}

# Get handle to current patient database
patient_db = get_current('PatientDB')

# Define patient and examination handles
patient = get_current('Patient')
examination = get_current('Examination')
case = get_current('Case')

# Define the workflow for the autoplan step
# 1. Confirm that all mandatory structures exist and have non-zero volumes
# 2. Assign correct CT to Density Table
# 3. Define density override material for region around prostate markers
# 4. Grow all required volumes and conformity structures
# 5. Create new plan with unique name
# 6. Create first beam set
# 7. Set default dose grid
# 8. Load beam(s) list
# 9. Load clinical goals list
# 10. Load cost functions list
# 11. Load optimization settings
# 12. Optimization first-run
# 13. Compute full dose
# -- repeat from step 6 if more than one beam set is required f.ex. Prost Type B


# 1. Check structure set
# -------- Define composite handle for PATIENT ANATOMY MODELLING
pm = case.PatientModel
#
roi = pm.StructureSets[examination.Name]
# - check for finite CTV-T volume
volcheck = roi.RoiGeometries[ctvT].GetRoiVolume()
if (volcheck < 0.1):
	raise Exception('Please CHECK contouring - Volume of CTV-T might be less than 0.1 ccm!')
# - check for finite CTV-SV volume
volcheck = roi.RoiGeometries[ctvSV].GetRoiVolume()
if (volcheck < 0.1):
	raise Exception('Please CHECK contouring - Volume of CTV-SV might be less than 0.1 ccm!')
# - check for finite OR; Rectum volume
volcheck = roi.RoiGeometries[rectum].GetRoiVolume()
if (volcheck < 0.1):
	raise Exception('Please CHECK contouring - Volume of OR; Rectum might be less than 0.1 ccm!')
# - check for finite OR; Blaere volume
volcheck = roi.RoiGeometries[bladder].GetRoiVolume()
if (volcheck < 0.1):
	raise Exception('Please CHECK contouring - Volume of OR; Blaere might be less than 0.1 ccm!')
# - check for finite OR; Anal Canal volume
volcheck = roi.RoiGeometries[analCanal].GetRoiVolume()
if (volcheck < 0.1):
	raise Exception('Please CHECK contouring - Volume of OR; Anal Canal might be less than 0.1 ccm!')
# - check for finite OR; Bulbus penis volume
volcheck = roi.RoiGeometries[penileBulb].GetRoiVolume()
if (volcheck < 0.1):
	raise Exception('Please CHECK contouring - Volume of OR; Bulbus penis might be less than 0.1 ccm!')
# - check for finite OR; Testes volume
volcheck = roi.RoiGeometries[testes].GetRoiVolume()
if (volcheck < 0.1):
	raise Exception('Please CHECK contouring - Volume of OR; Testes might be less than 0.1 ccm!')
# - check for finite External volume
volcheck = roi.RoiGeometries[external].GetRoiVolume()
if (volcheck < 0.1):
	raise Exception('Please CHECK contouring - Volume of External might be less than 0.1 ccm!')
# - check for finite Couch Model volume
volcheck = roi.RoiGeometries[pelvicCouchModel].GetRoiVolume()
if (volcheck < 0.1):
	raise Exception('Please CHECK Couch Model - this geometry might not have been included!')
#
#
# ----------- only for future workflow
# EXTERNAL body contour will be created using scripted threshold-based segmentation
# In future, we will initialize an empty structure set with the following structures
# BLAERE
# RECTUM
# ANAL CANAL
# BULBUS PENIS
# TESTES
# CTV-T
# CTV-SV *where applicable
#
#
#with CompositeAction('Create External (External)'):
#	pm.CreateRoi(Name=external, Color="Orange", Type="External", TissueName=None, RoiMaterial=None)
#	pm.RegionsOfInterest[external].CreateExternalGeometry(Examination=examination, ThresholdLevel=externalContourThreshold)
#	# CompositeAction ends
#
#


# 2. Assign CT Density Table
# OVERWRITE current simulation modality to the REQUIRED density table name
try:
	examination.EquipmentInfo.SetImagingSystemReference(ImagingSystemName = densityConversionTable)
except Exception:
	print 'Failed to find matching name in list of commissioned CT scanners'


# 3. Define density override material for region adjacent to fiducial markers
# find muscle in the materials template and clone it as soft tissue with density override 1.060 g/ccm
try:
	index = IndexOfMaterial(patient_db.TemplateMaterials[0].Materials,'Muscle')
	pm.CreateMaterial(BaseOnMaterial=patient_db.TemplateMaterials[0].Materials[index], Name = "IcruSoftTissue", MassDensityOverride = 1.060)
except Exception:
	print 'Failed to generate override ROI. Continues...'
# ------- GROW DENSITY OVERRIDE REGION AROUND IMPLANTED GOLD MARKERS
try:
	index = IndexOfMaterial(pm.Materials,'IcruSoftTissue')
	OverrideFiducialsDensity(pm,examination,index)
except Exception:
	print 'Failed to complete soft tissue density override around fiducials markers. Continues...'


# 4. Grow all required structures from the initial set
# --------- FEMORALS HEADS will be approximated using built-in MALE PELVIS Model Based Segmentation
#get_current("ActionVisibility:Internal") # needed due to that MBS actions not visible in evaluation version.
pm.MBSAutoInitializer(MbsRois=[
	{ 'CaseType': "PelvicMale", 'ModelName': "FemoralHead (Left)", 'RoiName': femHeadLeft, 'RoiColor': colourCaputFemori }, 
	{ 'CaseType': "PelvicMale", 'ModelName': "FemoralHead (Right)", 'RoiName': femHeadRight, 'RoiColor': colourCaputFemori }],
	CreateNewRois=True, Examination=examination, UseAtlasBasedInitialization=True)
pm.AdaptMbsMeshes(Examination=examination, RoiNames=[femHeadLeft, femHeadRight], CustomStatistics=None, CustomSettings=None)
#
# ---------- GROW RECTAL HELP VOLUME FOR IGRT
CreateWallHvRectum(pm,examination)
#
# ---------- GROW ALL PTVs
CreateMarginPtvT(pm,examination) #all prostate types
CreateMarginPtvSV(pm,examination) #all prostate types except Type A
CreateUnionPtvTSV(pm,examination) #all prostate types except Type A
#
# ----------- Conformity structure - Wall; PTV-TSV+5mm
try:
	pm.CreateRoi(Name=wall5mmPtvTSV, Color="Blue", Type="Avoidance", TissueName=None, RoiMaterial=None)
	pm.RegionsOfInterest[wall5mmPtvTSV].SetWallExpression(SourceRoiName=ptvTSV, OutwardDistance=0.5, InwardDistance=0)
	pm.RegionsOfInterest[wall5mmPtvTSV].UpdateDerivedGeometry(Examination=examination)
except Exception:
	print 'Failed to create Wall;PTV-TSV+5mm. Continues ...'
#
#------------- Suppression roi for low dose wash - Ext-(PTV-TSV+5mm)
try :
	pm.CreateRoi(Name=complementExt5mmPtvTsv, Color="Gray", Type="Avoidance", TissueName=None, RoiMaterial=None)
	pm.RegionsOfInterest[complementExt5mmPtvTsv].SetAlgebraExpression(
		ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [external], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
		ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvTSV], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
		ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
	pm.RegionsOfInterest[complementExt5mmPtvTsv].UpdateDerivedGeometry(Examination=examination)
except Exception:
		print 'Failed to create Ext-(PTV-TSV+5mm). Continues...'
#
# ------------- ANATOMY PREPARATION COMPLETE
# --------- save the active plan
patient.Save()


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




# 5 - 7. Define unique plan, beamset and dosegrid
#---------- auto-generate a unique plan name if the name ProstC_78_39 already exists
planName = 'ProstC_78_39'
planName = UniquePlanName(planName, case)
#
beamSetPrimaryName = 'Arc1' #prepares a single CC arc VMAT for the primary field
examinationName = examination.Name
#
# --------- Setup a standard VMAT protocol plan
with CompositeAction('Adding plan with name {0} '.format(planName)):
    # add plan
    plan = case.AddNewPlan(PlanName=planName, Comment="Single CC arc prostate VMAT ", ExaminationName=examinationName)
	# set standard dose grid size
    plan.SetDefaultDoseGrid(VoxelSize={'x':defaultDoseGrid, 'y':defaultDoseGrid, 'z':defaultDoseGrid})
	# set the dose grid size to cover
    # add only one beam set
    beamSetArc1 = plan.AddNewBeamSet(Name = beamSetPrimaryName, ExaminationName = examinationName,
		MachineName = defaultLinac, Modality = "Photons",
		TreatmentTechnique = "VMAT", PatientPosition = "HeadFirstSupine", NumberOfFractions = defaultFractions,
		CreateSetupBeams = False)
# Save the current patient
patient.Save()


# Load the current plan and beamset into the system
LoadPlanAndBeamSet(case, plan, beamSetArc1)


# 9 - 11. Create beam list, clinical goals and optimisation functions for the first beam set
with CompositeAction('Add beams, clinical goals and optimization functions'):
	# ----- no need to add prescription for dynamic delivery
	#beamSetArc1.AddDosePrescriptionToRoi(RoiName = ptvTSV, PrescriptionType = "AverageDose", DoseValue = defaultPrescDose, DoseVolume = 0, RelativePrescriptionLevel = 1)
	#
	# ----- set the plan isocenter to the centre of the reference ROI
	isocenter = pm.StructureSets[examinationName].RoiGeometries[ptvTSV].GetCenterOfRoi()
	isodata = beamSetArc1.CreateDefaultIsocenterData(Position={'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	#
	# ------ load single counterclockwise full arc
	beamSetArc1.CreateArcBeam(Name='Arc1', Energy=defaultPhotonEn, CouchAngle=0, GantryAngle=179.9, ArcStopGantryAngle=180.1, ArcRotationDirection='CounterClockwise', CollimatorAngle = 45, IsocenterData = isodata)
	#
	# deprecate - add 7 static IMRT fields around the ROI-based isocenter
	#beamSetImrt.CreatePhotonBeam(Name = '1; T154A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 154, CollimatorAngle = 15, Isocenter = {'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	#beamSetImrt.CreatePhotonBeam(Name = '2; T102A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 102, CollimatorAngle = 345, Isocenter = {'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	#beamSetImrt.CreatePhotonBeam(Name = '3; T050A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 50, CollimatorAngle = 45, Isocenter = {'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	#beamSetImrt.CreatePhotonBeam(Name = '4; T206A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 206, CollimatorAngle = 345, Isocenter = {'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	#beamSetImrt.CreatePhotonBeam(Name = '5; T258A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 258, CollimatorAngle = 15, Isocenter = {'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	#beamSetImrt.CreatePhotonBeam(Name = '6; T310A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 310, CollimatorAngle = 315, Isocenter = {'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	#beamSetImrt.CreatePhotonBeam(Name = '7; T000A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 0, CollimatorAngle = 0, Isocenter = {'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	#
#
# ------- import clinical goals from a predefined template
plan.TreatmentCourse.EvaluationSetup.ApplyClinicalGoalTemplate(Template=patient_db.TemplateTreatmentOptimizations[defaultClinicalGoalsProstC])
#
# ------- import optimization functions from a predefined template
plan.PlanOptimizations[0].ApplyOptimizationTemplate(Template=patient_db.TemplateTreatmentOptimizations[defaultOptimVmatProstC])
# Save the current beamset
patient.Save()


# 12. set opt parameters and run first optimization for the VMAT plan
optimPara = plan.PlanOptimizations[0].OptimizationParameters #shorter handle
# - set the maximum limit on the number of iterations
optimPara.Algorithm.MaxNumberOfIterations = 80
# - set optimality tolerance level
optimPara.Algorithm.OptimalityTolerance = 1E-08
# - set to compute intermediate and final dose
optimPara.DoseCalculation.ComputeFinalDose = 'True'
optimPara.DoseCalculation.ComputeIntermediateDose = 'True'
# - set number of iterations in preparation phase
optimPara.DoseCalculation.InterationsInPreparationsPhase = 20
# - constraint arc segmentation for machine deliverability
optimPara.SegmentConversion.ArcConversionProperties.USeMaxLeafTravelDistancePerDegree = 'True'
optimPara.SegmentConversion.ArcConversionProperties.MaxLeafTravelDistancePerDegree = 0.40
#
#
patient.Save()
# - execute first run optimization
plan.PlanOptimizations[0].RunOptimization()	


# 13. compute final dose not necessary due to optimization setting
#beamSetArc1.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="CCDose", ForceRecompute=False)


# Save final
patient.Save()
#
#
#
#
#
#
#end of AUTOPLAN





