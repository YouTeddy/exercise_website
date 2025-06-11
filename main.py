# main.py 또는 app.py 등의 메인 실행 파일

import customtkinter as ctk
import gui  # gui.py 파일을 임포트합니다.

def run():
    # customtkinter의 메인 윈도우(root)를 생성합니다.
    root = ctk.CTk()

    # gui.py 파일의 setup_gui 함수를 호출하여 GUI를 설정하고,
    # 위젯들과 root 윈도우 객체를 반환받습니다.
    # 반환되는 튜플의 마지막 요소가 root 윈도우입니다.
    height_entry, weight_entry, age_entry, level_var, goal_var, day_vars, \
    elbow_pain_var, shoulder_pain_var, wrist_pain_var, knee_pain_var, \
    ankle_pain_var, back_pain_var, bmi_text, result_text, \
    exclude_chest_var, exclude_back_var, exclude_legs_var, \
    exclude_shoulders_var, exclude_abs_var, exclude_fullbody_var, \
    root_window = gui.setup_gui(root)

    # GUI의 메인 이벤트 루프를 시작합니다.
    # root_window는 gui.setup_gui에서 반환된 root 객체와 동일합니다.
    root_window.mainloop()

if __name__ == "__main__":
    run()