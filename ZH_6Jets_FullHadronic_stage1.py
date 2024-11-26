"""
January 2023
Abraham Tishelman-Charny

Parts adapted from George Iakovidis 
The purpose of this python module is to perform initial selections and variable definitions for processing FCC files.
"""

import os
import urllib.request
import yaml 
import sys
from examples.FCCee.weaver.config import collections
from CustomDefinitions import CustomDefinitions
sys.path.append("/afs/cern.ch/work/p/pusharma/public/FCC_studies/ZH_6Jets_FullHadronic/FCCAnalyses/")

import ROOT
ROOT.gInterpreter.Declare(CustomDefinitions)

# originally had YAML config here. Not strictly necessary. Check previous commits if you want an example.

batch = 1 # use HTCondor
EOSoutput = 1 # output to EOS
version_number=1
JobName = f"ZHadronic_6JetReco_v{version_number}" # job named used for output directory
njets = 6 # number of jets in exclusive reclustering
outputDir   = f"/eos/home-p/pusharma/FCC_analysis/outputs/{JobName}/stage1/"

#exclusive = 1 # to be implemented: type of reclustering to e.g. inclusive vs. exclusive

# originally was using the flag definitions below. Should follow the path of the `exclusive` flag to see what it actually means.
# these files may be relevant:
#addons/FastJet/python/jetClusteringHelper.py
#addons/FastJet/src/JetClustering.cc
  # flag for exclusive jet clustering. Possible choices are: 
  # 0 = inclusive clustering, for duram kt 
  # 1 = exclusive clustering that would be obtained when running the algorithm with the given dcut, 
  # 2 = exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 
  # 3 = exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets,
  # 4 = exclusive jets obtained at the given ycutei 

# example for running locally (will also happen by default if you specify an input file at the command line)
#batch = 0
#EOSoutput = 0
#JobName = "Inclusive_R0p4"
#njets = 4
#exclusive = 0 
#outputDir   = f"/usatlas/atlas01/atlasdisk/users/atishelma/{JobName}/stage1/"

print("batch:",batch)
print("EOSoutput:",EOSoutput)
print("name:",JobName)
print("njets:",njets)

processList = {
    # # Hadronic ZH
    #For CHECK
    # "wzp6_ee_bbH_Hbb_ecm240" : {'chunks' : 1},



     "wzp6_ee_bbH_Hbb_ecm240" : {'chunks' : 2},    
     "wzp6_ee_bbH_Hcc_ecm240" : {'chunks' : 2},
     "wzp6_ee_bbH_Hgg_ecm240" : {'chunks' : 2},
     "wzp6_ee_bbH_Hss_ecm240" : {'chunks' : 2},
     "wzp6_ee_bbH_Htautau_ecm240" : {'chunks' : 2},
     "wzp6_ee_bbH_HWW_ecm240" : {'chunks' : 2},
     "wzp6_ee_bbH_HZa_ecm240" : {'chunks' : 2},
     "wzp6_ee_bbH_HZZ_ecm240" : {'chunks' : 2},
     "wzp6_ee_ccH_Hbb_ecm240" : {'chunks' : 2},
     "wzp6_ee_ccH_Hcc_ecm240" : {'chunks' : 2},
     "wzp6_ee_ccH_Hgg_ecm240" : {'chunks' : 2},
     "wzp6_ee_ccH_Hss_ecm240" : {'chunks' : 2},
     "wzp6_ee_ccH_Htautau_ecm240" : {'chunks' : 2},
     "wzp6_ee_ccH_HWW_ecm240" : {'chunks' : 2},
     "wzp6_ee_ccH_HZa_ecm240" : {'chunks' : 2},
     "wzp6_ee_ccH_HZZ_ecm240" : {'chunks' : 2},
     "wzp6_ee_nunuH_ecm240" : {'chunks' : 2},
     "wzp6_ee_qqH_Hbb_ecm240" : {'chunks' : 2},
     "wzp6_ee_qqH_Hcc_ecm240" : {'chunks' : 2},
     "wzp6_ee_qqH_Hgg_ecm240" : {'chunks' : 2},
     "wzp6_ee_qqH_Hss_ecm240" : {'chunks' : 2},
     "wzp6_ee_qqH_Htautau_ecm240" : {'chunks' : 2},
     "wzp6_ee_qqH_HWW_ecm240" : {'chunks' : 2},
     "wzp6_ee_qqH_HZa_ecm240" : {'chunks' : 2},
     "wzp6_ee_qqH_HZZ_ecm240" : {'chunks' : 2},
     "wzp6_ee_ssH_Hbb_ecm240" : {'chunks' : 2},
     "wzp6_ee_ssH_Hcc_ecm240" : {'chunks' : 2},
     "wzp6_ee_ssH_Hgg_ecm240" : {'chunks' : 2},
     "wzp6_ee_ssH_Hss_ecm240" : {'chunks' : 2},
     "wzp6_ee_ssH_Htautau_ecm240" : {'chunks' : 2},
     "wzp6_ee_ssH_HWW_ecm240" : {'chunks' : 2},
     "wzp6_ee_ssH_HZa_ecm240" : {'chunks' : 2},
     "wzp6_ee_ssH_HZZ_ecm240" : {'chunks' : 2},   
     
     
     
     
     'p8_ee_WW_ecm240' : {'chunks':3740},
     'p8_ee_ZZ_ecm240' : {'chunks':562},
     'p8_ee_Zqq_ecm240' : {'chunks':1007}


    # backgrounds. Option: 'fraction' : frac_value
    #'p8_ee_WW_ecm240' : {'chunks':3740, 'fraction' : 0.0001},
    
#     'p8_ee_WW_ecm240' : {'chunks':1000},
#     'p8_ee_ZZ_ecm240' : {'chunks':250},
#     'p8_ee_Zqq_ecm240' : {'chunks':250}
    
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/" 
procDict = "FCCee_procDict_winter2023_IDEA.json" 

if(EOSoutput):
    # example output directory on EOS - note that by default this includes copying the output file from one location to another
    #outputDirEos = f"/eos/user/a/atishelm/ntuples/FCC/{JobName}/stage1/" # if you define outputDirEos, this process creates the file locally and copies it to eos.
    #outputDir = f"/eos/user/a/atishelm/ntuples/FCC/ZH_Hadronic_4JetReco/"
    outputDir   = f"/eos/user/p/pusharma/FCC_analysis/outputs/{JobName}/stage1/"
    eosType = "pusharma" # specify as necessary

runBatch    = batch
batchQueue = "nextweek" 

# Define any functionality which is not implemented in FCCAnalyses

import ROOT

# ____________________________________________________________
def get_file_path(url, filename):
    print("Looking for file:",filename)
    if os.path.exists(filename):
        print("File exists")
        return os.path.abspath(filename)
    else:
        urllib.request.urlretrieve(url, os.path.basename(url))
        return os.path.basename(url)

# ____________________________________________________________

## input file needed for unit test in CI
testFile = "https://fccsw.web.cern.ch/fccsw/testsamples/wzp6_ee_nunuH_Hss_ecm240.root"


url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"

model_name = "fccee_flavtagging_edm4hep_wc"

## model files needed for unit testing in CI
url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
url_preproc = "{}/{}.json".format(url_model_dir, model_name)
url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos

model_dir = "/afs/cern.ch/work/p/pusharma/public/FCC_studies/ZH_6Jets_FullHadronic/FCCAnalyses/"
local_preproc = "{}/{}.json".format(model_dir,model_name)
local_model = "{}/{}.onnx".format(model_dir,model_name)

weaver_preproc = local_preproc
weaver_model = local_model



from examples.FCCee.weaver.config import (
    variables_pfcand,
    variables_jet,
)
print('Current dir: ',os.getcwd())
from addons.ONNXRuntime.python.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.python.jetClusteringHelper import ExclusiveJetClusteringHelper

jetFlavourHelper = None
jetClusteringHelper = None

def analysis_sequence(df):
    collections["Electrons"] = "Electron"
    collections["Muons"] = "Muon"
    collections["Photons"] = "Photons"

    df = (
        # electrons
        df.Alias("Electron0", "{}#0.index".format(collections["Electrons"]))
        .Define(
            "electrons",
            "ReconstructedParticle::get(Electron0, {})".format(collections["PFParticles"]),
        )
        .Define("event_nel", "electrons.size()")
        .Define("electrons_p", "ReconstructedParticle::get_p(electrons)[0]")
        
        # muons
        .Alias("Muon0", "{}#0.index".format(collections["Muons"]))
        .Define(
            "muons",
            "ReconstructedParticle::get(Muon0, {})".format(collections["PFParticles"]),
        )
        .Define("event_nmu", "muons.size()")
        .Define("muons_p", "ReconstructedParticle::get_p(muons)[0]")
        #Get kinematics variables needed for selection later
        .Define("P4_vis", "ReconstructedParticle::get_P4vis({})".format(collections["PFParticles"]))
        .Define("vis_M", "P4_vis.M()")
        .Define("vis_E", "P4_vis.E()")
        .Define("P3_vis","TVector3(P4_vis.Px(), P4_vis.Py(), P4_vis.Pz())")
        .Define("vis_theta", "P3_vis.Theta()")

        #EVENTWIDE VARIABLES: Access quantities that exist only once per event, such as the missing energy (despite the name, the MissingET collection contains the total missing energy)
        .Define("RecoMissingEnergy_e", "ReconstructedParticle::get_e(MissingET)")
        .Define("RecoMissingEnergy_p", "ReconstructedParticle::get_p(MissingET)")
        .Define("RecoMissingEnergy_pt", "ReconstructedParticle::get_pt(MissingET)")
        .Define("RecoMissingEnergy_px", "ReconstructedParticle::get_px(MissingET)") #x-component of RecoMissingEnergy
        .Define("RecoMissingEnergy_py", "ReconstructedParticle::get_py(MissingET)") #y-component of RecoMissingEnergy
        .Define("RecoMissingEnergy_pz", "ReconstructedParticle::get_pz(MissingET)") #z-component of RecoMissingEnergy
        .Define("RecoMissingEnergy_eta", "ReconstructedParticle::get_eta(MissingET)")
        .Define("RecoMissingEnergy_theta", "ReconstructedParticle::get_theta(MissingET)")
        .Define("RecoMissingEnergy_phi", "ReconstructedParticle::get_phi(MissingET)") #angle of RecoMissingEnergy
    )
    for x in range(1, 9):
        df = (df.Define("d_{}{}".format(x,x+1), "JetClusteringUtils::get_exclusive_dmerge(_jet, {})".format(x))) #dmerge from x+1 to x

    return df


#def jet_sequence(df, njets, exclusive):
def jet_sequence(df, njets):

    global jetClusteringHelper
    global jetFlavourHelper

    tag = ""
    tagVar="Base"

    ## define jet clustering parameters
    # This is where you can try passing the "exclusive" parameter, and you will have to follow it to the ExclusiveJetClusteringHelper definition, which then goes to something else...
    #jetClusteringHelper = ExclusiveJetClusteringHelper(collections["PFParticles"], njets, exclusive, tag)
    jetClusteringHelper = ExclusiveJetClusteringHelper(collections["PFParticles"], njets, tag)

    ## run jet clustering
    df = jetClusteringHelper.define(df)

    ## define jet flavour tagging parameters
    jetFlavourHelper = JetFlavourHelper(
        collections,
        jetClusteringHelper.jets,
        jetClusteringHelper.constituents,
        tag
    )


    ## define observables for tagger
    df = jetFlavourHelper.define(df)
    df = df.Define("jet_p4", "JetConstituentsUtils::compute_tlv_jets({})".format(jetClusteringHelper.jets))
   
    # apply energy correction
    jet_reco_vars = ["e", "p", "px", "py", "pz", "m", "theta"]
    for jet_reco_var in jet_reco_vars:
        df=(df.Define("recojet_{}".format(jet_reco_var), "JetClusteringUtils::get_{}(jet)".format(jet_reco_var)))
    
    # phi has slightly different naming
    df=(df.Define("recojet_phi", "JetClusteringUtils::get_phi_std(jet)"))
 

    df = df.Define("jets_tlv_corr", "FCCAnalyses::energyReconstructFourJet(recojet_px, recojet_py, recojet_pz, recojet_e)")

    jet_corr_vars = ["e", "px", "py", "pz"]
    for jet_corr_var in jet_corr_vars: df = df.Define("jet_%s_corr"%(jet_corr_var), "FCCAnalyses::TLVHelpers::get_%s(jets_tlv_corr)"%(jet_corr_var))
    
    df = df.Define("all_invariant_masses", "JetConstituentsUtils::all_invariant_masses(jet_p4)")
    df = df.Define("recoil_masses", "all_recoil_masses(jet_p4)")
    
    # df = jetFlavourHelper.inference(baseline_noTOF_weaver_preproc,baseline_noTOF_weaver_model, df,tagVar="baseline_noTOF",Setup_weaverTrue=True)

    ## tagger inference\\    ## define variables using tagger inference outputs
    df = jetFlavourHelper.inference(weaver_preproc, weaver_model, df) 
   
 
    

    df = df.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(_jet)")
    df = df.Define("jets_truth", "FCCAnalyses::jetTruthFinder(jetconstituents, ReconstructedParticles, Particle)")
    # df = df.Define("jets_truthv2", "FCCAnalyses::jetTruthFinderV2(jet_p4, Particle)")
    return df

# Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis:
    # __________________________________________________________
    # Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df = jet_sequence(df, njets)        #df = jet_sequence(df, njets, exclusive) # again, was playing with exclusive parameter here. Don't remember if you need to pass it here.
        df = analysis_sequence(df)
        # Get list of column names
        column_names = df.GetColumnNames()
        return df

    # __________________________________________________________
    # Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = []

        # jets
        branches_jet = list(variables_jet.keys())
        branchList = branches_jet 
        branchList += jetFlavourHelper.outputBranches()
        branchList += ["event_njet"]
        
        # branchList += ["all_invariant_masses"]
        # branchList += ["recoil_masses"]

        branchList += ["jet_e_corr"]
        branchList += ["jet_px_corr"]
        branchList += ["jet_py_corr"]
        branchList += ["jet_pz_corr"]
        # not corrected pt, e
        # branchList += ["recojet_e"]
        # branchList += ["recojet_px"]
        # branchList += ["recojet_py"]
        # branchList += ["recojet_pz"]
        
        # truth info
        branchList += ["jets_truth"]
        # branchList += ["jets_truthv2"]
        
        # vis kinematics
        branchList += ["vis_theta"]
        branchList += ["vis_M"]
        branchList += ["vis_E"]

        for x in range(1, 9):
            branchList.append("d_{}{}".format(x,x+1))
        
        # leptons
        branchList += ["event_nel"]
        branchList += ["event_nmu"]
        branchList += ["muons_p"]
        branchList += ["electrons_p"]

        # MET
        MET_vars = ["e", "p", "pt", "px", "pt", "pz", "eta", "theta", "phi"]
        for MET_var in MET_vars:
            branchList += [f"RecoMissingEnergy_{MET_var}"]

        branchList = sorted(list(set(branchList))) # remove duplicates, sort
        return branchList
