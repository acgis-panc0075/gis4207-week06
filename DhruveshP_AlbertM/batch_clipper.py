import arcpy
import os
import sys

def batch_clipper(in_workspace, clip_workspace, out_workspace):
    arcpy.env.overwriteOutput = True

    if not arcpy.Exists(in_workspace) or not arcpy.Exists(clip_workspace) or not arcpy.Exists(out_workspace):
        print("One or more workspaces do not exist. Please check your paths.")
        sys.exit(1)

    arcpy.env.workspace = in_workspace
    in_feature_classes = arcpy.ListFeatureClasses(feature_type="ALL")

    arcpy.env.workspace = clip_workspace
    clip_feature_classes = arcpy.ListFeatureClasses(feature_type="ALL")

    for in_feature_class in in_feature_classes:
        for clip_feature_class in clip_feature_classes:
            # Extract the base name of the input feature class (without extension)
            in_feature_base_name = os.path.splitext(os.path.basename(in_feature_class))[0]

            # Extract the base name of the clip feature class (without extension)
            clip_feature_base_name = os.path.splitext(os.path.basename(clip_feature_class))[0]

            # Create the output feature class name
            out_feature_class_name = f"{clip_feature_base_name}_{in_feature_base_name}.shp"
            out_feature_class = os.path.join(out_workspace, out_feature_class_name)

            # Use os.path.join for constructing paths to avoid platform-specific issues
            arcpy.analysis.Clip(in_features=os.path.join(in_workspace, in_feature_class),
                                clip_features=os.path.join(clip_workspace, clip_feature_class),
                                out_feature_class=out_feature_class)

            print(f"Clipping {in_feature_base_name}.shp with {clip_feature_base_name}.shp to create {out_feature_class}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: batch_clipper.py <InWorkspace> <ClipWorkspace> <OutputWorkspace>")
        sys.exit(1)

    in_workspace = sys.argv[1]
    clip_workspace = sys.argv[2]
    out_workspace = sys.argv[3]

    batch_clipper(in_workspace, clip_workspace, out_workspace)

