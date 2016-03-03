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
examination.EquipmentInfo.SetImagingSystemReference(ImagingSystemName = densityConversionTable)
patient.Save()

#ROI algebra to join left and right lung structures together
# -- first CK set
with CompositeAction('ROI Algebra (SD; Pulmones)'):
	try:
		r1 = patient.PatientModel.CreateRoi(Name='CK; Pulmones', Color="0,51,25", Type="Organ", TissueName=None, RoiMaterial=None)
		r1.SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['CK; Pulmo sin'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['CK; Pulmo dxt'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		r1.UpdateDerivedGeometry(Examination=examination)
	except Exception:
		print 'Failed to create structure union. Continues ...'
	#end composite action

# -- next SD set
with CompositeAction('ROI Algebra (SD; Pulmones)'):
	try:
		r2 = patient.PatientModel.CreateRoi(Name='SD; Pulmones', Color="255,128,0", Type="Organ", TissueName=None, RoiMaterial=None)
		r2.SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['SD; Pulmo sin'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['SD; Pulmo dxt'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		r2.UpdateDerivedGeometry(Examination=examination)
	except Exception:
		print 'Failed to create structure union. Continues ...'
	#end composite action

# EXTERNAL body contour will be created using threshold-based segmentation
#with CompositeAction('Create External'):
#	patient.PatientModel.CreateRoi(Name='ABAS Ext', Color="Orange", Type="External", TissueName=None, RoiMaterial=None)
#	patient.PatientModel.RegionsOfInterest['ABAS Ext'].CreateExternalGeometry(Examination=examination, ThresholdLevel=-150)
#	# CompositeAction ends 

get_current("ActionVisibility:Internal") # needed due to that MBS actions not visible in evaluation version.
patient.PatientModel.MBSAutoInitializer(MbsRois=[
	{ 'CaseType': "Thorax", 'ModelName': "SpinalCord (Thorax)", 'RoiName': "Spinal Cord", 'RoiColor': "0,0,255" }],
	CreateNewRois=True, Examination=examination, UseAtlasBasedInitialization=True)
patient.PatientModel.AdaptMbsMeshes(Examination=examination, RoiNames=['Spinal Cord'], CustomStatistics=None, CustomSettings=None) 

#first pass autosegmentation using the default atlas for heart and lung
patient.PatientModel.CreateStructuresFromAtlas(SourceTemplateName="AbpDefaultData - HeartAndLung",
	SourceExaminationsNames=["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11", "P12", "P13", "P14", "P15", "P16"],
	SourceRoiNames=["Heart", "Lung (Right)", "Lung (Left)"], SourcePoiNames=[], AssociateStructuresByName=True, TargetExamination=examination)
patient.Save()

#second pass autosegmentation using the MedFys atlas for heart, lung and spinal cord
patient.PatientModel.CreateStructuresFromAtlas(SourceTemplateName="VsAtlas-CorPulmSpinalis",
	SourceExaminationsNames=["ThFemG1_5", "ThFemG1_6", "ThFemG1_8", "ThFemG2_0", "ThFemG2_4", "ThFemG2_6", "ThFemIG1_0", "ThFemIG1_2", "ThFemIG1_6", "ThFemIG2_0"],
	SourceRoiNames=["ABAS; Cor", "ABAS; Pulmo dxt", "ABAS; Pulmo sin","ABAS; Canalis spinalis"], SourcePoiNames=[], AssociateStructuresByName=True, TargetExamination=examination)

	 
# -- process autosegmentation volumes "Lung (Right)", "Lung (Left)"
with CompositeAction('ROI Algebra (Pulmones)'):
	try:
		r3 = patient.PatientModel.CreateRoi(Name='Pulmones (union)', Color="102,0,102", Type="Organ", TissueName=None, RoiMaterial=None)
		r3.SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['Lung (Right)'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['Lung (Left)'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		r3.UpdateDerivedGeometry(Examination=examination)
	except Exception:
		print 'Failed to create structure union. Continues ...'
	#end composite action


# -- process autosegmentation volumes "ABAS; Pulmo dxt", "ABAS; Pulmo sin"
with CompositeAction('ROI Algebra (ABAS; Pulmones)'):
	try:
		r4 = patient.PatientModel.CreateRoi(Name='ABAS; Pulmones', Color="204,255,153", Type="Organ", TissueName=None, RoiMaterial=None)
		r4.SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['ABAS; Pulmo dxt'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['ABAS; Pulmo sin'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		r4.UpdateDerivedGeometry(Examination=examination)
	except Exception:
		print 'Failed to create structure union. Continues ...'
	#end composite action

#save before forcing computation
patient.Save()

plan = patient.TreatmentPlans['abas'] #work on abas plan
# import clinical goals from a predefined template
plan.TreatmentCourse.EvaluationSetup.ApplyClinicalGoalTemplate(Template=db.TemplateTreatmentOptimizations['ck-sd-abas'])

beamset = patient.TreatmentPlans['abas'].BeamSets['abas'] #work on abas beamset

#force small dose grid
plan.SetDefaultDoseGrid(VoxelSize={'x':0.20, 'y':0.20, 'z':0.20})

#recompute
beamset.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="CCDose", ForceRecompute=False)


#save final result
patient.Save()



