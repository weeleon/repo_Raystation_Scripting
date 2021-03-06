library(reshape2)
library(ggplot2)
library(dplyr)
#this needs to be edited to set the folder that contains the files
setwd("/Users/lenw/Documents/Python_Programming/repo_Raystation_Scripting/ABAS_Studies")
list.files(pattern = "\\.csv$")

#read csv file of raw values
rawdata <- read.csv("ck-sd-genanalyser2.csv", header=T)
rawdataNew <- read.csv("ck-sd-genanalyser3.csv", header=T)

#parse the volume subset
volumes <- filter(rawdata, type=="vol")
volumesNew <- filter(rawdataNew,type == "vol")

volumesDistribution <- data.frame(
      patid = volumes$patid,
      organ = volumes$organ,
      ref = volumes$OR,
      ck = volumes$CK,
      sd = volumes$SD,
      rs = volumes$RS,
      mf = volumes$MF,
      mf2 = volumesNew$Mfnew,
      CKvsOR = volumes$CK - volumes$OR,
      SDvsOR = volumes$SD - volumes$OR,
      RSvsOR = volumes$RS - volumes$OR,
      MFvsOR = volumes$MF - volumes$OR,
      MF2vsOR = volumesNew$Mfnew - volumes$OR,
      Rel.CK = volumes$dCK / volumes$CK,
      Dice.CK = (2*volumes$dCK)/(volumes$OR + volumes$CK),
      Rel.SD = volumes$dSD / volumes$SD,
      Dice.SD = (2*volumes$dSD)/(volumes$OR + volumes$SD),
      Rel.RS = volumes$dRS / volumes$RS,
      Dice.RS = (2*volumes$dRS)/(volumes$OR + volumes$RS),
      Rel.MF = volumes$dMF / volumes$MF,
      Dice.MF = (2*volumes$dMF)/(volumes$OR + volumes$MF),
      Rel.MF2 = volumesNew$dMFnew / volumesNew$Mfnew,
      Dice.MF2 = (2*volumesNew$dMFnew)/(volumes$OR + volumesNew$Mfnew)
      )
mVolumesDistribution <- melt(volumesDistribution,id=c("patid","organ"))
names(mVolumesDistribution) <- c("patid","organ","Category","VolDiff")
mVolumesDistribution <- mVolumesDistribution[complete.cases(mVolumesDistribution),]

#parse the dosimetry subset
dose <- filter(rawdata, type!="vol")
doseNew <- filter(rawdataNew, type!="vol")
doseDistribution <- data.frame(
      patid = dose$patid,
      organ = dose$organ,
      type = dose$type,
      ref = dose$OR,
      ck = dose$CK,
      sd = dose$SD,
      rs = dose$RS,
      mf = dose$MF,
      mf2 = doseNew$Mfnew,
      CKvsOR = as.numeric(as.character(dose$CK))-as.numeric(as.character(dose$OR)),
      SDvsOR = as.numeric(as.character(dose$SD))-as.numeric(as.character(dose$OR)),
      RSvsOR = as.numeric(as.character(dose$RS))-as.numeric(as.character(dose$OR)),
      MFvsOR = as.numeric(as.character(dose$MF))-as.numeric(as.character(dose$OR)),
      MF2vsOR = as.numeric(as.character(doseNew$Mfnew))-as.numeric(as.character(doseNew$OR))
      )
mDoseDistribution <- melt(doseDistribution,id=c("patid","organ","type"))
names(mDoseDistribution) <- c("patid","organ","type","Category","DoseDiff")
mDoseDistribution <- mDoseDistribution[complete.cases(mDoseDistribution),]

#clean up
rm(dose,volumes,rawdata,doseNew,volumesNew,rawdataNew)
rm(doseDistribution,volumesDistribution)

#colour palette definition
paldef0 <- c("#E41A1C", "#377EB8", "#4DAF4A", "#984EA3")
paldef <- c("#E41A1C", "#377EB8", "black", "#4DAF4A", "#984EA3")
paldef2 <- c("#E41A1C", "#377EB8", "grey80", "#4DAF4A", "#984EA3")
paldef3 <- c("black", "#4DAF4A", "#984EA3")

ppi <- 600
# Calculate the height and width (in pixels) for a 4x4-inch image at 600 ppi
png("ABAS-Lung-in_Raystation-%d.png", width=6*ppi, height=4*ppi, res=ppi)

#absolute lung volume correlation plot
y <- filter(mVolumesDistribution, organ=="pulm" & Category %in% c("ck","sd","rs","mf","mf2"))
x <- filter(mVolumesDistribution, organ=="pulm" & Category %in% c("ref"))
all <- cbind(y,Baseline=x$VolDiff)

ggplot(all,aes(
             x=Baseline,
             y=VolDiff,
             shape=Category, colour=Category)) +
      geom_point(size=3) +
      scale_shape_manual(values=c(15,16,0,17,18)) +
      xlim(1900,5500) + ylim(1900,5500) +
      geom_abline(intercept = 0, slope = 1, linetype="dashed") +
      labs(x = "Reference Lung Volume (in cc)", y = "Drawn Lung Volume (in cc)") +
      theme_bw() +
      scale_colour_manual(values = paldef)

#summarise the median and distribution of the absolute volume differences
y <- filter(mVolumesDistribution, organ=="pulm" & Category %in% c("CKvsOR","SDvsOR","RSvsOR","MFvsOR","MF2vsOR"))
aggregate(y$VolDiff, by=list(y$Category), FUN=summary)

#summary information graphically
ggplot(filter(mVolumesDistribution, organ=="pulm" & Category %in% c("CKvsOR","SDvsOR","RSvsOR","MFvsOR","MF2vsOR") ),
       aes(x=Category, y=VolDiff)) +
      ylim(-200,800) +
      geom_boxplot(aes(fill=Category)) +
      theme_bw() +
      labs(x = "Contouring comparison", y = "Lung volume difference (in ccm)") +
      scale_fill_manual(values = paldef2, guide=FALSE)

#correlations in lung doses differences
y <- filter(mDoseDistribution, type=="v20" & organ=="pulm" & Category %in% c("CKvsOR","SDvsOR","RSvsOR","MFvsOR","MF2vsOR"))
x <- filter(mDoseDistribution, type=="avdose" & organ=="pulm" & Category %in% c("CKvsOR","SDvsOR","RSvsOR","MFvsOR","MF2vsOR"))
all <- cbind(y,MLD=x$DoseDiff)

ggplot(all,aes(
      y=MLD,
      x=100*DoseDiff,
      shape=Category, colour=Category)) +
      geom_point(size=3) +
      scale_shape_manual(values=c(15,16,0,17,18)) +
      geom_abline(intercept = 0, slope = 0.5, linetype="dashed") +
      labs(y = "Change in MLD (Gy)", x = "Change in Lung V20Gy (pct difference)") +
      theme_bw() +
      scale_colour_manual(values = paldef)

#summarise the median and distribution of the V20 volume differences
y <- filter(mDoseDistribution, organ=="pulm" & type=="v20" & Category %in% c("CKvsOR","SDvsOR","RSvsOR","MFvsOR","MF2vsOR"))
aggregate(100*y$DoseDiff, by=list(y$Category), FUN=summary)

#summarise the median and distribution of the mean lung dose differences
y <- filter(mDoseDistribution, organ=="pulm" & type=="avdose" & Category %in% c("CKvsOR","SDvsOR","RSvsOR","MFvsOR","MF2vsOR"))
aggregate(y$DoseDiff, by=list(y$Category), FUN=summary)

#dice similarity comparison
ggplot(filter(mVolumesDistribution, organ=="pulm" & Category %in% c("Dice.CK","Dice.SD","Dice.RS","Dice.MF","Dice.MF2") ),
       aes(x=Category, y=VolDiff)) +
      geom_boxplot(aes(fill=Category)) +
      theme_bw() +
      labs(x = "Contouring comparison", y = "Dice Similarity in Lung (a.u.)") +
      scale_fill_manual(values = paldef2, guide=FALSE)
y <- filter(mVolumesDistribution, organ=="pulm" & Category %in% c("Dice.CK","Dice.SD","Dice.RS","Dice.MF","Dice.MF2"))
aggregate(y$VolDiff, by=list(y$Category), FUN=summary)

dev.off()


ppi <- 600
# Calculate the height and width (in pixels) for a 4x4-inch image at 600 ppi
png("ABAS-Heart-in_Raystation-%d.png", width=6*ppi, height=4*ppi, res=ppi)

#absolute heart volume correlation plot
y <- filter(mVolumesDistribution, organ=="cor" & Category %in% c("ck","sd","rs","mf","mf2"))
x <- filter(mVolumesDistribution, organ=="cor" & Category %in% c("ref"))
all <- cbind(y,Baseline=x$VolDiff)

ggplot(all,aes(
      x=Baseline,
      y=VolDiff,
      shape=Category, colour=Category)) +
      geom_point(size=3) +
      xlim(400,1600) + ylim(400,1600) +
      scale_shape_manual(values=c(15,16,0,17,18)) +
      geom_abline(intercept = 0, slope = 1, linetype="dashed") +
      labs(x = "Reference Heart Volume (in cc)", y = "Drawn Heart Volume (in cc)") +
      theme_bw() +
      scale_colour_manual(values = paldef)

#summarise the median and distribution of the absolute volume differences
y <- filter(mVolumesDistribution, organ=="cor" & Category %in% c("CKvsOR","SDvsOR","RSvsOR","MFvsOR","MF2vsOR"))
aggregate(y$VolDiff, by=list(y$Category), FUN=summary)

#summary information graphically
ggplot(filter(mVolumesDistribution, organ=="cor" & Category %in% c("CKvsOR","SDvsOR","RSvsOR","MFvsOR","MF2vsOR") ),
       aes(x=Category, y=VolDiff)) +
      ylim(-300,200) +
      geom_boxplot(aes(fill=Category)) +
      theme_bw() +
      labs(x = "Contouring comparison", y = "Heart volume difference (in ccm)") +
      scale_fill_manual(values = paldef2, guide=FALSE)

#correlations in heart doses differences
y <- filter(mDoseDistribution, type=="v50" & organ=="cor" & Category %in% c("CKvsOR","SDvsOR","RSvsOR","MFvsOR","MF2vsOR"))
x <- filter(mDoseDistribution, type=="avdose" & organ=="cor" & Category %in% c("CKvsOR","SDvsOR","RSvsOR","MFvsOR","MF2vsOR"))
all <- cbind(y,MHD=x$DoseDiff)

ggplot(all,aes(
      y=MHD,
      x=100*DoseDiff,
      shape=Category, colour=Category)) +
      geom_point(size=3) +
      scale_shape_manual(values=c(15,16,0,17,18)) +
      geom_abline(intercept = 0, slope = 0.8, linetype="dashed") +
      labs(y = "Change in MHD (Gy)", x = "Change in Heart V50Gy (pct difference)") +
      theme_bw() +
      scale_colour_manual(values = paldef)

#summarise the median and distribution of the V50 volume differences
y <- filter(mDoseDistribution, organ=="cor" & type=="v50" & Category %in% c("CKvsOR","SDvsOR","RSvsOR","MFvsOR","MF2vsOR"))
aggregate(100*y$DoseDiff, by=list(y$Category), FUN=summary)

#summarise the median and distribution of the mean heart dose differences
y <- filter(mDoseDistribution, organ=="cor" & type=="avdose" & Category %in% c("CKvsOR","SDvsOR","RSvsOR","MFvsOR","MF2vsOR"))
aggregate(y$DoseDiff, by=list(y$Category), FUN=summary)

#dice similarity comparison
ggplot(filter(mVolumesDistribution, organ=="cor" & Category %in% c("Dice.CK","Dice.SD","Dice.RS","Dice.MF","Dice.MF2") ),
       aes(x=Category, y=VolDiff)) +
      geom_boxplot(aes(fill=Category)) +
      theme_bw() +
      labs(x = "Contouring comparison", y = "Dice Similarity in Heart (a.u.)") +
      scale_fill_manual(values = paldef2, guide=FALSE)
y <- filter(mVolumesDistribution, organ=="cor" & Category %in% c("Dice.CK","Dice.SD","Dice.RS","Dice.MF","Dice.MF2"))
aggregate(y$VolDiff, by=list(y$Category), FUN=summary)

dev.off()


ppi <- 600
# Calculate the height and width (in pixels) for a 4x4-inch image at 600 ppi
png("ABAS-SpinalCord-in_Raystation-%d.png", width=6*ppi, height=4*ppi, res=ppi)

#absolute spinal cord volume correlation plot
#
#note that here - it is not the volume agreement that matters but
#rather the dice similarity and overlap volume
#
#summarise the median and distribution of the absolute volume differences
y <- filter(mVolumesDistribution, organ=="canalis" & Category %in% c("RSvsOR","MFvsOR","MF2vsOR"))
aggregate(y$VolDiff, by=list(y$Category), FUN=summary)

#summary information graphically
ggplot(filter(mVolumesDistribution, organ=="canalis" & Category %in% c("RSvsOR","MFvsOR","MF2vsOR") ),
       aes(x=Category, y=VolDiff)) +
      ylim(-50,50) +
      geom_boxplot(aes(fill=Category)) +
      theme_bw() +
      labs(x = "Contouring comparison", y = "Spinal cord volume difference (in ccm)") +
      scale_fill_manual(values = c("grey80", "#4DAF4A", "#984EA3"), guide=FALSE)


#similarity and overlap
y <- filter(mVolumesDistribution, organ=="canalis" & Category %in% c("Rel.CK","Rel.SD","Rel.RS","Rel.MF","Rel.MF2"))
x <- filter(mVolumesDistribution, organ=="canalis" & Category %in% c("Dice.CK","Dice.SD","Dice.RS","Dice.MF","Dice.MF2"))
all <- cbind(y,Dice=x$VolDiff)

ggplot(all,aes(
      y=VolDiff,
      x=Dice,
      shape=Category, colour=Category)) +
      geom_point(size=3) +
      scale_shape_manual(values=c(0,17,18)) +
      xlim(0.5,1) + ylim(0.5,1) +
      geom_abline(intercept = 0, slope = 1, linetype="dashed") +
      labs(y = "Volume overlap fraction", x = "Dice Similarity in spinal cord") +
      theme_bw() +
      scale_colour_manual(values = c("black", "#4DAF4A", "#984EA3"))

#summarise the median and distribution of the high dose differences (d1cc)
y <- filter(mDoseDistribution, organ=="canalis" & type=="d1cc" & Category %in% c("CKvsOR","SDvsOR","RSvsOR","MFvsOR","MF2vsOR"))
aggregate(y$DoseDiff, by=list(y$Category), FUN=summary)

#summary information graphically
ggplot(filter(mDoseDistribution, organ=="canalis" & Category %in% c("RSvsOR","MFvsOR","MF2vsOR") ),
       aes(x=Category, y=DoseDiff)) +
      ylim(-5,12) +
      geom_boxplot(aes(fill=Category)) +
      theme_bw() +
      labs(x = "Contouring comparison", y = "Change in D1cc High Dose (Gy)") +
      scale_fill_manual(values = c("grey80", "#4DAF4A", "#984EA3"), guide=FALSE)


dev.off()






#paired non-parametric test (Wilcoxon)

#are volumes of lung different?
temp <- filter(rawdata, type=="vol" & organ=="pulm")[4:8]
OR <- as.numeric(as.character(temp$OR))
CK <- as.numeric(as.character(temp$CK))
SD <- as.numeric(as.character(temp$SD))
RS <- as.numeric(as.character(temp$RS))
MF <- as.numeric(as.character(temp$MF))

wilcox.test(CK, OR, paired=TRUE, conf.int=TRUE)
#pseudomedian = -12 ccm, CI = -54.6 to 36.5, p = 0.53

wilcox.test(SD, OR, paired=TRUE, conf.int=TRUE)
#pseudomedian = 27 ccm, CI = -32 to 83, p = 0.35

wilcox.test(RS, OR, paired=TRUE, conf.int=TRUE)
# *** pseudomedian = 318 ccm, CI = 221 to 418, p < 0.01

wilcox.test(MF, OR, paired=TRUE, conf.int=TRUE)
#pseudomedian = -23 ccm, CI = -78 to 41, p = 0.53

#are V20 levels in lung different?
temp <- filter(rawdata, type=="v20" & organ=="pulm")[4:8]
OR <- as.numeric(as.character(temp$OR))
CK <- as.numeric(as.character(temp$CK))
SD <- as.numeric(as.character(temp$SD))
RS <- as.numeric(as.character(temp$RS))
MF <- as.numeric(as.character(temp$MF))

wilcox.test(CK, OR, paired=TRUE, conf.int=TRUE)
#pseudomedian = 0.12%, CI = 0 to 0.42, p = 0.2

wilcox.test(SD, OR, paired=TRUE, conf.int=TRUE)
# ** pseudomedian = 0.29%, CI = 0 to 0.60, p < 0.05

wilcox.test(RS, OR, paired=TRUE, conf.int=TRUE)
#pseudomedian = 0.24%, CI = 0 to 0.67, p = 0.16

wilcox.test(MF, OR, paired=TRUE, conf.int=TRUE)
#pseudomedian = 0.11%, CI = -0.19 to 0.39%, p = 0.42

#are MLD levels in lung different?
temp <- filter(rawdata, type=="avdose" & organ=="pulm")[4:8]
OR <- as.numeric(as.character(temp$OR))
CK <- as.numeric(as.character(temp$CK))
SD <- as.numeric(as.character(temp$SD))
RS <- as.numeric(as.character(temp$RS))
MF <- as.numeric(as.character(temp$MF))

wilcox.test(CK, OR, paired=TRUE, conf.int=TRUE)
#pseudomedian = 8.4 cGy, CI = -2 to 20, p = 0.11

wilcox.test(SD, OR, paired=TRUE, conf.int=TRUE)
# ** pseudomedian = 17 cGy, CI = 2.5 to 30, p < 0.05

wilcox.test(RS, OR, paired=TRUE, conf.int=TRUE)
#pseudomedian = 16 cGy, CI = -1 to 36, p = 0.09

wilcox.test(MF, OR, paired=TRUE, conf.int=TRUE)
#pseudomedian = 6.3 cGy, CI = -8.5 to 18, p = 0.34


#are volumes of heart different?
temp <- filter(rawdata, type=="vol" & organ=="cor")[4:8]
OR <- as.numeric(as.character(temp$OR))
CK <- as.numeric(as.character(temp$CK))
SD <- as.numeric(as.character(temp$SD))
RS <- as.numeric(as.character(temp$RS))
MF <- as.numeric(as.character(temp$MF))

wilcox.test(CK, OR, paired=TRUE, conf.int=TRUE)
#pseudomedian = -3.4 ccm, CI = -23 to 13, p = 0.78

wilcox.test(SD, OR, paired=TRUE, conf.int=TRUE)
#pseudomedian = -10 ccm, CI = -37 to 4, p = 0.13

wilcox.test(RS, OR, paired=TRUE, conf.int=TRUE)
# ** pseudomedian = 60 ccm, CI = 4.5 to 95, p < 0.05

wilcox.test(MF, OR, paired=TRUE, conf.int=TRUE)
#pseudomedian = 0.9 ccm, CI = -45 to 47, p = 0.98

#are V50 levels in heart different?
temp <- filter(rawdata, type=="v50" & organ=="cor")[4:8]
OR <- as.numeric(as.character(temp$OR))
CK <- as.numeric(as.character(temp$CK))
SD <- as.numeric(as.character(temp$SD))
RS <- as.numeric(as.character(temp$RS))
MF <- as.numeric(as.character(temp$MF))

wilcox.test(CK, OR, paired=TRUE, conf.int=TRUE)

wilcox.test(SD, OR, paired=TRUE, conf.int=TRUE)

wilcox.test(RS, OR, paired=TRUE, conf.int=TRUE)

wilcox.test(MF, OR, paired=TRUE, conf.int=TRUE)

#are MHD levels in heart different?
temp <- filter(rawdata, type=="avdose" & organ=="cor")[4:8]
OR <- as.numeric(as.character(temp$OR))
CK <- as.numeric(as.character(temp$CK))
SD <- as.numeric(as.character(temp$SD))
RS <- as.numeric(as.character(temp$RS))
MF <- as.numeric(as.character(temp$MF))

wilcox.test(CK, OR, paired=TRUE, conf.int=TRUE)

wilcox.test(SD, OR, paired=TRUE, conf.int=TRUE)

wilcox.test(RS, OR, paired=TRUE, conf.int=TRUE)

wilcox.test(MF, OR, paired=TRUE, conf.int=TRUE)


#are volumes of spinal cord different?
temp <- filter(rawdata, type=="vol" & organ=="canalis")[4:8]
OR <- as.numeric(as.character(temp$OR))
RS <- as.numeric(as.character(temp$RS))
MF <- as.numeric(as.character(temp$MF))

wilcox.test(RS, OR, paired=TRUE, conf.int=TRUE)

wilcox.test(MF, OR, paired=TRUE, conf.int=TRUE)

#are hot spots on spinal cord different?
temp <- filter(rawdata, type=="d1cc" & organ=="canalis")[4:8]
OR <- as.numeric(as.character(temp$OR))
RS <- as.numeric(as.character(temp$RS))
MF <- as.numeric(as.character(temp$MF))

wilcox.test(RS, OR, paired=TRUE, conf.int=TRUE)

wilcox.test(MF, OR, paired=TRUE, conf.int=TRUE)
