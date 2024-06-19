from presage_physiology_preprocessing import mediapipefunctions
import ffmpeg
import json
import cv2
import numpy as np
from presage_physiology_preprocessing.version import __version__
class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)

def get_x_int(pt1, pt2):
    """
    with pt1 and pt2 creating a line, what is the intercept x point of that line with y=0
    pt1 and pt2 are tuples [x1,y1] and [x2,y2], respectively
    """
    m = (pt2[1] - pt1[1])/(pt2[0] - pt1[0])
    x0 = pt2[0]-pt2[1]/m
    return x0

def track_points_rr(frame, frame_prev, points_prev):
    corners = []
    try:
        lk_params = dict(winSize=(15, 15),
                         maxLevel=3,
                         criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        corners_1, corners_Found1, err1 = cv2.calcOpticalFlowPyrLK(frame_prev, frame, points_prev, None, **lk_params)
        corners_0, corners_Found2, err2 = cv2.calcOpticalFlowPyrLK(frame, frame_prev, corners_1, None, **lk_params)
        corners_1v = []
        corners_0v = []

        for cc in range(points_prev.shape[0]):
            if (corners_Found1[cc] and corners_Found2[cc]) and (np.sqrt(np.sum((points_prev[cc]-corners_0[cc])**2)) < 2 ):
                corners_0v.append(corners_0[cc])
                corners_1v.append(corners_1[cc])
            else:
                corners_0v.append(np.array([[np.nan, np.nan]]))
                corners_1v.append(np.array([[np.nan, np.nan]]))
        corners_0v = np.array(corners_0v)
        corners_1v = np.array(corners_1v)
        corners = np.float32(corners_1v)

        # corners = np.array(corners_1v)
        valid_count = np.sum([~np.isnan(x[0][0]) for x in corners])
    except Exception as ex:
        print(f'Error in track points rr: {ex}')
    return corners

def get_rr_tracking_pts(frame, face_location):
    """
    returns chest, and left right shoulder rois - binary mask same size as input
    """
    corners = []
    corner_labels = []

    try:
        with mediapipefunctions.POSE.Pose(
            model_complexity=1,
            enable_segmentation=True,
                min_detection_confidence=0.5) as pose:

            sz = frame.shape[0:2]
            # Convert the BGR image to RGB before processing.
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            lshoulder = results.pose_landmarks.landmark[mediapipefunctions.POSE.PoseLandmark.RIGHT_SHOULDER]
            rshoulder = results.pose_landmarks.landmark[mediapipefunctions.POSE.PoseLandmark.LEFT_SHOULDER]
            lhip = results.pose_landmarks.landmark[mediapipefunctions.POSE.PoseLandmark.RIGHT_HIP]
            rhip = results.pose_landmarks.landmark[mediapipefunctions.POSE.PoseLandmark.LEFT_HIP]

            rshoulder = [int(rshoulder.x * sz[1]), int(rshoulder.y * sz[0])]
            lshoulder = [int(lshoulder.x * sz[1]), int(lshoulder.y * sz[0])]
            rhip = [int(rhip.x * sz[1]), int(rhip.y * sz[0])]
            lhip = [int(lhip.x * sz[1]), int(lhip.y * sz[0])]

            lxint = get_x_int(lhip, lshoulder)
            rxint = get_x_int(rhip, rshoulder)


            polygon = np.array([[lhip[0], lhip[1]],
                                [lshoulder[0], lshoulder[1]],
                                [lxint, 0],
                                [rxint, 0],
                                [rshoulder[0], rshoulder[1]],
                                [rhip[0], rhip[1]]], dtype='int32')

            polygon_chest = np.array([[lhip[0], lhip[1]],
                                [lshoulder[0], lshoulder[1]],
                                [rshoulder[0], rshoulder[1]],
                                [rhip[0], rhip[1]]], dtype='int32')

            polygon_face = []
            smaller_face = False
            if len(face_location)>4:
                polygon_face = np.array(face_location, dtype='int32')
            elif len(face_location)>0:
                polygon_face = np.array([
                                   [face_location[0], face_location[3]],
                                   [face_location[2], face_location[3]],
                                   [face_location[2], face_location[1]],
                                   [face_location[0], face_location[1]]], dtype='int32')
            else:
                # here we use mp to extract the face points
                smaller_face = True
                for i in range(11):
                    polygon_face.append(
                                [int(results.pose_landmarks.landmark[i].x * sz[1]),
                                 int(results.pose_landmarks.landmark[i].y * sz[0])])

                polygon_face = np.array(polygon_face, dtype='int32')

            upper_mask = np.zeros(frame.shape[0:2])
            if len(polygon) > 0:
                hull = cv2.convexHull(polygon)
                upper_mask = cv2.fillConvexPoly(upper_mask, hull, 1)
            upper_mask = upper_mask > 0.5

            chest_mask = np.zeros(frame.shape[0:2])
            if len(polygon_chest) > 0:
                hull = cv2.convexHull(polygon_chest)
                chest_mask = cv2.fillConvexPoly(chest_mask, hull, 1)
            chest_mask = chest_mask > 0.5


            face_mask = np.zeros(frame.shape[0:2])
            if len(polygon_face) > 0:
                hull = cv2.convexHull(polygon_face)
                face_mask = cv2.fillConvexPoly(face_mask, hull, 1)
            if False: #smaller_face:
                dilate_sz = int(np.sum(face_mask)**.5/4)
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_sz, dilate_sz))
                face_mask = cv2.dilate(face_mask, kernel, iterations=2)
            face_mask = face_mask > 0.5


            pose_mask = results.segmentation_mask > .5

            # for the area we use, assume 15^2 points, must be spaced this much apart
            min_distance = round(np.sum((upper_mask & pose_mask).astype('uint8'))**.5/15)
            feature_params = dict(maxCorners=225, qualityLevel=.0005, minDistance=min_distance)  # , blockSize=3)
            corners = cv2.goodFeaturesToTrack(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                                              mask=(upper_mask & pose_mask & ~face_mask).astype('uint8'), **feature_params)


            # ret, thresh = cv2.threshold(chest_mask*255, 125, 255, cv2.THRESH_BINARY_INV) #, 0.5, 1, 0)
            contours_chest, hierarchy = cv2.findContours(chest_mask.astype('uint8'), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours_face, hierarchy = cv2.findContours(face_mask.astype('uint8'), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            corner_labels = np.zeros(corners.shape[0])
            for ipt in range(corners.shape[0]):
                closest_chest = cv2.pointPolygonTest(contours_chest[0],  (corners[ipt,0,0], corners[ipt,0,1]), True)
                closest_face = cv2.pointPolygonTest(contours_face[0], (corners[ipt, 0, 0], corners[ipt, 0, 1]), True)
                if closest_face > closest_chest:  # closer to face, within face point (1)
                    corner_labels[ipt] = 1

    except Exception as ex:
        pass
    return corners, corner_labels

def average_rois(frame, points):
    """
       inputs: frame (frame in BGR); points (face mesh points)
       outputs: average of BGR values in face mesh points

       computes the convex hull of the face and then takes average of RGB values
       """
    # forehead
    left_fh_t = [54, 68, 104, 69, 67, 103]
    left_fh_b = [68, 63, 105, 66, 69, 104]
    center_fh_lt = [67, 69, 108, 151, 10, 109]
    center_fh_lb = [69, 66, 107, 9, 151, 108]
    center_fh_rt = [10, 151, 337, 299, 297, 338]
    center_fh_rb = [151, 9, 336, 296, 299, 337]
    right_fh_t = [297, 299, 333, 298, 284, 332]
    right_fh_b = [299, 296, 334, 293, 298, 333]
    center_fh_b = [107, 55, 193, 168, 417, 285, 336, 9]
    # nose
    nose_top = [193, 122, 196, 197, 419, 351, 417, 168]
    nose_bot = [196, 3, 51, 45, 275, 281, 248, 419, 197]
    # left cheek
    lc_t = [31, 117, 50, 101, 100, 47, 114, 121, 230, 229]
    lc_b = [50, 187, 207, 206, 203, 129, 142, 101]
    # right cheek
    rc_t = [261, 346, 280, 330, 329, 277, 343, 350, 450, 449, 448]
    rc_b = [280, 411, 427, 426, 423, 358, 371, 330]
    all_rois = [left_fh_t, left_fh_b, center_fh_lt, center_fh_lb, center_fh_rt, center_fh_rb, right_fh_t, right_fh_b,
                center_fh_b, nose_top, nose_bot, lc_t, lc_b, rc_t, rc_b]

    grid_bgr = np.zeros((len(all_rois),3))
    points = np.array(np.squeeze(points), dtype='int32')
    h, w, _ = frame.shape
    dummy_mat = np.zeros((h, w)).astype(np.int32)

    for ccc, kk in enumerate(all_rois):
        outline = np.squeeze(cv2.convexHull(points[kk, :]))
        face_mask = cv2.fillPoly(dummy_mat.copy(), [outline], 1)
        grid_bgr[ccc, :] = np.array(cv2.mean(frame, face_mask.astype(np.uint8)))[:-1]

    outline = np.squeeze(cv2.convexHull(points))
    face_mask = cv2.fillPoly(dummy_mat.copy(), [outline], 1)
    whole_face = np.array(cv2.mean(frame, face_mask.astype(np.uint8)))[:-1]
    return np.around(whole_face, decimals=8), np.around(grid_bgr, decimals=8)

def get_face_values(frame, face_points):
    """
    get_face_values gets intensity of image within ROIs
    """
    bgr = average_rois(frame, face_points)
    return bgr
def track_points_face(frame):
    """
    Updates the new mesh face vertices simply by calling mediapipe again with the new frame
    - using the old model as input, we get less jitter and it's significantly faster
    """
    try:
        mesh_pts= mediapipefunctions.get_face_mesh_landmarks(frame, mediapipefunctions.FACE_MESH)
        return mesh_pts

    except Exception as e:
        print(f'Error in track points face: {e}')
        return None

    if not mesh_pts:
        print("No Face")
        return None

def get_face_points(frame):
    """
    get_face_points gets usable points to track on the face
    - get feature landmarks on face (eg. from dlib or mediapipe)
    - get ROIs
    - get "good points to track" within particular ROI
    - get the boundary of the face (using face mesh or otherwise)
    - if None for track points (pts) and face mesh points (current_face_cords)

    returns pts (good points to track for tracking), current_face_cords (media pipe face mesh points)
    returns pts: None, current_face_cords: None if there is no face found to trigger a reset
    """
    try:
        pts= mediapipefunctions.get_face_mesh_landmarks(frame, mediapipefunctions.FACE_MESH)
    except Exception as e:
        print(f'Error in getting face points: {e}')
        pts = None
    return pts
def process_frame_rr(frame, frame_last, traces_last):
    """
    proces_frame_rr analyzes the image to extract points to be tracked on upper body regions
    - reset flag turned on when tracking needs to be reset
    """
    save_face = False
    # todo: fix resets
    try:
        face_location = traces_last['hr_pts']
    except:
        save_face = True
        face_location = get_face_points(frame)

    try:
        rr_pts_prev = traces_last["rr_pts"]
        rr_pt_labels = traces_last["rr_pt_labels"]
    except:
        rr_pts_prev = []
        rr_pt_labels = []

    valid_count = np.sum([~np.isnan(x[0][0]) for x in rr_pts_prev])
    if valid_count < 20:
        reset_flag = True
        rr_pts, rr_pt_labels = get_rr_tracking_pts(frame, face_location)
    else:
        reset_flag = False
        rr_pts = track_points_rr(frame, frame_last, rr_pts_prev)

    valid_count = np.sum([~np.isnan(x[0][0]) for x in rr_pts])
    data = {"rr_pts": rr_pts, "rr_pt_labels": rr_pt_labels, 'rr_reset': reset_flag}
    if save_face:
        data['hr_pts'] = face_location
    return data


def process_frame_pleth(frame):
    """
    process_frame_pleth analyzes the image to extract the face location, points to track, and ultimately the RGB traces
    - all data here can be used for HR/RR/SpO2/HRV/pleth generation
    - frame_analyzed is a dictionary of all analysis content
    """
    bgr = []
    if mediapipefunctions.FACE_MESH is None:
        hr_pts = get_face_points(frame)
    else:
        try:
            hr_pts = track_points_face(frame)
        except:
            # here we are in a "reset" state.  the last frame analyzed didn't have points, so we start over
            hr_pts = get_face_points(frame)

    if hr_pts is not None:
        bgr = get_face_values(frame, hr_pts)  # mean RGB over ROIs
    return {"bgr": bgr, "hr_pts": hr_pts}

def frame_skipper(fps_current, fps_desired):
    """
    computes the number of frames to skip given the original fps and the desired fps
    - eg. if og fps = 30, and desired is 10fps, then we must skip 3 frames (eg. every 3rd frame) to ensure that
    """
    if fps_desired == float('inf'):
        mod_amount = 1
    else:
        mod_amount = int(np.round(fps_current / fps_desired))
    return mod_amount


def frame_skipper_rr(fps, mod_hr):
    """
    this function tries to find the optimal number of frames to jump such that
    we are maximizing overlap between HR analysis and RR analysis
    - RR is optimal when analyzed on the order of 3-8 FPS
    """
    rr_fps_ideal = 5
    mod_rr = frame_skipper(fps, rr_fps_ideal)
    # mod_rr = round(mod_rr / mod_hr)
    return mod_rr


def video_preprocess(path, HR_FPS=30, DN_SAMPLE=1):
    """
    Video_preprocess reads in a video from source (path) and subsequently processes each frame into a set of variables stored in traces
    - internally used parameter variables are stored in settings
    - traces a python dict which is then serialized into a json object and returned
     - traces can be post processed to extract absolute vital measurements
    """

    traces = {}
    cap = cv2.VideoCapture(path)
    fps_orig = round(cap.get(cv2.CAP_PROP_FPS))
    if fps_orig == 0:
        fps_orig = 30
    vid_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    mod_amount = frame_skipper(fps_orig, HR_FPS)
    mod_amount_rr = frame_skipper_rr(fps_orig, mod_amount)

    traces['settings'] = {
        "FPS_NR_EFF": fps_orig / mod_amount,
        "MOD_AMOUNT_HR": mod_amount,
        "MOD_AMOUNT_RR": mod_amount_rr,
        "preprocessing_version":__version__}
    traces["frames"] = []

    orientation_done = False
    video_metadata = ffmpeg.probe(path)
    use_meta = None
    side_list_location = -1

    #only needed if the vertical video bug persists on mobile
    if cv2.__version__ == "4.6.0":
        for ind in video_metadata["streams"]:
            if ind["codec_type"] == "video":
                use_meta = ind
                break

        if use_meta:
            if len(use_meta.get("side_data_list", [])) > 0:
                for x in range(0, len(use_meta["side_data_list"])):
                    if use_meta["side_data_list"][x].get("displaymatrix", False):
                        side_list_location = x
                        break
    try:
        frame_last_rr = None
        frame_index_last = None
        frame_index_last_rr = None
        # traces[frame_index_last] = None
        # traces[frame_index_last_rr] = None
        fake_time = 0.0
        for frame_index in range(0, vid_length):
            save_time = False
            if frame_index > 0:
                fake_time += 1.0/fps_orig
            frame_data = {}
            ret, frame = cap.read()
            if not ret:
                continue
            if not orientation_done:
                vid_height, vid_width = frame.shape[:2]

                orientation_done = True
            if (frame_index % mod_amount == 0) or (frame_index % mod_amount_rr == 0):
                save_time = True
                if cv2.__version__ == "4.6.0":
                    if frame.shape[0] > frame.shape[1]:
                        if side_list_location > -1:
                            if "\n00000000:            0       65536           0\n00000001:       -65536           0           0" in \
                                    use_meta["side_data_list"][side_list_location]["displaymatrix"]:
                                frame = cv2.rotate(frame, cv2.ROTATE_180)
                        else:
                            frame = cv2.rotate(frame, cv2.ROTATE_180)

                dn_frame = cv2.resize(frame,
                                   (frame.shape[1] // DN_SAMPLE, frame.shape[0] // DN_SAMPLE),
                                   cv2.INTER_AREA)

                if frame_index % mod_amount == 0:
                    #this will likely not apply on mobile since all videos are vertical
                    #but it is a good idea to make sure they are being processed right side up

                    try:
                        frame_data.update(process_frame_pleth(dn_frame))
                    except Exception as e:
                        print(f"Processing error in HR analysis at frame: {frame_index}, error: {e}")
                        pass

                try:
                    # here we compute all metrics associated with RR analysis, tracked points of body
                    if frame_index % mod_amount_rr == 0:
                        if frame_last_rr is None and frame_index_last_rr is None:
                            frame_data.update(process_frame_rr(dn_frame, None, None))
                        else:
                            frame_data.update(process_frame_rr(dn_frame, frame_last_rr, traces["frames"][frame_index_last_rr]))
                        frame_index_last_rr = len(traces["frames"])
                        frame_last_rr = dn_frame

                except Exception as e:
                    print(f"Processing error in RR analysis at frame: {frame_index}, error: {e}")
                    pass

                if save_time:
                    frame_data.update({'time_now': round(fake_time, 3)})
                traces["frames"].append(frame_data)

    except Exception as e:
        print(f"CV2 error at frame: {frame_index}, error: {e}")
        pass
    cap.release()
    return json.loads(json.dumps(traces, cls=NumpyArrayEncoder))
