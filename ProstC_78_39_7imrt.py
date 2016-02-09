from connect import *
import os #file system libraries
import sys #system libraries

scriptsPath = 'F:/ManagedScripts' #set path to managed python scripts
os.chdir(scriptsPath) #change path to managed python scripts

#imports the module containing structure definitions and ROI-growing procedures
from C_Prostata_Integning import * 

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


# Define null filter
filter = {}

# Get handle to patient db
db = get_current('PatientDB')

# Define patient and examination handles
patient = get_current('Patient')
examination = get_current('Examination')

# STUDY PREPARATION AND FOR ALL PROSTATE TYPES
# --------------------------------------------
InitialiseDensityConversionTable() #this sets the table to "HR_OEB HUsetting"

CreateExternalBodyContour() #this draws an external contour called "External"

AutosegmentFemurAndBladder() #autosegments 'OR; Cap fem dex', 'OR; Cap fem sin' and 'OR; Blaere'

CreateWallHvRectum() #creates the cylindrical help volume around 'OR; Rectum'

OverrideFiducialsDensity() #over-rides density around fiducial markers (max of 6 seeds)

patient.Save()

#
#
# DEFINE THE STANDARD PLANNING AND PRESCRIPTION PARAMETERS
defaultLinac = 'LW_Agility_VMAT' #standard linac beam model for dose planning
defaultDoseGrid = 0.25 #isotropic dose grid dimension
defaultPhotonEn = 6 #standard photon beam modality in units of MV
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

# Define plan set and beam set and density dataset handles
planName = 'ProstC_78_39'
planName = UniquePlanName(planName, patient) #auto-generate a unique plan name if ProstC_78_39 already exists

beamSetPrimaryName = 'Primaer' #name of the primary beamset
beamSetBoostName = 'Boost' #where necessary the name of the dependent boost beamset

examinationName = examination.Name #name of the current examination

# GROW PLANNING VOLUMES AND STANDARD MARGINS FOR PROSTATA TYPE C
# --------------------------------------------------------------
CreateMarginPtvT() #used for all prostate types

CreateComplementBladderPtvT() #used for all prostate types

CreateComplementRectumPtvT() #used for all prostate types

CreateWallPtvT() #used for all prostate types

CreateComplementExternalPtvT() #all prostate types

CreateMarginPtvSV() #all prostate types except Type A

CreateUnionPtvTSV() #all prostate types except Type A

CreateComplementBladderPtvTSV() #all prostate types except Type A

CreateComplementRectumPtvTSV() #all prostate types except Type A

CreateWallPtvTSV() #all prostate types except Type A

CreateComplementExternalPtvTSV() #all prostate types except Type A

#CreateMarginPtvE() #only for Type N+
#CreateTransitionPtvTsvPtvE() #only for Type N+
#CreateComplementPtvTsvPtvE() #only for Type N+
#CreateComplementBladderPtvE() #only for Type N+
#CreateComplementRectumPtvE() #only for Type N+
#CreateComplementBowelPtvTSV() #only for Type N+
#CreateComplementBowelPtvE() #only for Type N+
#CreateWallPtvE() #only for Type N+
#CreateComplementExternalPtvE() #only for Type N+

# HELP VOLUME PREPARATION COMPLETE - save the active plan
patient.Save()


# Setup a standard IMRT protocol plan
with CompositeAction('Adding IMRT beams for name {0} '.format(planName)):
	# add plan
    plan = patient.AddNewPlan(PlanName=planName, Comment="Prostate IMRT auto-plan", ExaminationName=examinationName)
	# set standard dose grid size
    plan.SetDefaultDoseGrid(VoxelSize={'x':defaultDoseGrid, 'y':defaultDoseGrid, 'z':defaultDoseGrid})
    # add beam set
    beamSet1 = plan.AddNewBeamSet(Name = beamSetPrimaryName, ExaminationName = examinationName,
		MachineName = defaultLinac, NominalEnergy = None, Modality = "Photons",
		TreatmentTechnique = "SMLC", PatientPosition = "HeadFirstSupine", NumberOfFractions = defaultFractions,
		CreateSetupBeams = False)

# Save the current patient
patient.Save()

# Load the plan and first beamset into the system
LoadPlanAndBeamSet(patient, plan, beamSet1)


# Create prescription, clinical goals and optimisation functions for the first IMRT beamset
with CompositeAction('Add prescription, beams, clinical goals, optimization functions'):
 	# add prescription
 	beamSet1.AddDosePrescriptionToRoi(RoiName = ptvTSV, PrescriptionType = "AverageDose", DoseValue = defaultPrescDose, DoseVolume = 0, RelativePrescriptionLevel = 1)
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
beamSet1.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="CCDose", ForceRecompute=False)

# Save final
patient.Save()
#end of AUTOPLAN


