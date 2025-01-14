import pyrealsense2 as rs
import numpy as np
import cv2

# 创建Realsense管道
pipeline = rs.pipeline()
config = rs.config()

# 配置管道以获取深度和RGB数据
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# 启动管道
pipeline.start(config)

# 创建一个OpenCV窗口
cv2.namedWindow("RealSense", cv2.WINDOW_AUTOSIZE)

while True:
    # 获取一帧数据
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()

    # 将数据转换为numpy数组
    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())

    # 转换为灰度图像
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

    # 使用Canny边缘检测来识别物体
    edges = cv2.Canny(gray_image, 100, 200)

    # 查找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 在原图上绘制边框
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # 过滤掉小面积的噪声
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(color_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 显示图像
    cv2.imshow("RealSense", color_image)

    # 按'q'键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
pipeline.stop()
cv2.destroyAllWindows()
