#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# ==========================
# PID 쓸 경우 대비하여 남겨둠
# ==========================
import math

class PID:
    def __init__(self):
        self.P_GAIN = 5.0
        self.I_GAIN = 0.0
        self.D_GAIN = 0.0

        # error = Target - Current (목표값과 현재 값의 차이)
        # acc_error += Error (누적오차)
        # prev_error == error(t-1)
        # error_gap = error(t) - error(t-1) (현재 스텝과 이전 스텝의 오차)
        self.error, self.acc_error = 0.0, 0.0
        self.prev_error, self.error_gap = 0.0, 0.0
        
        # pid control 결과 값
        self.pControl, self.iControl = 0.0, 0.0
        self.dControl, self.pidControl = 0.0, 0.0

        self.time = 0.033  # 30HZ --> 0.033 sec
    
    # motor speed 값을 실제 m/s단위로 변환
    def conv_to_real_speed(self, motor_val):
        if motor_val >= 20.0:
            motor_val = 20.0
        real_speed = motor_val * 0.08 # (8/100)
        return real_speed

    def p_control_system(self, current_speed, target_speed):
        self.error = self.conv_to_real_speed(target_speed) - current_speed
        self.pControl = self.P_GAIN * self.error

    def i_control_system(self):
        self.acc_error += self.error
        self.iControl = self.I_GAIN * self.acc_error * self.time

    def d_control_system(self):
        self.error_gap = self.error - self.prev_error
        self.dControl = self.D_GAIN * (self.error_gap / self.time)
        self.prev_error = self.error


    def pid_control_system(self):
        self.pidControl = self.pControl + self.iControl + self.dControl

    def pid_main(self, current_speed, target_speed):
        self.p_control_system(current_speed, target_speed)
        self.i_control_system()
        self.d_control_system()
        self.pid_control_system()
        controlled_speed = self.pidControl * 12.5  # (100/8)
        
        # 최대 속도 범위 제한
        if controlled_speed >= 20.0:
            controlled_speed = 20.0
        
        return controlled_speed
