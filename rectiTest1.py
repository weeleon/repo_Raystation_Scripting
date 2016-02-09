# Script recorded 03 Feb 2016

#   RayStation version: 4.7.2.5
#   Selected patient: ...

from connect import *

#example of a path query
patient_db = get_current('PatientDB')
myPath = r'S:/Patients'
myFilter = {}
query = patient_db.QueryPatientsFromPath(Path=myPath, Filter=myFilter)
for i, q in enumerate(query):
	print i,query[i]['Name']







#user specific environment
clinicGridResolution = { 'x': 0.25, 'y': 0.25, 'z': 0.25 }
clinicMachineName = "ElektaAgility"
clinicMachineCT = "CT 1"

#define data structure
patient = get_current("Patient")
examination = get_current("Examination")



def UniquePlanName(name, pat):
	for p in pat.TreatmentPlans:
		if name == p.Name:
			name = name + '_1'
			name = UniquePlanName(name, pat)
	return name
#conclude function def

#initialise plan name
myPlanName = 'Recti_2arc'
myPlanName = UniquePlanName(myPlanName, patient)
myExaminationName = examination.Name
myPlanIso = patient.PatientModel.StructureSets[myExaminationName].RoiGeometries['PTV'].GetCenterOfRoi()
#note expando object here



with CompositeAction('Add Treatment plan'):
  retval_0 = patient.AddNewPlan(PlanName=myPlanName, PlannedBy="", Comment="", ExaminationName=clinicMachineCT, AllowDuplicateNames=False)
  retval_0.SetDefaultDoseGrid(VoxelSize=clinicGridResolution)
  retval_1 = retval_0.AddNewBeamSet(Name="Beam_1", ExaminationName=clinicMachineCT, MachineName=clinicMachineName, NominalEnergy=None, Modality="Photons", TreatmentTechnique="VMAT", PatientPosition="HeadFirstSupine", NumberOfFractions=28, CreateSetupBeams=False, UseLocalizationPointAsSetupIsocenter=False, Comment="")
  retval_1.AddDosePrescriptionToRoi(RoiName="PTV", DoseVolume=0, PrescriptionType="AverageDose", DoseValue=5040, RelativePrescriptionLevel=1, AutoScaleDose=False)
  retval_1.CreateArcBeam(ArcStopGantryAngle=180.1, ArcRotationDirection="CounterClockwise", Energy=6, MachineCone=None, Isocenter={ 'x': myPlanIso.x, 'y': myPlanIso.y, 'z': myPlanIso.z }, Name="VMAT_1", Description="", GantryAngle=179.9, CouchAngle=0, CollimatorAngle=45, ApertureBlock=None)
  retval_1.CreateArcBeam(ArcStopGantryAngle=179.9, ArcRotationDirection="Clockwise", Energy=6, MachineCone=None, Isocenter={ 'x': myPlanIso.x, 'y': myPlanIso.y, 'z': myPlanIso.z }, Name="VMAT_2", Description="", GantryAngle=180.1, CouchAngle=0, CollimatorAngle=315, ApertureBlock=None)
  # CompositeAction ends


patient.Save()


plan = patient.TreatmentPlans['Recti_2arc']
beamset = plan.BeamSets['Beam_1']

po = plan.PlanOptimizations[0].CreateMco()
top = po.TemplateOptimizationProblem

#first pareto function
mcoFn1 = top.AddOptimizationFunction(RoiName='PTV', FunctionType='MinDvh')
mcoFn1.DoseFunctionParameters.DoseLevel = 4980
mcoFn1.DoseFunctionParameters.PercentVolume = 98.8

# po = plan.PlanOptimizations[0]
# poSetting = po.OptimizationParameters
# poSetting.Algorithm.MaxNumberOfIterations = 80
# poSetting.DoseCalculation.IterationsInPreparationsPhase = 10
# poSetting.DoseCalculation.ComputeFinalDose = True
# poSetting.DoseCalculation.ComputeIntermediateDose = True

# #first objective function
# function1 = po.AddOptimizationFunction(RoiName='PTV', FunctionType='MinDvh')
# function1.DoseFunctionParameters.DoseLevel = 4980
# function1.DoseFunctionParameters.PercentVolume = 98.8
# function1.DoseFunctionParameters.Weight = 6000
# #second objective function
# function2 = po.AddOptimizationFunction(RoiName='PTV', FunctionType='MaxDvh')
# function2.DoseFunctionParameters.DoseLevel = 5393
# function2.DoseFunctionParameters.PercentVolume = 1
# function2.DoseFunctionParameters.Weight = 1000
# #external objective function
# function3 = po.AddOptimizationFunction(RoiName='External', FunctionType='DoseFallOff')
# function3.DoseFunctionParameters.HighDoseLevel = 5040
# function3.DoseFunctionParameters.LowDoseLevel = 2500
# function3.DoseFunctionParameters.LowDoseDistance = 2.4
# function3.DoseFunctionParameters.Weight = 10
# #constraining ring help volume
# function4 = po.AddOptimizationFunction(RoiName='_R1', FunctionType='MaxEud')
# function4.DoseFunctionParameters.DoseLevel = 4788
# function4.DoseFunctionParameters.EudParameterA = 1
# function4.DoseFunctionParameters.Weight = 50

# patient.Save()




# po.RunOptimization()






 
 
