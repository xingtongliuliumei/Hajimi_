import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics import YOLO
from sklearn.linear_model import RANSACRegressor
from coco_classes import coco_classes  # 确保coco_classes.py位置正确
import time

# 初始化RealSense管道
pipeline = rs.pipeline()
config = rs.config()

# 启用颜色和深度流
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# 启动管道
profile = pipeline.start(config)

# 获取深度传感器的深度标定值
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

# 对齐颜色和深度帧
align = rs.align(rs.stream.color)

# 加载YOLOv5模型
model = YOLO('yolov5s.pt')  # 请确保模型路径正确

# 用于计算帧率的时间变量
prev_time = time.time()

def estimate_depth_with_ransac(depth_data, num_samples=50):
    sampled_depths = np.random.choice(depth_data.flatten(), num_samples, replace=False)
    ransac = RANSACRegressor()
    X = np.arange(len(sampled_depths)).reshape(-1, 1)
    ransac.fit(X, sampled_depths)
    inlier_mask = ransac.inlier_mask_
    estimated_depth = np.mean(sampled_depths[inlier_mask])
    return estimated_depth

try:
    while True:
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        
        if not color_frame or not depth_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        # 进行YOLOv5模型推理
        results = model(color_image)

        for result in results:  # 遍历检测结果
            boxes = result.boxes  # 获取检测框
            for bbox in boxes:
                class_id = result.names[int(bbox.cls[0])]  # 获取类别名称
                confidence = bbox.conf[0]
                
                if confidence > 0.7:  # 只处理置信度高于0.7的检测结果
                    x1, y1, x2, y2 = bbox.xyxy[0].int().tolist()
                    bbox_depth_data = depth_image[((y1 + y2) // 2 - np.abs(y1 - y2) // 4):((y1 + y2) // 2 + np.abs(y1 - y2) // 4), 
                                                  ((x1 + x2) // 2 - np.abs(x1 - x2) // 4):((x1 + x2) // 2 + np.abs(x1 - x2) // 4)] 
                    # 选择图像中目标框的中心区域来采样深度数据
                    estimated_depth = estimate_depth_with_ransac(bbox_depth_data) * depth_scale
                    
                    # 在图像上绘制检测框和深度信息
                    cv2.rectangle(color_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(color_image, f'{class_id}: {confidence:.2f}, Depth: {estimated_depth:.2f}m', 
                                 (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 计算当前帧的处理时间
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # 在图像上显示实时帧率
        cv2.putText(color_image, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 显示图像
        cv2.imshow('RealSense with YOLOv5 Detection', color_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    pipeline.stop()
    cv2.destroyAllWindows()
