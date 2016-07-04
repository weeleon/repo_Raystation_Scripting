import math
from connect import *
import time
import sys
clr.AddReference("PresentationFramework")
from System.Windows import *


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





#### PROSTATE TYPE C AUTO-PLAN
#### 78Gy/39F Normo-fractionated prescribed to PTV-T and PTV-SV
#### As a 7-field IMRT beam distribution

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

# Define null filter
filter = {}

# Get handle to patient db
db = get_current('PatientDB')

# Define patient and examination handles
patient = get_current('Patient')
examination = get_current('Examination')

# Define plan set and beam set and density dataset handles
planName = 'ProstC_78_39'
planName = UniquePlanName(planName, patient) #auto-generate a unique plan name if ProstC_78_39 already exists
beamSetImrtName = 'Primaer' #prepares a 7-field IMRT standard primary beamset
beamSetBoostName = 'Boost' #prepares a 7-field IMRT boost beamset
examinationName = examination.Name

# GROW PLANNING VOLUMES AND STANDARD MARGINS FOR PROSTATA TYPE C
CreateMarginPtvT() #all prostate types
CreateComplementBladderPtvT() #all prostate types
CreateComplementRectumPtvT() #all prostate types
CreateWallPtvT() #all prostate types
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


