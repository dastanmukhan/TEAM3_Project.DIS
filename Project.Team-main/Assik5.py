import open3d as o3d
import numpy as np
import copy

print("=" * 80)
print("OPEN3D ASSIGNMENT #5 - 3D MODEL PROCESSING")
print("=" * 80)

# ============================================================================
# STEP 1: Loading and Visualization
# ============================================================================
print("\n" + "=" * 80)
print("STEP 1: LOADING AND VISUALIZATION")
print("=" * 80)

# Load the 3D model (replace with your .obj file path)
mesh_file = "cow.obj"  # CHANGE THIS to your file path
mesh = o3d.io.read_triangle_mesh(mesh_file)

# Compute normals if not present
if not mesh.has_vertex_normals():
    mesh.compute_vertex_normals()

# Print information
print(f"Number of vertices: {len(mesh.vertices)}")
print(f"Number of triangles: {len(mesh.triangles)}")
print(f"Has vertex colors: {mesh.has_vertex_colors()}")
print(f"Has vertex normals: {mesh.has_vertex_normals()}")

# Visualize original model
print("\nDisplaying original mesh...")
o3d.visualization.draw_geometries([mesh], 
                                   window_name="Step 1: Original Mesh",
                                   width=800, height=600)

# ============================================================================
# STEP 2: Conversion to Point Cloud
# ============================================================================
print("\n" + "=" * 80)
print("STEP 2: CONVERSION TO POINT CLOUD")
print("=" * 80)

# Sample points from the mesh
pcd = mesh.sample_points_uniformly(number_of_points=10000)

# Print information
print(f"Number of points: {len(pcd.points)}")
print(f"Has colors: {pcd.has_colors()}")
print(f"Has normals: {pcd.has_normals()}")

# Visualize point cloud
print("\nDisplaying point cloud...")
o3d.visualization.draw_geometries([pcd], 
                                   window_name="Step 2: Point Cloud",
                                   width=800, height=600)

# ============================================================================
# STEP 3: Surface Reconstruction from Point Cloud
# ============================================================================
print("\n" + "=" * 80)
print("STEP 3: SURFACE RECONSTRUCTION")
print("=" * 80)

# Estimate normals for reconstruction
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
    radius=0.1, max_nn=30))

# Perform Poisson surface reconstruction
print("Performing Poisson reconstruction...")
mesh_poisson, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
    pcd, depth=9)

# Remove low-density vertices (artifacts)
densities = np.asarray(densities)
density_threshold = np.quantile(densities, 0.01)
vertices_to_remove = densities < density_threshold
mesh_poisson.remove_vertices_by_mask(vertices_to_remove)

# Crop using bounding box
bbox = pcd.get_axis_aligned_bounding_box()
mesh_poisson = mesh_poisson.crop(bbox)

# Print information
print(f"Number of vertices: {len(mesh_poisson.vertices)}")
print(f"Number of triangles: {len(mesh_poisson.triangles)}")
print(f"Has vertex colors: {mesh_poisson.has_vertex_colors()}")

# Visualize reconstructed mesh
mesh_poisson.compute_vertex_normals()
print("\nDisplaying reconstructed mesh...")
o3d.visualization.draw_geometries([mesh_poisson], 
                                   window_name="Step 3: Reconstructed Mesh",
                                   width=800, height=600)

# ============================================================================
# STEP 4: Voxelization
# ============================================================================
print("\n" + "=" * 80)
print("STEP 4: VOXELIZATION")
print("=" * 80)

# Calculate appropriate voxel size based on point cloud dimensions
bbox = pcd.get_axis_aligned_bounding_box()
bbox_size = bbox.get_max_bound() - bbox.get_min_bound()
max_dimension = bbox_size.max()

# Set voxel size as a fraction of the maximum dimension
voxel_size = max_dimension / 20  # Adjust this divisor if needed (try 15-30)

print(f"Bounding box size: {bbox_size}")
print(f"Max dimension: {max_dimension:.3f}")
print(f"Calculated voxel size: {voxel_size:.3f}")

# Create voxel grid from point cloud
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size)

# Get voxels information
voxels = voxel_grid.get_voxels()
print(f"Number of voxels: {len(voxels)}")

# Check if we have voxels
if len(voxels) == 0:
    print("WARNING: No voxels created. Trying with larger voxel size...")
    voxel_size = max_dimension / 10
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size)
    voxels = voxel_grid.get_voxels()
    print(f"New voxel size: {voxel_size:.3f}")
    print(f"Number of voxels: {len(voxels)}")

# Visualize voxel grid
print("\nDisplaying voxel grid...")
o3d.visualization.draw_geometries([voxel_grid], 
                                   window_name="Step 4: Voxel Grid",
                                   width=800, height=600,
                                   point_show_normal=False)

# ============================================================================
# STEP 5: Adding a Plane
# ============================================================================
print("\n" + "=" * 80)
print("STEP 5: ADDING A PLANE")
print("=" * 80)

# Get bounding box of the point cloud
bbox = pcd.get_axis_aligned_bounding_box()
center = bbox.get_center()
bbox_extent = bbox.get_max_bound() - bbox.get_min_bound()

# Create a vertical plane (YZ plane) next to the object
plane_height = bbox_extent[1] * 1.5
plane_depth = bbox_extent[2] * 1.5
plane_thickness = 0.01

plane = o3d.geometry.TriangleMesh.create_box(
    width=plane_thickness, 
    height=plane_height, 
    depth=plane_depth)

# Position the plane at the center X coordinate
plane_position = np.array([
    center[0] - plane_thickness/2,
    center[1] - plane_height/2,
    center[2] - plane_depth/2
])
plane.translate(plane_position)

# Color the plane
plane.paint_uniform_color([0.8, 0.2, 0.2])  # Red color
plane.compute_vertex_normals()

print(f"Plane positioned at X = {center[0]:.3f}")
print(f"Plane dimensions: {plane_thickness:.3f} x {plane_height:.3f} x {plane_depth:.3f}")
print(f"Object center: [{center[0]:.3f}, {center[1]:.3f}, {center[2]:.3f}]")

# Create a copy of point cloud for visualization
pcd_display = copy.deepcopy(pcd)

# Visualize object with plane
print("\nDisplaying point cloud with plane...")
print("Red plane is positioned at the center of the object")
o3d.visualization.draw_geometries([pcd_display, plane], 
                                   window_name="Step 5: Object with Plane",
                                   width=800, height=600)

# ============================================================================
# STEP 6: Surface Clipping
# ============================================================================
print("\n" + "=" * 80)
print("STEP 6: SURFACE CLIPPING")
print("=" * 80)

# Clip points on the right side of the plane (X > center[0])
points = np.asarray(pcd.points)
colors = np.asarray(pcd.colors) if pcd.has_colors() else None

print(f"Plane position (X): {center[0]:.3f}")
print(f"Clipping all points where X > {center[0]:.3f}")

# Keep points on the left side of the plane
mask = points[:, 0] < center[0]
clipped_points = points[mask]

# Create new point cloud with clipped points
pcd_clipped = o3d.geometry.PointCloud()
pcd_clipped.points = o3d.utility.Vector3dVector(clipped_points)
if colors is not None and len(colors) > 0:
    pcd_clipped.colors = o3d.utility.Vector3dVector(colors[mask])

# Reconstruct mesh from clipped point cloud
print("Reconstructing mesh from clipped points...")
pcd_clipped.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
    radius=0.1, max_nn=30))

mesh_clipped, densities_clip = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
    pcd_clipped, depth=9)

# Clean up the clipped mesh
densities_clip = np.asarray(densities_clip)
if len(densities_clip) > 0:
    density_threshold = np.quantile(densities_clip, 0.01)
    vertices_to_remove = densities_clip < density_threshold
    mesh_clipped.remove_vertices_by_mask(vertices_to_remove)

mesh_clipped.compute_vertex_normals()

# Print information
print(f"\nOriginal number of points: {len(points)}")
print(f"Remaining points after clipping: {len(clipped_points)}")
print(f"Points removed: {len(points) - len(clipped_points)}")
print(f"Number of vertices in clipped mesh: {len(mesh_clipped.vertices)}")
print(f"Number of triangles in clipped mesh: {len(mesh_clipped.triangles)}")
print(f"Has vertex colors: {mesh_clipped.has_vertex_colors()}")
print(f"Has vertex normals: {mesh_clipped.has_vertex_normals()}")

# Visualize clipped mesh with plane
print("\nDisplaying clipped mesh with plane...")
o3d.visualization.draw_geometries([mesh_clipped], 
                                   window_name="Step 6: Clipped Mesh",
                                   width=800, height=600)

# ============================================================================
# STEP 7: Working with Color and Extremes
# ============================================================================
print("\n" + "=" * 80)
print("STEP 7: WORKING WITH COLOR AND EXTREMES")
print("=" * 80)

# Use the clipped point cloud
points = np.asarray(pcd_clipped.points)

# Apply gradient along Z axis
z_values = points[:, 2]
z_min, z_max = z_values.min(), z_values.max()
z_normalized = (z_values - z_min) / (z_max - z_min + 1e-8)

# Create color gradient (blue to red)
colors = np.zeros((len(points), 3))
colors[:, 0] = z_normalized  # Red channel increases with Z
colors[:, 2] = 1 - z_normalized  # Blue channel decreases with Z

pcd_colored = o3d.geometry.PointCloud()
pcd_colored.points = o3d.utility.Vector3dVector(points)
pcd_colored.colors = o3d.utility.Vector3dVector(colors)

# Find extreme points along Z axis
z_min_idx = np.argmin(z_values)
z_max_idx = np.argmax(z_values)

min_point = points[z_min_idx]
max_point = points[z_max_idx]

print(f"Applying gradient along Z axis")
print(f"Z range: [{z_min:.3f}, {z_max:.3f}]")
print(f"\nMinimum Z point:")
print(f"  Coordinates: X={min_point[0]:.3f}, Y={min_point[1]:.3f}, Z={min_point[2]:.3f}")
print(f"\nMaximum Z point:")
print(f"  Coordinates: X={max_point[0]:.3f}, Y={max_point[1]:.3f}, Z={max_point[2]:.3f}")

# Create spheres at extreme points
sphere_radius = (z_max - z_min) * 0.05  # Proportional to object size

sphere_min = o3d.geometry.TriangleMesh.create_sphere(radius=sphere_radius)
sphere_min.translate(min_point)
sphere_min.paint_uniform_color([0, 1, 0])  # Green for minimum
sphere_min.compute_vertex_normals()

sphere_max = o3d.geometry.TriangleMesh.create_sphere(radius=sphere_radius)
sphere_max.translate(max_point)
sphere_max.paint_uniform_color([1, 1, 0])  # Yellow for maximum
sphere_max.compute_vertex_normals()

# Visualize colored point cloud with extreme points
print("\nDisplaying colored point cloud with extreme points...")
print("  Green sphere = Minimum Z point")
print("  Yellow sphere = Maximum Z point")
print("  Color gradient: Blue (low Z) -> Red (high Z)")
o3d.visualization.draw_geometries([pcd_colored, sphere_min, sphere_max], 
                                   window_name="Step 7: Colored with Extremes",
                                   width=800, height=600)

print("\n" + "=" * 80)
print("ALL STEPS COMPLETED SUCCESSFULLY!")
print("=" * 80)