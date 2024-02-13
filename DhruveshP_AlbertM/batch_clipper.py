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

            out_feature_class_name = f"{clip_feature_class}_{os.path.basename(in_feature_class)}"
            out_feature_class = os.path.join(out_workspace, out_feature_class_name)


            arcpy.analysis.Clip(in_features=os.path.join(in_workspace, in_feature_class),
                                clip_features=clip_feature_class,
                                out_feature_class=out_feature_class)

            print(f"Clipping {in_feature_class} with {clip_feature_class} to create {out_feature_class}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: batch_clipper.py <InWorkspace> <ClipWorkspace> <OutputWorkspace>")
        sys.exit(1)

    in_workspace = sys.argv[1]
    clip_workspace = sys.argv[2]
    out_workspace = sys.argv[3]

    batch_clipper(in_workspace, clip_workspace, out_workspace)

