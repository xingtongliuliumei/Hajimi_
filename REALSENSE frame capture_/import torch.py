import pyrealsense2 as rs

# 查询连接的设备
devices = rs.context().query_devices()

# 打印所有连接的设备
for device in devices:
    print(f"Device found: {device.get_info(rs.camera_info.name)}")

    # 获取设备的深度传感器和颜色传感器
    depth_sensor = device.first_depth_sensor()  # 获取深度传感器
    color_sensor = device.first_color_sensor()  # 获取颜色传感器

    # 获取深度传感器的配置（分辨率、帧率等）
    depth_stream = depth_sensor.get_stream_profiles()
    color_stream = color_sensor.get_stream_profiles()

    # 打印流的配置信息
    print("Depth Stream Profiles:")
    for profile in depth_stream:
        print(f"  {profile}")

    print("Color Stream Profiles:")
    for profile in color_stream:
        print(f"  {profile}")
