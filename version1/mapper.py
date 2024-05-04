import pandas as pd
from polygons import PolygonCell
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class CellIDMapper():


    def __init__(self,mapped_from) -> None:

        print(f"Reading data from {mapped_from}")
        self.data = pd.read_excel(mapped_from)
        print(f"Reading data from {mapped_from} completed!")
        self.result = None
        self.cell_data_dict = {}


    def map_cell_ID_to_fov_and_save(self,fov_number,fov_data_file_name,file_name_to_be_saved):

        

        print(f"Reading file {fov_data_file_name}")
        df = pd.read_csv(fov_data_file_name)
        print(f"Reading file {fov_data_file_name} completed!")
        print()
        print(f"Extracting data which has fov equal to :  {fov_number}")
        fov_cell_data = self.extract_fov(fov_number)
        print(f"Extracting data which has fov equal to :  {fov_number} completed!")
        print()
        unique_cell_ids = self.data['cellID'].unique()
        print(f"Total Cell IDs found: {len(unique_cell_ids)}")
        print()
        # print(unique_cell_ids)
        grouped_data = {}

        #for each cell ID getting all the coordinates and creating PolygonCell object which is from the file Polygons.py
        for cell_id, group in fov_cell_data.groupby('cellID'):
            
            print(f"Creating PloygonCell Object for Cell ID : {cell_id}")
            coordinates = list(zip(group['x_local_px'], group['y_local_px']))
            # grouped_data[cell_id] = coordinates
            self.cell_data_dict[cell_id]=PolygonCell(cell_id,coordinates)
            print(f"Creating PloygonCell Object for Cell ID : {cell_id} Completed!")
            print()



        print(f"Mapping Cell ID to file {fov_data_file_name}")

        #using pandas apply function we apply _map_id function for each row
        df["cellID"] = df.apply(self._map_id,axis=1)
        print()
        #file is later saved
        df.to_csv(f"{file_name_to_be_saved}.csv")
        print(f"Mapping is done! file saved to {file_name_to_be_saved}.csv")
            
    #helper function to check a single point is inside a given cell ID's polygon or not
    def point_in_cell(self,point,cell_id):
        print(self.cell_data_dict[cell_id])
        return self.cell_data_dict[cell_id].in_polygon(point)
    
    #used in apply function where it takes dataframe row as input and for each cell_id's PolygonCell object we check in all cell ID polygons
    #whether the coordinates from the row lies inside the polygon or not.
    def _map_id(self,row):

        for cell_id,pCell in self.cell_data_dict.items():
            
            if pCell.in_polygon((row['x_local_px'],row['y_local_px'])):

                print(f"{row.name} index is assigned cell ID = {cell_id}")
                print()
                return cell_id
        return -1


    #helper function to extract and save records which are having fov equal to fovNumber 
    def extract_and_save_fov_to_excel(self,fovNumber,file_name_to_be_saved=""):

        if file_name=="":
            file_name = "fovData-{fovNumber}.xlsx"
        else:
            file_name+=".xlsx"


        df = self.extract_fov(fovNumber)

        df.to_excel(file_name_to_be_saved,index=False)
        print()

    #subhelper function of the above function which returns a data frame having given fovNumber
    def extract_fov(self,fovNumber):

        df = self.data[(self.data['fov']==fovNumber)]
        return df




#creating object of the class by providing the main file
C = CellIDMapper("Run5907_slide1-polygons.xlsx")

#running mapping function
C.map_cell_ID_to_fov_and_save(8,"slide1_F008_maskOnly.csv","mapped_result")

#checking for the same record values which are already mapped in the main file to check whether the polygon method is working properly or not
print(C.point_in_cell((211,4256),1))

print(C.point_in_cell((3,4147),1))

