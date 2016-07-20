import math
from connect import *
import time
import sys
clr.AddReference("PresentationFramework")
from System.Windows import *

from PROS_Alle_Definitions import *

# Define null filter
filter = {}

# Get handle to current patient database
patient_db = get_current('PatientDB')

# Define patient and examination handles
patient = get_current('Patient')
examination = get_current('Examination')
case = get_current('Case')

#### PROSTATE TYPE S (Salvage) AUTO-PLAN
#### 78Gy/39F Normo-fractionated prescribed to PTV-T only
#### As a VMAT 1 arc solution
#### With a 7-field IMRT beam as a fall-back plan

defaultPrescDose = 7000 #the absolute prescribed dose in cGy
defaultFractions = 35 #standard number of fractions

# -------- Define composite handle for PATIENT ANATOMY MODELLING
pm = case.PatientModel
rois = pm.StructureSets[examination.Name]
# --- the plan shall NOT be made without the following required Rois
RequiredRois = [ctvT, rectum, bladder, analCanal, penileBulb, testes, pelvicCouchModel]
# --- the script shall REGENERATE each of the following Rois each time
#therefore if they already exist, delete first
ScriptedRois = [external, femHeadLeft, femHeadRight, hvRect, marker1, marker2, marker3, marker4, marker5, marker6, ptvT, wall5mmPtvT, complementExt5mmPtvT]
#the following structures are excluded from DICOM export to the linear acc to help the nurses
ExcludedRois = [wall5mmPtvT, complementExt5mmPtvT]
#the following ROIs are generated as intermediate processes, and should be removed before running the script
TemporaryRois = ['temp_ext', 'supports', 'Temp1', 'Temp2', 'Temp3', 'Temp4', 'Temp5', 'Temp6']


#---------- auto-generate a unique planname if the given planname already exists
planName = 'ProstS_70_35'
planName = UniquePlanName(planName, case)
#
beamSetPrimaryName = planName #prepares a single CC arc VMAT for the primary field
beamArcPrimaryName = 'A1'
examinationName = examination.Name




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
#
# - confirm that the required rois for autoplanning have been drawn
minVolume = 1 #at least 1cc otherwise the ROI does not make sense or might be empty
for r in RequiredRois:
	try :
		v = rois.RoiGeometries[r].GetRoiVolume()
		if v < minVolume :
			raise Exception('The volume of '+r+' seems smaller than required ('+minVolume+'cc).')
	except Exception :
		raise Exception('Please check structure set : '+r+' appears to be missing.')
#
for sr in ScriptedRois:
	try:
		pm.RegionsOfInterest[sr].DeleteRoi()
		print 'Deleted - scripting will be used to generate fresh '+sr+'.'
	except Exception:
		print 'Scripting will be used to generate '+sr+'.'
#
for sr in TemporaryRois:
	try:
		pm.RegionsOfInterest[sr].DeleteRoi()
		print 'Deleted - scripting will be used to generate fresh '+sr+'.'
	except Exception:
		print 'Scripting will be used to generate '+sr+'.'
#
numLP = 0
for lp in pm.PointsOfInterest:
	if (lp.Type == 'LocalizationPoint'):
		numLP = numLP + 1
if (numLP < 1):
	raise Exception('No localization point defined - please define using POI Tools.')




# ----------- only for future workflow
# EXTERNAL body contour will be initially created using threshold-based segmentation
# In future, we will initialize an empty structure set with the following structures
# BLAERE
# RECTUM
# ANAL CANAL
# BULBUS PENIS
# TESTES
# CTV-T
# CTV-SV *where applicable
#
#Then the physician will define finite boundaries for the above ROIs


# 2. Assign CT Density Table
# OVERWRITE current simulation modality to the REQUIRED density table name
try:
	examination.EquipmentInfo.SetImagingSystemReference(ImagingSystemName = densityConversionTable)
except Exception:
	print 'Failed to find matching name in list of commissioned CT scanners'


# 3. Define density override material for region adjacent to fiducial markers
# find muscle in the materials template and clone it as soft tissue with density override 1.060 g/ccm
test = IndexOfMaterial(pm.Materials,'IcruSoftTissue')
if test < 0:
	try:
		index = IndexOfMaterial(patient_db.TemplateMaterials[0].Materials,'Muscle')
		pm.CreateMaterial(BaseOnMaterial=patient_db.TemplateMaterials[0].Materials[index], Name = "IcruSoftTissue", MassDensityOverride = 1.060)
	except Exception:
		print 'Not able to generate new material based on template material. Continues...'
# ------- GROW DENSITY OVERRIDE REGION AROUND IMPLANTED GOLD MARKERS
try:
	index = IndexOfMaterial(pm.Materials,'IcruSoftTissue')
	OverrideFiducialsDensity(pm,examination,index)
except Exception:
	print 'Failed to complete soft tissue density override around fiducials markers. Continues...'


# 4. Grow all required structures from the initial set
# --------- EXTERNAL will be set using threshold contour generate at the user-defined intensity value
pm.CreateRoi(Name='temp_ext', Color="Orange", Type="External", TissueName=None, RoiMaterial=None)
pm.RegionsOfInterest['temp_ext'].CreateExternalGeometry(Examination=examination, ThresholdLevel=externalContourThreshold)
#
#the above temporary external typically includes bit of sim couch therefore the true
#External needs to be generated from the temp external
pm.CreateRoi(Name=external, Color="Orange", Type="Organ", TissueName=None, RoiMaterial=None)
pm.RegionsOfInterest[external].SetAlgebraExpression(
		ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['temp_ext'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
		ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [pelvicCouchModel], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
		ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
pm.RegionsOfInterest[external].UpdateDerivedGeometry(Examination=examination)
pm.RegionsOfInterest[external].SetAsExternal()
#
#then remove the temporary external
pm.RegionsOfInterest['temp_ext'].DeleteRoi()
#
#and simplify straggly bits of the remaining true External
rois.SimplifyContours(RoiNames=[external], RemoveHoles3D='False', RemoveSmallContours='True', AreaThreshold=10, ReduceMaxNumberOfPointsInContours='False', MaxNumberOfPoints=None, CreateCopyOfRoi='False')
#
# FEMORALS HEADS will be approximated using built-in MALE PELVIS Model Based Segmentation
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
CreateMarginPtvT(pm,examination)
#
# ----------- Conformity structure - Wall; PTV-T+5mm
try:
	pm.CreateRoi(Name=wall5mmPtvT, Color=colourWallStructures, Type="Avoidance", TissueName=None, RoiMaterial=None)
	pm.RegionsOfInterest[wall5mmPtvT].SetWallExpression(SourceRoiName=ptvT, OutwardDistance=0.5, InwardDistance=0)
	pm.RegionsOfInterest[wall5mmPtvT].UpdateDerivedGeometry(Examination=examination)
except Exception:
	print 'Failed to create Wall;PTV-T+5mm. Continues ...'
#
#------------- Suppression roi for low dose wash - Ext-(PTV-T+5mm)
try :
	pm.CreateRoi(Name=complementExt5mmPtvT, Color=colourComplementExternal, Type="Avoidance", TissueName=None, RoiMaterial=None)
	pm.RegionsOfInterest[complementExt5mmPtvT].SetAlgebraExpression(
		ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [external], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
		ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvT], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
		ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
	pm.RegionsOfInterest[complementExt5mmPtvT].UpdateDerivedGeometry(Examination=examination)
except Exception:
		print 'Failed to create Ext-(PTV-T+5mm). Continues...'
#
#-------------- Exclude help rois used only for planning and optimization from dicom export
for e in ExcludedRois:
	try :
		rois.RoiGeometries[e].OfRoi.ExcludeFromExport = 'True'
	except Exception :
		raise Exception('Please check structure set : '+e+' cannot be excluded from DCM export.')
# ------------- ANATOMY PREPARATION COMPLETE
# --------- save the active plan
patient.Save()


#
# ------------- AUTO VMAT PLAN CREATION
#

# 5 - 7. Define unique plan, beamset and dosegrid
# --------- Setup a standard VMAT protocol plan
with CompositeAction('Adding plan with name {0} '.format(planName)):
    # add plan
    plan = case.AddNewPlan(PlanName=planName, Comment="Single CC arc prostate VMAT ", ExaminationName=examinationName)
	# set standard dose grid size
    plan.SetDefaultDoseGrid(VoxelSize={'x':defaultDoseGrid, 'y':defaultDoseGrid, 'z':defaultDoseGrid})
	# set the dose grid size to cover
    # add only one beam set
    beamSetArc1 = plan.AddNewBeamSet(Name = beamSetPrimaryName, ExaminationName = examinationName,
		MachineName = defaultLinac, Modality = "Photons", TreatmentTechnique = "VMAT",
		PatientPosition = "HeadFirstSupine", NumberOfFractions = defaultFractions, CreateSetupBeams = False)


# Load the current plan and beamset into the system
LoadPlanAndBeamSet(case, plan, beamSetArc1)


# 8. Create beam list
with CompositeAction('Create arc beam'):
	# ----- no need to add prescription for dynamic delivery
	beamSetArc1.AddDosePrescriptionToRoi(RoiName = ptvT, PrescriptionType = "NearMinimumDose", DoseValue = 6650, RelativePrescriptionLevel = 1, AutoScaleDose='False')
	#
	# ----- set the plan isocenter to the centre of the reference ROI
	isocenter = pm.StructureSets[examinationName].RoiGeometries[ptvT].GetCenterOfRoi()
	isodata = beamSetArc1.CreateDefaultIsocenterData(Position={'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	# ------ load single counterclockwise full arc
	beamSetArc1.CreateArcBeam(Name=beamArcPrimaryName, Description=beamArcPrimaryName, Energy=defaultPhotonEn, CouchAngle=0, GantryAngle=179.9, ArcStopGantryAngle=180.1, ArcRotationDirection='CounterClockwise', CollimatorAngle = 45, IsocenterData = isodata)
#

patient.Save()

# 9. Set a predefined template manually for v.5.0.1 or before
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=rectum,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.12,ParameterValue=7400,IsComparativeGoal='False',Priority=1)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=rectum,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.20,ParameterValue=7000,IsComparativeGoal='False',Priority=2)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=ctvT,GoalCriteria='AtLeast',GoalType='DoseAtVolume',AcceptanceLevel=6650,ParameterValue=1.00,IsComparativeGoal='False',Priority=3)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=ptvT,GoalCriteria='AtLeast',GoalType='DoseAtVolume',AcceptanceLevel=6650,ParameterValue=0.98,IsComparativeGoal='False',Priority=4)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=ptvT,GoalCriteria='AtMost',GoalType='DoseAtVolume',AcceptanceLevel=7350,ParameterValue=0.01,IsComparativeGoal='False',Priority=4)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=analCanal,GoalCriteria='AtMost',GoalType='AverageDose',AcceptanceLevel=3000,ParameterValue=0,IsComparativeGoal='False',Priority=7)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=bladder,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.30,ParameterValue=7000,IsComparativeGoal='False',Priority=8)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=bladder,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.50,ParameterValue=5500,IsComparativeGoal='False',Priority=9)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=rectum,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.50,ParameterValue=5000,IsComparativeGoal='False',Priority=9)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=external,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.01,ParameterValue=7350,IsComparativeGoal='False',Priority=10)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=penileBulb,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.50,ParameterValue=4000,IsComparativeGoal='False',Priority=11)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=femHeadLeft,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.05,ParameterValue=5000,IsComparativeGoal='False',Priority=12)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=femHeadRight,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.05,ParameterValue=5000,IsComparativeGoal='False',Priority=12)

# 9. Set a predefined template directly from the clinical database for v.5.0.2
plan.TreatmentCourse.EvaluationSetup.ApplyClinicalGoalTemplate(Template=patient_db.TemplateTreatmentOptimizations[defaultClinicalGoalsProstS])

# 10. import optimization functions from a predefined template
plan.PlanOptimizations[0].ApplyOptimizationTemplate(Template=patient_db.TemplateTreatmentOptimizations[defaultOptimVmatProstS])

# 11. set opt parameters and run first optimization for the VMAT plan
optimPara = plan.PlanOptimizations[0].OptimizationParameters #shorter handle
# - set the maximum limit on the number of iterations
optimPara.Algorithm.MaxNumberOfIterations = 40
# - set optimality tolerance level
optimPara.Algorithm.OptimalityTolerance = 1E-05
# - set to compute intermediate and final dose
optimPara.DoseCalculation.ComputeFinalDose = 'True'
optimPara.DoseCalculation.ComputeIntermediateDose = 'True'
# - set number of iterations in preparation phase
optimPara.DoseCalculation.IterationsInPreparationsPhase = 7
# - constraint arc segmentation for machine deliverability
optimPara.SegmentConversion.ArcConversionProperties.UseMaxLeafTravelDistancePerDegree = 'True'
optimPara.SegmentConversion.ArcConversionProperties.MaxLeafTravelDistancePerDegree = 0.40
#


# 12. Execute first run optimization with final dose (as set above in opt settings)
plan.PlanOptimizations[0].RunOptimization()	
# ---- trigger just one additional warmstart
plan.PlanOptimizations[0].RunOptimization()	

# 13. compute final dose not necessary due to optimization setting
#beamSetArc1.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="CCDose", ForceRecompute=False)

bNum = 1
# set beam number(s)
for b in beamSetArc1.Beams :
	b.Number = bNum
	bNum = bNum + 1


# Save VMAT auto-plan result
patient.Save()
#


#
# ------------- AUTO IMRT FALLBACK PLAN CREATION
#
# 5 - 7. Define unique plan, beamset and dosegrid
#---------- redefine the plan name parameter
planName = 'ProstS_70_35_fb'
planName = UniquePlanName(planName, case)
#
beamSetPrimaryName = planName #prepares a standard 7-fld StepNShoot IMRT
#
# --------- Setup a standard IMRT protocol plan
with CompositeAction('Adding plan with name {0} '.format(planName)):
    # add plan
    plan = case.AddNewPlan(PlanName=planName, Comment="7-fld SMLC prostate IMRT ", ExaminationName=examinationName)
	# set standard dose grid size
    plan.SetDefaultDoseGrid(VoxelSize={'x':defaultDoseGrid, 'y':defaultDoseGrid, 'z':defaultDoseGrid})
	# set the dose grid size to cover
    # add only one beam set
    beamSetImrt = plan.AddNewBeamSet(Name = beamSetPrimaryName, ExaminationName = examinationName,
		MachineName = defaultLinac, Modality = "Photons", TreatmentTechnique = "SMLC",
		PatientPosition = "HeadFirstSupine", NumberOfFractions = defaultFractions, CreateSetupBeams = False)


# Load the current plan and beamset into the system
LoadPlanAndBeamSet(case, plan, beamSetImrt)


# 8. Create beam list
with CompositeAction('Create StepNShoot beams'):
	# ----- no need to add prescription for dynamic delivery
	beamSetImrt.AddDosePrescriptionToRoi(RoiName = ptvT, PrescriptionType = "NearMinimumDose", DoseValue = 6650, RelativePrescriptionLevel = 1, AutoScaleDose='False')
	#
	# ----- set the plan isocenter to the centre of the reference ROI
	isocenter = pm.StructureSets[examinationName].RoiGeometries[ptvT].GetCenterOfRoi()
	isodata = beamSetImrt.CreateDefaultIsocenterData(Position={'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	# add 7 static IMRT fields around the ROI-based isocenter
	beamSetImrt.CreatePhotonBeam(Name = 'T154A', Description = 'T154A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 154, CollimatorAngle = 15, IsocenterData = isodata)
	beamSetImrt.CreatePhotonBeam(Name = 'T102A', Description = 'T102A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 102, CollimatorAngle = 345, IsocenterData = isodata)
	beamSetImrt.CreatePhotonBeam(Name = 'T050A', Description = 'T050A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 50, CollimatorAngle = 45, IsocenterData = isodata)
	beamSetImrt.CreatePhotonBeam(Name = 'T206A', Description = 'T206A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 206, CollimatorAngle = 345, IsocenterData = isodata)
	beamSetImrt.CreatePhotonBeam(Name = 'T258A', Description = 'T258A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 258, CollimatorAngle = 15, IsocenterData = isodata)
	beamSetImrt.CreatePhotonBeam(Name = 'T310A', Description = 'T310A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 310, CollimatorAngle = 315, IsocenterData = isodata)
	beamSetImrt.CreatePhotonBeam(Name = 'T000A', Description = 'T000A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 0, CollimatorAngle = 0, IsocenterData = isodata)
#

patient.Save()

# 9. Set a predefined template manually for v.5.0.1 or before
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=rectum,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.12,ParameterValue=7400,IsComparativeGoal='False',Priority=1)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=rectum,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.20,ParameterValue=7000,IsComparativeGoal='False',Priority=2)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=ctvT,GoalCriteria='AtLeast',GoalType='DoseAtVolume',AcceptanceLevel=6650,ParameterValue=1.00,IsComparativeGoal='False',Priority=3)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=ptvT,GoalCriteria='AtLeast',GoalType='DoseAtVolume',AcceptanceLevel=6650,ParameterValue=0.98,IsComparativeGoal='False',Priority=4)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=ptvT,GoalCriteria='AtMost',GoalType='DoseAtVolume',AcceptanceLevel=7350,ParameterValue=0.01,IsComparativeGoal='False',Priority=4)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=analCanal,GoalCriteria='AtMost',GoalType='AverageDose',AcceptanceLevel=3000,ParameterValue=0,IsComparativeGoal='False',Priority=7)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=bladder,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.30,ParameterValue=7000,IsComparativeGoal='False',Priority=8)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=bladder,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.50,ParameterValue=5500,IsComparativeGoal='False',Priority=9)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=rectum,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.50,ParameterValue=5000,IsComparativeGoal='False',Priority=9)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=external,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.01,ParameterValue=7350,IsComparativeGoal='False',Priority=10)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=penileBulb,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.50,ParameterValue=4000,IsComparativeGoal='False',Priority=11)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=femHeadLeft,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.05,ParameterValue=5000,IsComparativeGoal='False',Priority=12)
#plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=femHeadRight,GoalCriteria='AtMost',GoalType='VolumeAtDose',AcceptanceLevel=0.05,ParameterValue=5000,IsComparativeGoal='False',Priority=12)

# 9. Set a predefined template directly from the clinical database for v.5.0.2
plan.TreatmentCourse.EvaluationSetup.ApplyClinicalGoalTemplate(Template=patient_db.TemplateTreatmentOptimizations[defaultClinicalGoalsProstS])

# 10. import optimization functions from a predefined template
plan.PlanOptimizations[0].ApplyOptimizationTemplate(Template=patient_db.TemplateTreatmentOptimizations[defaultOptimVmatProstS])

# 11. set opt parameters and run first optimization for the IMRT plan
optimPara = plan.PlanOptimizations[0].OptimizationParameters #shorter handle
# - set the maximum limit on the number of iterations
optimPara.Algorithm.MaxNumberOfIterations = 40
# - set optimality tolerance level
optimPara.Algorithm.OptimalityTolerance = 1E-05
# - set to compute intermediate and final dose
optimPara.DoseCalculation.ComputeFinalDose = 'True'
optimPara.DoseCalculation.ComputeIntermediateDose = 'True'
# - set number of iterations in preparation phase
optimPara.DoseCalculation.IterationsInPreparationsPhase = 7
# - constraint arc segmentation for machine deliverability
#optimPara.SegmentConversion.ArcConversionProperties.UseMaxLeafTravelDistancePerDegree = 'True'
#optimPara.SegmentConversion.ArcConversionProperties.MaxLeafTravelDistancePerDegree = 0.40
# - constrain SMLC segmentation parameters for machine deliverability
optimPara.SegmentConversion.MaxNumberOfSegments = 70
optimPara.SegmentConversion.MinEquivalentSquare = 2
optimPara.SegmentConversion.MinLeafEndSeparation = 0.5
optimPara.SegmentConversion.MinNumberOfOpenLeafPairs = 4
optimPara.SegmentConversion.MinSegmentArea = 4
optimPara.SegmentConversion.MinSegmentMUPerFraction = 4


# 12. Execute first run optimization with final dose (as set above in opt settings)
plan.PlanOptimizations[0].RunOptimization()
# one more as warm start
plan.PlanOptimizations[0].RunOptimization()

# 13. compute final dose not necessary due to optimization setting
#beamSetArc1.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="CCDose", ForceRecompute=False)

# set beam number(s)
bNum = 11
for b in beamSetImrt.Beams :
	b.Number = bNum
	bNum = bNum + 1


# Save IMRT auto-plan result
patient.Save()
#
#
#
#
#end of AUTOPLAN





