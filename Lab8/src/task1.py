import numpy as np
import cv2 as cv
import open3d as o3d

OUT_FN = "out.ply"
PLY_HEADER = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

vis = o3d.visualization.VisualizerWithKeyCallback()
geometry = o3d.io.read_point_cloud(OUT_FN)
vis.create_window(width=650, height=650, left=20, top=20)
vis.add_geometry(geometry)
vis.poll_events()
vis.update_renderer()


def update_3d_geometry(cloud):
    vis.clear_geometries()
    vis.add_geometry(cloud)
    vis.poll_events()
    vis.update_renderer()


def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((PLY_HEADER % dict(vert_num=len(colors) - 1)).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')


def make_3d_reconstruction(
        img_l,
        img_r,
        stereo,
        min_disp,
        num_disp
):
    disp = stereo.compute(img_l, img_r).astype(np.float32) / 16

    h, w = img_l.shape[:2]
    Q = np.float32([[1, 0, 0, -0.5 * w],
                    [0, -1, 0, 0.5 * h],
                    [0, 0, 0, - 0.8 * w],
                    [0, 0, 1, 0]])

    points = cv.reprojectImageTo3D(disp, Q)
    colors = cv.cvtColor(img_l, cv.COLOR_BGR2RGB)

    # Remove 2d background
    mask = disp > disp.min()
    out_points = points[mask]
    out_colors = colors[mask]

    write_ply(OUT_FN, out_points, out_colors)
    cv.imshow('disparity', (disp - min_disp) / num_disp)

    cloud = o3d.io.read_point_cloud(OUT_FN)
    update_3d_geometry(cloud)


def start_loop(get_frame1, get_frame2):
    cv.namedWindow('disp params', cv.WINDOW_NORMAL)
    cv.resizeWindow('disp params', 800, 200)
    cv.createTrackbar('minDisparity', 'disp params', 3, 25, lambda: ...)
    cv.createTrackbar('numDisparities', 'disp params', 1, 17, lambda: ...)
    cv.createTrackbar('blockSize', 'disp params', 5, 50, lambda: ...)
    cv.createTrackbar('disp12MaxDiff', 'disp params', 5, 25, lambda: ...)
    cv.createTrackbar('uniquenessRatio', 'disp params', 4, 99, lambda: ...)
    cv.createTrackbar('speckleWindowSize', 'disp params', 0, 25, lambda: ...)
    cv.createTrackbar('speckleRange', 'disp params', 30, 100, lambda: ...)
    cv.createTrackbar('window_size', 'disp params', 9, 10, lambda: ...)
    # Creating an object of StereoBM algorithm
    stereo = cv.StereoSGBM_create()
    while True:
        # Updating the parameters based on the trackbar positions
        min_disp = cv.getTrackbarPos('minDisparity', 'disp params')
        num_disp = cv.getTrackbarPos('numDisparities', 'disp params') * 16
        block_size = cv.getTrackbarPos('blockSize', 'disp params') * 2 + 5
        disp12_max_diff = cv.getTrackbarPos('disp12MaxDiff', 'disp params')
        uniqueness_ratio = cv.getTrackbarPos('uniquenessRatio', 'disp params')
        speckle_window_size = cv.getTrackbarPos('speckleWindowSize', 'disp params') * 2
        speckle_range = cv.getTrackbarPos('speckleRange', 'disp params')
        window_size = cv.getTrackbarPos('window_size', 'disp params')

        # Adjust parameters
        num_disp = 1 if num_disp == 0 else num_disp
        min_disp = 1 if min_disp == 0 else min_disp

        # Setting the updated parameters before computing disparity map
        stereo.setNumDisparities(1 if num_disp == 0 else num_disp)
        stereo.setBlockSize(block_size)
        stereo.setUniquenessRatio(uniqueness_ratio)
        stereo.setSpeckleRange(speckle_range)
        stereo.setSpeckleWindowSize(speckle_window_size)
        stereo.setDisp12MaxDiff(disp12_max_diff)
        stereo.setMinDisparity(min_disp)
        stereo.setP1(8 * 3 * window_size ** 2, )
        stereo.setP2(32 * 3 * window_size ** 2, )

        make_3d_reconstruction(get_frame1(), get_frame2(), stereo, min_disp, num_disp)

        if cv.waitKey(1) == ord("q"):
            cv.destroyAllWindows()
            break


if __name__ == '__main__':
    img1 = cv.pyrDown(cv.imread("12_1.jpg"))
    img2 = cv.pyrDown(cv.imread("12_4.jpg"))
    cv.imshow("Left image", img1)
    cv.imshow("Right image", img2)
    cv.waitKey()
    start_loop(lambda: img1, lambda: img2)
