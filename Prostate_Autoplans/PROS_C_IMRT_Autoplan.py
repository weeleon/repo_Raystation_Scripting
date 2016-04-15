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

# DEFINE THE NAMES OF THE STANDARD CLINICAL GOALS AND OPTIMIZATION FUNCTIONS
templateClinicalGoals = 'Pros C - Clinical Goals'
templateOptimizationFunctions = 'Pros C - Objective Functions'
#templateOptimizationFunctions = 'Pros C - MCO Tradeoffs' #the other alternative is MCO
# 
# names of the other clinical goals and optimisation templates
#templateClinicalGoals = 'Pros B - Clinical Goals'
#templateClinicalGoals = 'Pros N - Clinical Goals'
#templateClinicalGoals = 'Pros S - Clinical Goals'

# NOTE A TEMPLATE BEAMSET IS NOT DEFINED THROUGH A FUNCTION CALL TO APPLY A TEMPLATE
# but rather each field in the beamset has been explicitly defined using
# the 'CreatePhotonBeam' method acting on a BeamSet instance - see lines in script

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

# --- IMPORTANT : CREATE NEW MATERIAL BASED ON ATOMIC COMPOSITIONS OF STANDARD MUSCLE -> copy as SoftTissue with density override 1.060 g/ccm
#standard muscle is "db.TemplateMaterials[0].Materials[14]"
try:
	patient.PatientModel.CreateMaterial(BaseOnMaterial=db.TemplateMaterials[0].Materials[14], Name = "SoftTissue", MassDensityOverride = 1.060)
except Exception:
	print 'Failed to generate override ROI. Continues...'

# GROW DENSITY OVERRIDE REGION AROUND IMPLANTED GOLD MARKERS
OverrideFiducialsDensity(patient.PatientModel,examination)

# GROW RECTAL HELP VOLUME FOR IGRT
CreateWallHvRectum(patient.PatientModel,examination)

# PLAN PREPARATION COMPLETE - save the active plan and manually check/edit plan before inverse planning
patient.Save()

#
# - PLAN CREATION BEGINS
#
# Define plan set and beam set and density dataset handles
planName = 'ProstC_78_39'
planName = UniquePlanName(planName, patient) #auto-generate a unique plan name if ProstC_78_39 already exists
beamSetImrtName = 'Primaer' #prepares a 7-field IMRT standard primary beamset
beamSetBoostName = 'Boost' #prepares a 7-field IMRT boost beamset
examinationName = examination.Name

# GROW PLANNING VOLUMES AND STANDARD MARGINS FOR PROSTATA TYPE C
CreateMarginPtvT(patient.PatientModel,examination) #all prostate types
CreateComplementBladderPtvT(patient.PatientModel,examination) #all prostate types
CreateComplementRectumPtvT(patient.PatientModel,examination) #all prostate types
CreateWallPtvT(patient.PatientModel,examination) #all prostate types
CreateComplementExternalPtvT(patient.PatientModel,examination) #all prostate types

CreateMarginPtvSV(patient.PatientModel,examination) #all prostate types except Type A
CreateUnionPtvTSV(patient.PatientModel,examination) #all prostate types except Type A
CreateComplementBladderPtvTSV(patient.PatientModel,examination) #all prostate types except Type A
CreateComplementRectumPtvTSV(patient.PatientModel,examination) #all prostate types except Type A
CreateWallPtvTSV(patient.PatientModel,examination) #all prostate types except Type A
CreateComplementExternalPtvTSV(patient.PatientModel,examination) #all prostate types except Type A

#CreateMarginPtvE(patient.PatientModel,examination) #only for Type N+
#CreateTransitionPtvTsvPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementPtvTsvPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementBladderPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementRectumPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementBowelPtvTSV(patient.PatientModel,examination) #only for Type N+
#CreateComplementBowelPtvE(patient.PatientModel,examination) #only for Type N+
#CreateWallPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementExternalPtvE(patient.PatientModel,examination) #only for Type N+

# HELP VOLUME PREPARATION COMPLETE - save the active plan
patient.Save()


# Setup a standard IMRT protocol plan
with CompositeAction('Adding plan with name {0} '.format(planName)):
    # add plan
    plan = patient.AddNewPlan(PlanName=planName, Comment="Prostate IMRT auto-plan by Len Wee", ExaminationName=examinationName)
	# set standard dose grid size
    plan.SetDefaultDoseGrid(VoxelSize={'x':defaultDoseGrid, 'y':defaultDoseGrid, 'z':defaultDoseGrid})
	# how to set the dose grid size to cover
	#
    # add beam set
    beamSetImrt = plan.AddNewBeamSet(Name = beamSetImrtName, ExaminationName = examinationName,
		MachineName = defaultLinac, NominalEnergy = None, Modality = "Photons",
		TreatmentTechnique = "SMLC", PatientPosition = "HeadFirstSupine", NumberOfFractions = defaultFractions,
		CreateSetupBeams = False)

# Save the current patient
patient.Save()

# Load the plan and first beamset into the system
LoadPlanAndBeamSet(patient, plan, beamSetImrt)

# Create prescription, clinical goals and optimisation functions for the first beam set
with CompositeAction('Add prescription, beams, clinical goals, optimization functions'):
	# add prescription
	beamSetImrt.AddDosePrescriptionToRoi(RoiName = ptvTSV, PrescriptionType = "AverageDose", DoseValue = defaultPrescDose, DoseVolume = 0, RelativePrescriptionLevel = 1)
	#set the planning isocenter to the centre of the reference ROI
	isocenter = patient.PatientModel.StructureSets[examinationName].RoiGeometries[ptvTSV].GetCenterOfRoi()
	# add 7 static IMRT fields around the ROI-based isocenter
	beamSetImrt.CreatePhotonBeam(Name = '1; T154A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 154, CollimatorAngle = 15, Isocenter = {'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	beamSetImrt.CreatePhotonBeam(Name = '2; T102A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 102, CollimatorAngle = 345, Isocenter = {'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	beamSetImrt.CreatePhotonBeam(Name = '3; T050A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 50, CollimatorAngle = 45, Isocenter = {'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	beamSetImrt.CreatePhotonBeam(Name = '4; T206A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 206, CollimatorAngle = 345, Isocenter = {'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	beamSetImrt.CreatePhotonBeam(Name = '5; T258A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 258, CollimatorAngle = 15, Isocenter = {'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	beamSetImrt.CreatePhotonBeam(Name = '6; T310A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 310, CollimatorAngle = 315, Isocenter = {'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	beamSetImrt.CreatePhotonBeam(Name = '7; T000A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 0, CollimatorAngle = 0, Isocenter = {'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	# import clinical goals from a predefined template
	plan.TreatmentCourse.EvaluationSetup.ApplyClinicalGoalTemplate(Template=db.TemplateTreatmentOptimizations[templateClinicalGoals])
	# import optimization functions from a predefined template
	plan.PlanOptimizations[0].ApplyOptimizationTemplate(Template=db.TemplateTreatmentOptimizations[templateOptimizationFunctions])

# Save the current beamset
patient.Save()
	
# run optimization for the IMRT plan
plan.PlanOptimizations[0].RunOptimization()	

# compute final dose
beamSetImrt.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="CCDose", ForceRecompute=False)

# Save final
patient.Save()
#end of AUTOPLAN

