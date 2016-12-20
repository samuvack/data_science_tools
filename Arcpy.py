# Importing arcpy
import arcpy

# Set the workspace environment
arcpy.env.workspace = "D:/OneDrive/Documenten/Samuel/PhD/Python/ArcPy"

#run Clip_analysis
arcpy.Clip_analysis("standb4", "clipcov", "standby_clip", "1.25")

