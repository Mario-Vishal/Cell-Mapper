import pandas as pd
import numpy as np



class Mapper():


    def __init__(self,mapped_from) -> None:

        print(f"Reading data from {mapped_from}")
        self.data = pd.read_excel(mapped_from)
        print(f"Reading data from {mapped_from} completed!")
        self.result = None
        self.cell_data_dict = {}
        self.data_points = []
        self.input_points = list(zip(self.data['x_local_px'],self.data["y_local_px"]))
        
        print("input_points",self.input_points[:10])

    def map_cell_ID_to_fov_and_save(self,fov_number,fov_data_file_name):

        print(f"Reading file {fov_data_file_name}")
        df = pd.read_csv(fov_data_file_name)
        print(f"Reading file {fov_data_file_name} completed!")
        print()
        print(f"Extracting data which has fov equal to :  {fov_number}")
        fov_cell_data = self.extract_fov(fov_number)
        print(f"Extracting data which has fov equal to :  {fov_number} completed!")
        print()
        print("Creating cell id dictionary")

        #for each row in data frame create dictionary which has key as coordinate and value as key ID
        #get all the coordinates from the dataframe and store it in self.data_points
        for index,row in fov_cell_data.iterrows():

            self.cell_data_dict[(row['x_local_px'],row['y_local_px'])]=row["cellID"]
            self.data_points.append((row['x_local_px'],row['y_local_px']))

        print("data points",self.data_points[:10])
        
        print("(COMPLETED) Creating cell id dictionary")
        print()


        #applying using lambda function for every row in the data frame
        df["cellID"] = self.data.apply(lambda row : self.find_closest_point_vectorized([(row['x_local_px'],row['y_local_px'])],self.data_points,row.name),axis=1)

        df.to_csv(f"Final_Fov{fov_number}_mapped_data.csv")
    
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
        #extracting records which hav fov == fovNumber

        df = self.data[(self.data['fov']==fovNumber)]
        return df

    #this function returns the cell ID of the point which is the closest to the input point
    def find_closest_point_vectorized(self,input_points, data_points,row_index):
        input_array = np.array(input_points)
        data_array = np.array(data_points)

        # Calculating distances using vectorized operations
        distances = np.sqrt(np.sum((data_array - input_array[:, np.newaxis])**2, axis=2))

        # Finding the index of the closest point for each input point
        closest_indices = np.argmin(distances, axis=1)

        # Get the corresponding closest points
        closest_points = data_array[closest_indices]
        print(closest_points)
        point = (int(closest_points[0][0]),int(closest_points[0][1]))
        cell_id= self.cell_data_dict[point]
        print(f"{row_index} index is assigned cell ID = {cell_id}")

        return cell_id


    
df = Mapper("Run5907_slide1-polygons.xlsx")

df.map_cell_ID_to_fov_and_save(8,"slide1_F008_maskOnly.csv")