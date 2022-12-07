import pandas as pd
output_file = "test.csv"

for i in range(1,9893):
    if i == 1:
        number_str = str(i)
        file_name = 'p'+number_str.zfill(6)+'.psv'
        print(file_name, end='\r') 
        patientID = i
        df = pd.read_csv(file_name,sep='|', index_col = False)
        df.insert(0, 'patient_sk', patientID)
        df.to_csv(output_file,na_rep='NA', index=False)
        
    else:
        number_str = str(i)
        file_name = 'p'+number_str.zfill(6)+'.psv'
        print(file_name, end='\r') 
        patientID = i
        df = pd.read_csv(file_name,sep='|', index_col=False)
        df.insert(0, 'patient_sk', patientID)
        df.to_csv(output_file, mode='a', header=False, na_rep='NA', index=False)

for i in range(12578,19312):
        number_str = str(i)
        file_name = 'p'+number_str.zfill(6)+'.psv'
        print(file_name, end='\r') 
        patientID = i
        df = pd.read_csv(file_name,sep='|', index_col=False)
        df.insert(0, 'patient_sk', patientID)
        df.to_csv(output_file, mode='a', header=False, na_rep='NA', index=False)

for i in range(19314,20001):
        number_str = str(i)
        file_name = 'p'+number_str.zfill(6)+'.psv'
        print(file_name, end='\r') 
        patientID = i
        df = pd.read_csv(file_name,sep='|', index_col=False)
        df.insert(0, 'patient_sk', patientID)
        df.to_csv(output_file, mode='a', header=False, na_rep='NA', index=False)

for i in range(20308,20644):
        number_str = str(i)
        file_name = 'p'+number_str.zfill(6)+'.psv'
        print(file_name, end='\r') 
        patientID = i
        df = pd.read_csv(file_name,sep='|', index_col=False)
        df.insert(0, 'patient_sk', patientID)
        df.to_csv(output_file, mode='a', header=False, na_rep='NA', index=False)

print("\n")