import arcpy
import os
import argparse

def create_empty_gdb(gdb_path):
    arcpy.CreateFileGDB_management(os.path.dirname(gdb_path), os.path.basename(gdb_path))

def create_feature_dataset(gdb_path, feature_dataset_name):
    arcpy.env.workspace = gdb_path
    
    # Set the spatial reference to UTM Zone 10
    spatial_reference = arcpy.SpatialReference("Coordinate Systems/Projected Coordinate Systems/UTM/NAD 1983/NAD 1983 UTM Zone 10N.prj")
    
    arcpy.CreateFeatureDataset_management(gdb_path, feature_dataset_name, spatial_reference=spatial_reference)

def transfer_feature_class(input_gdb, output_gdb, output_feature_dataset, feature_class_name):
    arcpy.env.workspace = input_gdb
    feature_classes = arcpy.ListFeatureClasses(feature_class_name)
    
    # Print some information for troubleshooting
    print(f"Input GDB: {input_gdb}")
    print(f"Feature classes found: {feature_classes}")
    
    # Check if feature_classes is not None
    if feature_classes:
        for fc in feature_classes:
            # Assuming that 'output_feature_dataset' is a dataset under 'output_gdb'
            output_dataset_path = os.path.join(output_gdb, output_feature_dataset)
            
            # Print some more information for troubleshooting
            print(f"Output GDB: {output_gdb}")
            print(f"Output dataset path: {output_dataset_path}")
            
            # Check if the dataset exists, if not, create it
            if not arcpy.Exists(output_dataset_path):
                create_feature_dataset(output_gdb, output_feature_dataset)
            
            # Transfer feature class to the dataset
            arcpy.FeatureClassToFeatureClass_conversion(os.path.join(input_gdb, fc), output_dataset_path, fc)
    else:
        print(f"Error: No feature classes found in {input_gdb}")

def main():
    parser = argparse.ArgumentParser(description='Prepare data from file geodatabases.')
    parser.add_argument('in_gdbs_base_folder', help='Base folder containing file geodatabases.')
    parser.add_argument('out_gdb', help='Output geodatabase.')
    parser.add_argument('out_feature_dataset', help='Output feature dataset in the output geodatabase.')
    args = parser.parse_args()

    create_empty_gdb(args.out_gdb)

    # Loop through each .gdb folder and transfer feature classes
    for gdb_folder in os.listdir(args.in_gdbs_base_folder):
        gdb_path = os.path.join(args.in_gdbs_base_folder, gdb_folder)
        transfer_feature_class(gdb_path, args.out_gdb, args.out_feature_dataset, '*')  

if __name__ == "__main__":
    main()
