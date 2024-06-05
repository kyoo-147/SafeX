# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)
import Jetson.GPIO as GPIO
import time

def X_Buzzer_Alarm(buzzer_pin, initial_delay, decrement, duration):
    """
    Điều khiển buzzer với các tham số được truyền vào.

    Parameters:
    buzzer_pin (int): Chân GPIO của buzzer.
    initial_delay (float): Thời gian chờ ban đầu giữa các lần bật/tắt buzzer.
    decrement (float): Giá trị giảm của thời gian chờ sau mỗi lần bật/tắt.
    duration (float): Thời gian tổng cộng chạy còi báo.
    """
    # Thiết lập chân GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buzzer_pin, GPIO.OUT)

    try:
        start_time = time.time()
        delay = initial_delay

        while (time.time() - start_time) < duration:
            GPIO.output(buzzer_pin, GPIO.HIGH)  # Bật buzzer
            time.sleep(delay)
            GPIO.output(buzzer_pin, GPIO.LOW)   # Tắt buzzer
            time.sleep(delay)

            # Giảm thời gian chờ dần dần để tăng tần suất bật/tắt của buzzer
            delay = max(0, delay - decrement)

    except KeyboardInterrupt:
        print("Kết thúc chương trình")

    finally:
        GPIO.cleanup()  # Đặt lại trạng thái của các chân GPIO
