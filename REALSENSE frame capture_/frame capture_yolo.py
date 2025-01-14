import torch
import cv2
import numpy as np

# 加载 YOLOv5 模型（可以使用 yolov5s, yolov5m, yolov5l, yolov5x）
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # 这里加载的是 yolov5s 模型

# 读取图像
img = cv2.imread("/path/to/your/image.jpg")

# YOLOv5 推理
results = model(img)

# 打印推理结果（物体类别和置信度）
results.print()  

# 画出物体边框
results.show()  # 可以显示推理结果图像

# 获取推理结果的边框信息
boxes = results.xyxy[0].cpu().numpy()  # 获取边框坐标
for box in boxes:
    x1, y1, x2, y2, conf, cls = box
    label = model.names[int(cls)]  # 获取物体的类别名称
    print(f"Detected {label} with confidence {conf:.2f}")

    # 画出边框
    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    cv2.putText(img, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# 显示图像
cv2.imshow("Detected Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
