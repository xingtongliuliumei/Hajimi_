import cv2
import numpy as np
import pyrealsense2 as rs
import torch

# 加载YOLOv5模型（根据需要选择不同的模型，例如yolov5s、yolov5m等）
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline.start(config)

# 创建OpenCV窗口
cv2.namedWindow('RealSense YOLOv5 with Depth', cv2.WINDOW_NORMAL)

while True:
    # 获取RealSense视频帧
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()

    # 将颜色帧和深度帧转换为NumPy数组
    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())

    # 使用YOLOv5进行目标检测
    results = model(color_image)

    # 获取检测结果的DataFrame
    detections = results.pandas().xywh[0]  # 获取YOLOv5的输出

    # 渲染检测结果并确保其为可写副本
    output_image = results.render()[0].copy()  # 确保是可写的副本

    # 遍历检测结果并将深度信息显示在框内
    for _, row in detections.iterrows():
        if row['class'] == 0:  # 目标为人物类（class 0）
            # 计算边界框的坐标（xmin, ymin, xmax, ymax）
            x_center, y_center, width, height = row['xcenter'], row['ycenter'], row['width'], row['height']
            x1 = int((x_center - width / 2) * color_image.shape[1])
            y1 = int((y_center - height / 2) * color_image.shape[0])
            x2 = int((x_center + width / 2) * color_image.shape[1])
            y2 = int((y_center + height / 2) * color_image.shape[0])

            # 确保坐标在有效范围内
            center_x = min(max((x1 + x2) // 2, 0), color_image.shape[1] - 1)
            center_y = min(max((y1 + y2) // 2, 0), color_image.shape[0] - 1)

            # 提取中心点的深度值（单位为毫米）
            depth_value = depth_image[center_y, center_x]  # 获取中心点的深度值（单位为毫米）

            # 确保深度值在有效范围内
            depth_value = depth_value * 0.001  # 转换为毫米

            # 限制最大深度值
            depth_value = min(depth_value, 10000)  # 限制显示的最大深度值

            # 打印深度值进行调试
            print(f"Depth at ({center_x}, {center_y}): {depth_value} mm")

            # 在目标框上绘制深度信息
            text = f'Depth: {depth_value:.2f} mm'  # 显示为毫米
            cv2.putText(output_image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # 在窗口中显示检测结果和深度信息
    cv2.imshow('RealSense YOLOv5 with Depth', output_image)

    # 按'q'键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
pipeline.stop()
cv2.destroyAllWindows()
