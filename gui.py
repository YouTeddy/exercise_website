import customtkinter as ctk
# functions 모듈은 사용자가 정의한 파일로 가정합니다.
# 이 파일에는 generate_workout, reset_fields 함수가 있어야 합니다.
from functions import generate_workout, reset_fields, open_local_html_file

# 테마 상태를 저장할 전역 변수 (CTkinter IntVar)
# 0: 라이트 모드, 1: 다크 모드
theme_state_var = None

def on_theme_switch_toggle():
    """테마 스위치 상태가 변경될 때 호출되는 함수입니다."""
    global theme_state_var
    if theme_state_var is None:
        return  # 아직 초기화되지 않은 경우

    if theme_state_var.get() == 1:  # 스위치가 켜진 경우 (값 1)
        ctk.set_appearance_mode("dark")
    else:  # 스위치가 꺼진 경우 (값 0)
        ctk.set_appearance_mode("light")

def setup_gui(root):
    """GUI를 설정하고 주요 위젯을 생성합니다."""
    global theme_state_var # 전역 변수 theme_state_var에 IntVar 할당 예정

    # 다른 전역 위젯 변수 선언 (원래 코드와 동일하게 유지)
    global bmi_text
    global height_entry, weight_entry, age_entry
    global level_var, goal_var
    global day_vars
    global elbow_pain_var, shoulder_pain_var, wrist_pain_var, knee_pain_var, ankle_pain_var, back_pain_var
    global exclude_chest_var, exclude_back_var, exclude_legs_var, exclude_shoulders_var, exclude_abs_var, exclude_fullbody_var
    global result_text

    # 초기 외형 모드 설정: light
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # theme_state_var 초기화: 라이트 모드이므로 스위치는 꺼진 상태 (0)
    theme_state_var = ctk.IntVar(value=0)

    root.title("개인 맞춤형 운동 루틴 추천 프로그램")
    root.geometry("600x1117")

    # BMI 표시 레이블
    bmi_text = ctk.CTkLabel(root, text="", font=ctk.CTkFont(size=12, weight="bold"))
    bmi_text.grid(row=0, column=0, columnspan=3, pady=5, sticky="ew") # 스위치 공간 확보 위해 columnspan=3
    bmi_text.configure(anchor="center")

    # 테마 변경 스위치 (오른쪽 상단)
    theme_switch = ctk.CTkSwitch(master=root, text="다크 모드",
        variable=theme_state_var,
        onvalue=1, offvalue=0,
        command=on_theme_switch_toggle)
    theme_switch.grid(row=0, column=3, padx=10, pady=5, sticky="ne") # ne = north-east (오른쪽 상단)

    # 입력 필드 레이블 및 엔트리
    ctk.CTkLabel(root, text="키(cm):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    height_entry = ctk.CTkEntry(root)
    height_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    height_entry.configure(justify="center")

    ctk.CTkLabel(root, text="체중(kg):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    weight_entry = ctk.CTkEntry(root)
    weight_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    weight_entry.configure(justify="center")

    ctk.CTkLabel(root, text="나이:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    age_entry = ctk.CTkEntry(root)
    age_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
    age_entry.configure(justify="center")

    # 운동 수준 선택 옵션 메뉴
    ctk.CTkLabel(root, text="운동 수준:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    level_var = ctk.StringVar(value="초급")
    level_optionmenu = ctk.CTkOptionMenu(root, variable=level_var, values=["초급", "중급", "고급"])
    level_optionmenu.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    # 운동 목표 선택 옵션 메뉴
    ctk.CTkLabel(root, text="운동 목표:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    goal_var = ctk.StringVar(value="근육 증가")
    goal_optionmenu = ctk.CTkOptionMenu(root, variable=goal_var, values=["근육 증가", "지구력 향상", "체중 감량"])
    goal_optionmenu.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

    # 운동 요일 선택 체크 버튼
    # 운동 요일 라벨
    ctk.CTkLabel(root, text="  운동할 요일:").grid(row=6, column=0, padx=10, pady=5, sticky="nw")

    # 요일 선택 프레임
    day_frame = ctk.CTkFrame(root)
    day_frame.grid(row=6, column=1, columnspan=3, sticky="ew", padx=10, pady=5)

    day_vars = {}
    days = ["월", "화", "수", "목", "금", "토", "일"]

    # 전체 선택 체크박스 변수
    select_all_var = ctk.IntVar()

    def toggle_all_days():
        state = select_all_var.get()
        for var in day_vars.values():
            var.set(state)

    # 요일 체크박스 배치
    for i, day in enumerate(days):
        var = ctk.IntVar()
        chk = ctk.CTkCheckBox(day_frame, text=day, variable=var)
        row = i // 4   # 0~3: row=0, 4~6: row=1
        col = i % 4    # 열 위치
        chk.grid(row=row, column=col, sticky="w", padx=10, pady=2)
        day_vars[day] = var

    # 전체 선택 체크박스 (마지막 열에)
    select_all_chk = ctk.CTkCheckBox(day_frame, text="전체 선택", variable=select_all_var, command=toggle_all_days)
    select_all_chk.grid(row=1, column=3, sticky="w", padx=10, pady=2)



    # 관절 통증 선택 체크 버튼
    ctk.CTkLabel(root, text="     통증 부위:").grid(row=7, column=0, padx=10, pady=5, sticky="nw")
    pain_frame = ctk.CTkFrame(root)
    pain_frame.grid(row=7, column=1, columnspan=3, sticky="ew", padx=10, pady=5)

    elbow_pain_var = ctk.IntVar()
    ctk.CTkCheckBox(pain_frame, text="팔꿈치", variable=elbow_pain_var).grid(row=0, column=0, sticky="w", padx=10, pady=2)
    shoulder_pain_var = ctk.IntVar()
    ctk.CTkCheckBox(pain_frame, text="어깨", variable=shoulder_pain_var).grid(row=0, column=1, sticky="w", padx=10, pady=2)
    wrist_pain_var = ctk.IntVar()
    ctk.CTkCheckBox(pain_frame, text="손목", variable=wrist_pain_var).grid(row=0, column=2, sticky="w", padx=10, pady=2)
    knee_pain_var = ctk.IntVar()
    ctk.CTkCheckBox(pain_frame, text="무릎", variable=knee_pain_var).grid(row=1, column=0, sticky="w", padx=10, pady=2)
    ankle_pain_var = ctk.IntVar()
    ctk.CTkCheckBox(pain_frame, text="발목", variable=ankle_pain_var).grid(row=1, column=1, sticky="w", padx=10, pady=2)
    back_pain_var = ctk.IntVar()
    ctk.CTkCheckBox(pain_frame, text="허리", variable=back_pain_var).grid(row=1, column=2, sticky="w", padx=10, pady=2)

    # 하기 싫은 부위 선택 체크 버튼
    ctk.CTkLabel(root, text="  제외할 부위:").grid(row=8, column=0, padx=10, pady=5, sticky="nw")
    exclude_frame = ctk.CTkFrame(root)
    exclude_frame.grid(row=8, column=1, columnspan=3, sticky="ew", padx=10, pady=5)
    exclude_chest_var = ctk.IntVar()
    ctk.CTkCheckBox(exclude_frame, text="가슴", variable=exclude_chest_var).grid(row=0, column=0, sticky="w", padx=10, pady=2)
    exclude_back_var = ctk.IntVar()
    ctk.CTkCheckBox(exclude_frame, text="등", variable=exclude_back_var).grid(row=0, column=1, sticky="w", padx=10, pady=2)
    exclude_legs_var = ctk.IntVar()
    ctk.CTkCheckBox(exclude_frame, text="하체", variable=exclude_legs_var).grid(row=0, column=2, sticky="w", padx=10, pady=2)
    exclude_shoulders_var = ctk.IntVar()
    ctk.CTkCheckBox(exclude_frame, text="어깨", variable=exclude_shoulders_var).grid(row=1, column=0, sticky="w", padx=10, pady=2)
    exclude_abs_var = ctk.IntVar()
    ctk.CTkCheckBox(exclude_frame, text="복부", variable=exclude_abs_var).grid(row=1, column=1, sticky="w", padx=10, pady=2)
    exclude_fullbody_var = ctk.IntVar()
    ctk.CTkCheckBox(exclude_frame, text="전신 (ex.버피 등등)", variable=exclude_fullbody_var).grid(row=1, column=2, sticky="w", padx=10, pady=2)

    # 버튼 프레임 (운동 계획 생성, 초기화, 운동 하는 방법)
    button_frame = ctk.CTkFrame(root)
    button_frame.grid(row=9, column=0, columnspan=4, pady=10, padx=10, sticky="ew")

    # 세 개의 버튼이 공간을 균등하게 차지하도록 컬럼 가중치 설정
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1) # 새 버튼을 위해 컬럼 추가

    generate_button = ctk.CTkButton(button_frame, text="운동 계획 생성", command=lambda: generate_workout(
        height_entry, weight_entry, age_entry, level_var, goal_var, day_vars,
        elbow_pain_var, shoulder_pain_var, wrist_pain_var, knee_pain_var,
        ankle_pain_var, back_pain_var, bmi_text, result_text,
        exclude_chest_var, exclude_back_var, exclude_legs_var,
        exclude_shoulders_var, exclude_abs_var, exclude_fullbody_var
    ))
    generate_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")

    reset_button = ctk.CTkButton(button_frame, text="초기화", command=lambda: reset_fields(
        height_entry, weight_entry, age_entry, level_var, goal_var, day_vars,
        elbow_pain_var, shoulder_pain_var, wrist_pain_var, knee_pain_var,
        ankle_pain_var, back_pain_var, result_text, bmi_text,
        exclude_chest_var, exclude_back_var, exclude_legs_var,
        exclude_shoulders_var, exclude_abs_var, exclude_fullbody_var
    ))
    reset_button.grid(row=0, column=1, padx=5, sticky="ew") # padx 조정

    # 운동 하는 방법 버튼 추가
    # Replace "YOUR_URL_HERE" with the actual URL you want to open.
    how_to_button = ctk.CTkButton(button_frame, text="운동 하는 방법", command=lambda: open_local_html_file("https://youteddy.github.io/exercise_website/"))
    how_to_button.grid(row=0, column=2, padx=(5, 0), sticky="ew") # 새 컬럼에 배치

    # 결과 출력 텍스트 박스
    result_text = ctk.CTkTextbox(root, height=30) # height는 줄 수가 아닌 픽셀일 수 있습니다.
    result_text.grid(row=10, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1) # 스위치가 있는 열
    root.grid_rowconfigure(10, weight=1)

    # 반환 값은 기존과 동일
    return height_entry, weight_entry, age_entry, level_var, goal_var, day_vars, \
        elbow_pain_var, shoulder_pain_var, wrist_pain_var, knee_pain_var, \
        ankle_pain_var, back_pain_var, bmi_text, result_text, \
        exclude_chest_var, exclude_back_var, exclude_legs_var, \
        exclude_shoulders_var, exclude_abs_var, exclude_fullbody_var, root