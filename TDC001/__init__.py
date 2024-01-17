from pylablib.devices import Thorlabs
from tqdm import tqdm


def move_and_handle(stage, dis_per_step, n_step,
                    before_handler=None, back_handler=None,
                    home=True, back=True):
    """
    移动电机前后做出某种动作，如此往复直至完成任务。
    :param stage: 电机对象
    :param dis_per_step: 每步移动的距离，目前测算本值 1 = 2.83e-5mm。注意：距离太短，电机可能动不起来。
    :param n_step: 任务需要移动多少步。
    :param before_handler: 每次移动前执行的动作，签名需为：def handler(position) -> None，position:int为当前电机位置。
    :param back_handler: 每次移动后执行的动作，签名需为：def handler(position) -> None，position:int为当前电机位置。
    :param home: 执行任务之前是否将位置归零。
    :param back: 完成任务后，是否将电机位置归零。
    :return: None
    """
    if home:
        print(f'\r电机位置归零中……', flush=True, end='')
        stage.move_to(0)
        stage.wait_move()
        print(f"电机归位")
    for wait in range(10, 0, -1):
        print(f'\r实验将于{wait}秒后开始，请做好准备！', flush=True, end='')
    with tqdm(range(n_step), unit='步', position=0, desc='移动中……', mininterval=1) as pbar:
        if before_handler is not None:
            before_handler(stage.get_position())
        pbar.set_description("移动中……")
        stage.move_by(dis_per_step)
        stage.wait_move()
        cur_pos = stage.get_position()
        if back_handler is not None:
            back_handler(stage.get_position())
        pbar.set_description(f"当前位置为：{cur_pos}")
    for wait in range(10, 0, -1):
        print(f'\r电机将于{wait}秒后归位，请做好准备！', flush=True, end='')
    if back:
        stage.move_to(0)
        stage.wait_move()


def connect_device(SN):
    """
    检查连接至当前电脑的索雷博设备，并连接。
    :param SN: 索雷博设备的序列号，需为字符串类型
    :return: 连接到的设备
    :raise: 连接失败错误
    """
    # 检测当前电脑连接的设备
    device_list = Thorlabs.list_kinesis_devices()
    if SN in device_list:
        return Thorlabs.KinesisMotor(SN)
    else:
        raise Exception(f'无法找到序列号为{SN}的设备，当前连接到电脑的设备为{device_list}')


def disconnect_device(stage) -> None:
    """
    与设备断开连接
    :param stage: 设备对象
    :return: None
    """
    stage.close()
