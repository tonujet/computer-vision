import open3d as o3d

cloud = o3d.io.read_point_cloud("out.ply")
o3d.visualization.draw_geometries([cloud], width=650, height=650, left=20, top=20)
