import uproot
import ROOT
import numpy as np
import awkward as ak 


colors=[ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kCyan,ROOT.kMagenta]
flavs = ["cc","bb"]
captions = ["0.65 anti-kt with durham E-Corr","durham-kt-corr"]
alg=0

algs = [0,1,1,1,1]
files = ["04nocorr.root","04corr30000.root", "06corr.root","065corr.root", "07corr.root","chunk_1.root"]

key = "antidcorr065"

#set starting event
event_start = 0
#set number of events
nevents = 10000
#set number of bins
bins = 35
## 0--anti-kt 1--Durham


def get_masses(px,py,pz,e):
    p_mass=[]
    for i in range(len(px)):
        vecs=[]

        vecs.append(ROOT.TLorentzVector())
        vecs.append(ROOT.TLorentzVector())

        vecs[0].SetPxPyPzE(px[i][0],py[i][0], pz[i][0], e[i][0])
        vecs[1].SetPxPyPzE(px[i][1],py[i][1], pz[i][1], e[i][1])

        sum = ROOT.TLorentzVector()
        #compute tlv sum
        sum = vecs[0] + vecs[1]
    
        #get invariant mass of the sum 
        mass=sum.M()

        p_mass.append(mass)
        if i % 10000 == 0:
         print(i)
        
    return p_mass

def main(file):
    p_masses=[]
    file = uproot.open(files[0])
    tree = file['events']
    #array of the branches
    print("i read it hehe")
    branches = tree.arrays()

    event_njet = branches["event_njet"]
    #print(event_njet[:10])
    #array with events only with 4 jets

    if any(event_njet)>4:
        print("something is wrong")

    jets_mask = event_njet==4

    #create arrays for momentum and energy

    #np.array makes an array of the True/False values

    mask = np.array(ak.count_nonzero(np.abs(branches["jets_truth"][jets_mask])==4, axis=1)==2)
    mask &= np.array(ak.count_nonzero(np.abs(branches["jets_truth"][jets_mask])==5, axis=1)==2)

    mask_c = np.abs(branches["jets_truth"][jets_mask][mask])==4
    mask_b = np.abs(branches["jets_truth"][jets_mask][mask])==5

    
    jet_px_c=(branches["jet_px_corr"][jets_mask][mask][mask_c])
    jet_py_c=(branches["jet_py_corr"][jets_mask][mask][mask_c])
    jet_pz_c=(branches["jet_pz_corr"][jets_mask][mask][mask_c])
    jet_e_c=(branches["jet_e_corr"][jets_mask][mask][mask_c])
   
    c_masses = get_masses(jet_px_c,jet_py_c,jet_pz_c,jet_e_c)

    jet_px_b=(branches["jet_px_corr"][jets_mask][mask][mask_b])
    jet_py_b=(branches["jet_py_corr"][jets_mask][mask][mask_b])
    jet_pz_b=(branches["jet_pz_corr"][jets_mask][mask][mask_b])
    jet_e_b=(branches["jet_e_corr"][jets_mask][mask][mask_b])
   
    b_masses = get_masses(jet_px_b,jet_py_b,jet_pz_b,jet_e_b)

    # jet_px_c=(branches["recojet_px"][jets_mask][mask][mask_c])
    # jet_py_c=(branches["recojet_py"][jets_mask][mask][mask_c])
    # jet_pz_c=(branches["recojet_pz"][jets_mask][mask][mask_c])
    # jet_e_c=(branches["recojet_e"][jets_mask][mask][mask_c])

    # jet_px_b=(branches["recojet_px"][jets_mask][mask][mask_b])
    # jet_py_b=(branches["recojet_py"][jets_mask][mask][mask_b])
    # jet_pz_b=(branches["recojet_pz"][jets_mask][mask][mask_b])
    # jet_e_b=(branches["recojet_e"][jets_mask][mask][mask_b])


    p_masses.append(c_masses)
    p_masses.append(b_masses)

    
#first make all hists for the 
def make_hist(masses,av):
    maximum = 200
    minimum = 0
    hist = ROOT.TH1F("hist", "jet pair masses", bins, minimum, maximum)
    for m in masses: 
        hist.Fill(m)



def create_plot(p_mass, flav):

    maximum = 200
    minimum = 0

    # hists = []
    hist = ROOT.TH1F("hist","jet pair masses", bins, minimum, maximum)


    for pp in p_mass:
        # print(pp)
        # print(i)
        hist.Fill(pp)
        
    hist.Scale(1.0 / hist.Integral())
    # hists.append(hist)
       
    canvas = ROOT.TCanvas("canvas", flavs[flav]+" jet pair masses", 800, 600)
    legend = ROOT.TLegend(0, 0.85, 0.3, 1.05)
    
    # for i, hist in enumerate(hists):
    color = colors[alg]
    hist.SetLineColor(color)
    hist.SetMaximum(hist.GetMaximum() * 1.1) 
    hist.Sumw2(ROOT.kFALSE)
    hist.Draw("HIST")

    # if i==0:
    #     hist.Draw("HIST")
    # else:
    #     hist.Draw("SAME")
    
    mean = str(hist.GetMean())
    legend.AddEntry(hist, captions[alg]+mean, "l")
    legend.SetBorderSize(0)
    legend.Draw()
    canvas.SaveAs("../hists/"+key+flavs[flav]+"mass.pdf")



#print(len(p_masses))

for file in files: 

    main(files[alg])

    for i, p_mass in enumerate(p_masses):
        create_hist(p_mass, i)
        
    







