
import sys
from optparse import OptionParser

try:
    import cPickle as pickle
except:
    import pickle

import numpy as np
import random
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
#pd.options.mode.chained_assignment = None 
#import timeit


### Random split to train ,test and validation sets
def split_fn(pts_ls,pts_sls,outFile):
   print ("Splitting")
   dataSize = len(pts_ls)
   np.random.seed(0)
   ind = np.random.permutation(dataSize)
   nTest = int(0.2 * dataSize)
   nValid = int(0.1 * dataSize)
   test_indices = ind[:nTest]
   valid_indices = ind[nTest:nTest+nValid]
   train_indices = ind[nTest+nValid:]

   for subset in ['train','valid','test']:
       if subset =='train':
            indices = train_indices
       elif subset =='valid':
            indices = valid_indices
       elif subset =='test':
            indices = test_indices
       else: 
            print ('error')
            break
       subset_ptencs = [pts_ls[i] for i in indices]
       subset_ptencs_s =[pts_sls[i] for i in indices]
       ptencsfile = outFile +'.ptencs.'+subset
       bertencsfile = outFile +'.bencs.'+subset
       pickle.dump(subset_ptencs, open(ptencsfile, 'a+b'), -1)
       pickle.dump(subset_ptencs_s, open(bertencsfile, 'a+b'), -1)
       
### Main Function
if __name__ == '__main__':
    
   #targetFile= sys.argv[1]
  diagFile= sys.argv[1]
  typeFile= sys.argv[2]
  outFile = sys.argv[3]
  p_samplesize = int(sys.argv[4]) ### replace with argparse later

  parser = OptionParser()
  (options, args) = parser.parse_args()
 
   
  #_start = timeit.timeit()
   
  debug=False
  #np.random.seed(1)

  #### Data Loading¨
  print (" data file" )
  data_diag= pd.read_csv(diagFile, sep=',')   
  data_diag.columns=['patient_sk','HR','O2Sat','Temp','SBP','MAP','DBP','Resp','EtCO2','BaseExcess','HCO3','FiO2','pH','PaCO2','SaO2','AST','BUN','Alkalinephos','Calcium','Chloride','Creatinine','Bilirubin_direct','Glucose','Lactate','Magnesium','Phosphate','Potassium','Bilirubin_total','TroponinI','Hct','Hgb','PTT','WBC','Fibrinogen','Platelets','Age','Gender','Unit1','Unit2','HospAdmTime','ICULOS','SepsisLabel']
  
  if typeFile=='NA': 
       types={'empty_pad':0}
  else:
      with open(typeFile, 'rb') as t2:
             types=pickle.load(t2)
             
          

  #### Sampling
   
  if p_samplesize>0:
    print ('Sampling')
    ptsk_list=data_diag['patient_sk'].drop_duplicates()
    pt_list_samp=ptsk_list.sample(n=p_samplesize)
    n_data= data_diag[data_diag['patient_sk'].isin(pt_list_samp.values.tolist())]  
  else:
    n_data=data_diag
    
  #n_data.admit_dt_tm.fillna(n_data.discharge_dt_tm, inplace=True) ##, checked the data and no need for that line


  ##### Data pre-processing
  print ('Start Data Preprocessing !!!')
  count=0
  pts_ls=[]
  pts_sls=[]

  for Pt, group in n_data.groupby('patient_sk'):

      pt_encs=[]
      time_tonext=[]
      pt_los=[]
      full_seq=[]
      v_seg=[]
      pt_discdt=[]
      pt_addt=[]
      pt_ls=[]
      v=0
      for Time, subgroup in group.sort_values(['ICULOS'], ascending=True).groupby('ICULOS', sort=False): ### changing the sort order
          v=v+1
          diag_l=np.array(subgroup['SepsisLabel'].drop_duplicates()).tolist()
          if len(diag_l)> 0:
              diag_lm=[]
              for code in diag_l: 
                if code in types:
                    diag_lm.append(types[code])
                else: 
                    types[code] = max(types.values())+1
                    diag_lm.append(types[code])
                v_seg.append(v)
              full_seq.extend(diag_lm)
          pt_discdt.append(Time)
          pt_discdt.append(str(Time))
          pt_addt.append(min(np.array(subgroup['ICULOS'].drop_duplicates()).tolist()))
  
      if len(pt_encs)>0:
          pt_ls.append(pt_encs)
  
      pts_ls.append(pt_ls)
      pts_sls.append([Pt,pt_los,time_tonext,full_seq,v_seg])
  
     
      count=count+1

      if count % 1000 == 0: print ('processed %d pts' % count)
      
      if count % 100000 == 0:
          print ('dumping %d pts' % count)
          split_fn(pts_ls,pts_sls,outFile)
          pts_ls=[]
          pts_sls=[]
              
           
   
  split_fn(pts_ls,pts_sls,outFile)   
  pickle.dump(types, open(outFile+'.types', 'wb'), -1)