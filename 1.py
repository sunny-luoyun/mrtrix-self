
import os
# Sub = ['001','002','003','004','006','007','009','012','013','014','015','017','018','020','021','022','024','025','026','027','028','029','033','036','038','040','041','043']
Sub = ['043']
for i in Sub:
    '''process = os.popen(f'mkdir /data/Sham/S1/pre/Sub{i}')
    output = process.read()
    print(output)
    process.close()'''

    process = os.popen(f'dcm2niix -o /data/T1 -z y -f "%f"T1 /data/T1/Sub{i}')
    output = process.read()
    print(output)
    process.close()