import cartagen4py as c4
import numpy as np
import geopandas

constraint = c4.ConstraintMethod(max_iteration=100, norm_tolerance=0.05, verbose=True)

points = geopandas.read_file("cartagen4py/data/data_bourbonnaise/small/points.geojson")
buildings = geopandas.read_file("cartagen4py/data/data_bourbonnaise/small/buildings.geojson")
roads = geopandas.read_file("cartagen4py/data/data_bourbonnaise/small/roads.geojson")
rivers = geopandas.read_file("cartagen4py/data/data_bourbonnaise/small/rivers.geojson")

# buildings = geopandas.read_file("cartagen4py/data/data_bourbonnaise/atomic/buildings.geojson")
# roads = geopandas.read_file("cartagen4py/data/data_bourbonnaise/atomic/roads.geojson")

constraint.add(points, movement=1)
constraint.add(buildings, movement=1, stiffness=10)
constraint.add(roads, movement=1, curvature=10)
constraint.add(rivers, movement=1, curvature=10)

# constraint.add(buildings, movement=1)
# constraint.add(roads, movement=1)

d = constraint.get_objects_number()
distances = np.zeros((d, d))
spatial_weights = np.zeros((d, d))
for i in range(d):
    for j in range(d):
        if i != j:
            distances[i][j] = 8
            spatial_weights[i][j] = 15

constraint.add_spatial_conflicts(distances, spatial_weights)

geometries = constraint.generalize()

for i, g in enumerate(geometries):
    g.to_file("cartagen4py/data/data_bourbonnaise/{0}.geojson".format(i), driver="GeoJSON")