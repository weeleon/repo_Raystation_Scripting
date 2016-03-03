import math
from connect import *
import time
import sys
clr.AddReference("PresentationFramework")
from System.Windows import *


# DEFINE THE CT DENSITY TABLE NAME
densityConversionTable = 'HR_OEB HUsetting'
	

# Define null filter
filter = {}

# Get handle to patient db
db = get_current('PatientDB')

# Define patient and examination handles
patient = get_current('Patient')
examination = get_current('Examination')

# RESET current simulation modality to the REQUIRED HU-DENSITY MAPPING
#examination.EquipmentInfo.SetImagingSystemReference(ImagingSystemName = densityConversionTable)
#patient.Save()



#new autosegmentation using the updtaed MedFys atlas for heart, lung and spinal cord
patient.PatientModel.CreateStructuresFromAtlas(SourceTemplateName="MF-Atlas-CorPulmSpinalis",
	SourceExaminationsNames=["ThFemG1_5", "ThFemG1_6", "ThFemG1_8", "ThFemG2_4", "ThFemG2_6", "ThFemIG1_0", "ThFemIG1_2", "ThFemIG1_6", "ThFemIG2_0"],
	SourceRoiNames=["MF; Cor", "MF; Pulmo dxt", "MF; Pulmo sin","MF; Canalis spinalis"], SourcePoiNames=[], AssociateStructuresByName=True, TargetExamination=examination)


# -- process autosegmentation volumes to union the ABAS MF lung
with CompositeAction('ROI Algebra (MF; Pulmones)'):
	try:
		r4 = patient.PatientModel.CreateRoi(Name='MF; Pulmones', Color="102,0,102", Type="Organ", TissueName=None, RoiMaterial=None)
		r4.SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['MF; Pulmo dxt'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['MF; Pulmo sin'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		r4.UpdateDerivedGeometry(Examination=examination)
	except Exception:
		print 'Failed to create structure union. Continues ...'
	#end composite action

with CompositeAction('ROI Algebra (MF; PulmExGTV-T)'):
	try:
		r5 = patient.PatientModel.CreateRoi(Name='MF; PulmExGTV-T', Color="102,0,102", Type="Organ", TissueName=None, RoiMaterial=None)
		r5.SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['MF; Pulmones'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['GTV-T'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		r5.UpdateDerivedGeometry(Examination=examination)
	except Exception:
		print 'Failed to create structure subtraction. Continues ...'
	#end composite action




#intersection of new MF volumes with OR
with CompositeAction('ROI Algebra'):
	try:
		r7 = patient.PatientModel.CreateRoi(Name='dMFpulm', Color="102,0,102", Type="Organ", TissueName=None, RoiMaterial=None)
		r7.SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['MF; Pulmones'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['OR; Pulmones'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Intersection", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		r7.UpdateDerivedGeometry(Examination=examination)
	except Exception:
		print 'Failed to create structure intersection. Continues ...'
	#end composite action
with CompositeAction('ROI Algebra'):
	try:
		r8 = patient.PatientModel.CreateRoi(Name='dMFcor', Color="102,0,102", Type="Organ", TissueName=None, RoiMaterial=None)
		r8.SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['MF; Cor'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['OR; Cor'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Intersection", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		r8.UpdateDerivedGeometry(Examination=examination)
	except Exception:
		print 'Failed to create structure intersection. Continues ...'
	#end composite action
with CompositeAction('ROI Algebra'):
	try:
		r9 = patient.PatientModel.CreateRoi(Name='dMFcanalis', Color="102,0,102", Type="Organ", TissueName=None, RoiMaterial=None)
		r9.SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['MF; Canalis spinalis'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['OR; Canalis spinalis'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Intersection", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		r9.UpdateDerivedGeometry(Examination=examination)
	except Exception:
		print 'Failed to create structure intersection. Continues ...'
	#end composite action
#save final result
patient.Save()



#save before forcing computation
patient.Save()

plan = patient.TreatmentPlans['abas'] #work on abas plan
# import clinical goals from a predefined template
plan.TreatmentCourse.EvaluationSetup.ApplyClinicalGoalTemplate(Template=db.TemplateTreatmentOptimizations['mf-new-abas'])

beamset = patient.TreatmentPlans['abas'].BeamSets['abas'] #work on abas beamset

#force small dose grid
plan.SetDefaultDoseGrid(VoxelSize={'x':0.30, 'y':0.30, 'z':0.30})
beamset.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="CCDose", ForceRecompute=False)

plan.SetDefaultDoseGrid(VoxelSize={'x':0.25, 'y':0.25, 'z':0.25})
#recompute
beamset.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="CCDose", ForceRecompute=False)

#save before forcing computation
patient.Save()


