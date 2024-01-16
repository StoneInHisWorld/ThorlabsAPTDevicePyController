from time import sleep
from pylablib.devices import Thorlabs


def move_and_handle():
    # 设置单次移动距离，1step = 2.83e-5mm
    # 距离太短可能动不起来
    distance = 100000
    # 检测当前电脑连接的设备
    device_list = Thorlabs.list_kinesis_devices()
    print(device_list)
    # 在这里输入APT/Kinesis设备的序列号
    stage = Thorlabs.KinesisMotor("83******")
    print(f'\r电机位置归零中……', flush=True, end='')
    stage.move_to(0)
    stage.wait_move()
    print(f"电机归位")
    for wait in range(10, 0, -1):
        print(f'\r实验将于{wait}秒后开始，请做好准备！', flush=True, end='')
    for _ in range(8):
        stage.move_by(distance)
        stage.wait_move()
        print(stage.get_position())
    sleep(10)
    stage.move_to(0)
    stage.wait_move()
    stage.close()