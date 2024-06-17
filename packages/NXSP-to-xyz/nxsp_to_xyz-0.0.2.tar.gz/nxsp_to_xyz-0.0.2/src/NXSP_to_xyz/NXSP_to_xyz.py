from ase import units
import pandas as pd
def NX_to_xyz(filename):
    # import glob
    # import shutil
    # import os
    # from pathlib import Path
    # import platform
    # import numpy as np
    
    #df = pd.read_csv('initial_condition',engine='python',header=None)
    df = pd.read_csv(filename ,engine='python',header=None)
    df.columns = ['Output']
    
    
    Geometry_index = df[df['Output'].str.contains('Geometry', na=False)].index[1:]
    Velocity_index = df[df['Output'].str.contains('Velocity', na=False)].index[1:]
    atom_num = Velocity_index[0] - Geometry_index[0] - 1 
    
    xyz_title = pd.DataFrame([str(atom_num) , 'title'])
    xyz_title.columns = ['Output']
    
    
    xyz_list = []
    for j in range(0,len(Geometry_index)):
        Geometry_part = df[Geometry_index[j]+1 : Velocity_index[j] ]
        Geometry_part = Geometry_part['Output'].str.split(pat=r'\s+', expand=True)
        Geometry_part.drop(columns=Geometry_part.columns[[0,2,6]], inplace=True, errors='ignore')
        Geometry_part.columns = ['Atom','X','Y','Z']
        Geometry_part = Geometry_part.apply(pd.to_numeric, errors = 'ignore')    
        Geometry_part[['X','Y','Z']] = Geometry_part[['X','Y','Z']] * units.Bohr
        
        
        Geometry_part['Output'] = Geometry_part.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
        Geometry_part = pd.DataFrame(Geometry_part['Output'])
    
        Output_Geodf = pd.concat([xyz_title, Geometry_part] ).reset_index(drop=True)
        xyz_list.append(Output_Geodf)  
       
    
    df_xyz = pd.concat(xyz_list).reset_index(drop=True)
    df_xyz.to_csv('traj.xyz', index = False ,header = None)
    
    
    
# if __name__ == "__main__":
#     main()