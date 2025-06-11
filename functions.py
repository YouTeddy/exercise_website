from tkinter import messagebox
import customtkinter as ctk
import webbrowser


# -------------------- 보조 함수 --------------------
def round_to_nearest_5(x):
    """주어진 숫자를 가장 가까운 5의 배수로 반올림합니다."""
    return 5 * round(x / 5)

def calculate_bmi(height, weight):
    """키와 체중을 이용하여 BMI를 계산합니다."""
    if height > 0:
        bmi = weight / ((height / 100) ** 2)
        return bmi
    return None

def format_bmi(bmi):
    """계산된 BMI 값과 분류 결과를 문자열 형태로 반환합니다."""
    if bmi is not None:
        category = ""
        if bmi < 18.5:
            category = "(저체중)"
        elif 18.5 <= bmi < 23:
            category = "(정상 체중)"
        elif 23 <= bmi < 25:
            category = "(과체중)"
        else:
            category = "(비만)"
        return f"BMI: {bmi:.2f} {category}"
    return "BMI 계산 불가"

def calculate_weight(weight, level, age):
    """운동 수준과 나이에 따라 기본 운동 무게를 계산합니다."""
    base_weight = weight * 0.7  # 기본 무게 비율

    # 운동 수준에 따른 무게 조정
    if level == "초급":
        base_weight *= 1.0
    elif level == "중급":
        base_weight *= 1.2
    else:  # 고급
        base_weight *= 1.5

    # 나이에 따른 무게 조정
    if age < 30:
        age_factor = 1.0
    elif age < 50:
        age_factor = 0.9
    elif age < 60:
        age_factor = 0.8
    else:  # 60세 이상
        age_factor = 0.7

    return round_to_nearest_5(base_weight * age_factor)

# -------------------- 주요 기능 함수 --------------------

def open_local_html_file(file_path):
    try:
        webbrowser.open_new_tab(file_path)
    except Exception as e:
        messagebox.showerror("파일 열기 오류", f"HTML 파일을 여는 데 실패했습니다: {e}\n경로를 확인해주세요.")

        
def generate_workout(height_entry, weight_entry, age_entry, level_var, goal_var, day_vars,
    elbow_pain_var, shoulder_pain_var, wrist_pain_var, knee_pain_var,
    ankle_pain_var, back_pain_var, bmi_text, result_text,
    exclude_chest_var, exclude_back_var, exclude_legs_var,
    exclude_shoulders_var, exclude_abs_var, exclude_fullbody_var):
    """사용자 입력에 따라 운동 계획을 생성하고 결과 텍스트 박스에 표시합니다."""
    try:
        # 1. 사용자 입력 값 가져오기
        height = int(height_entry.get())
        weight = int(weight_entry.get())
        age = int(age_entry.get())
        level = level_var.get()
        goal = goal_var.get()
        selected_days = [day for day, var in day_vars.items() if var.get() == 1]
        excluded_muscles = {
            "가슴": exclude_chest_var.get(),
            "등": exclude_back_var.get(),
            "하체": exclude_legs_var.get(),
            "어깨": exclude_shoulders_var.get(),
            "복부": exclude_abs_var.get(),
            "전신": exclude_fullbody_var.get(),
        }

        # 2. 입력 유효성 검사
        if not all([height, weight, age]):
            messagebox.showwarning("경고", "키, 체중, 나이를 모두 입력해주세요!")
            return

        if not selected_days:
            messagebox.showwarning("경고", "하루 이상 선택하세요!")
            return

        # 3. BMI 계산 및 포맷
        bmi_value = calculate_bmi(height, weight)
        bmi_text.configure(text=format_bmi(bmi_value))
        bmi_summary = f"{format_bmi(bmi_value)}, " if bmi_value is not None else ""

        # 4. 기본 운동 무게 계산
        exercise_weight = calculate_weight(weight, level, age)

        # 5. 결과 텍스트 박스 초기화
        result_text.delete("1.0", ctk.END)

        # 6. 관절 통증 여부 확인 및 요약 문자열 생성
        painful_joints = []
        pain_summary = ""
        if elbow_pain_var.get():
            painful_joints.append("팔꿈치")
        if shoulder_pain_var.get():
            painful_joints.append("어깨")
        if wrist_pain_var.get():
            painful_joints.append("손목")
        if knee_pain_var.get():
            painful_joints.append("무릎")
        if ankle_pain_var.get():
            painful_joints.append("발목")
        if back_pain_var.get():
            painful_joints.append("허리")

        if painful_joints:
            pain_summary = f"체크한 부위 통증 고려: {', '.join(painful_joints)}\n"
        
        # 목표 요약 문자열 생성 및 표시
        goal_summary = f"목표: {goal}, {bmi_summary}\n"
        result_text.insert(ctk.END, goal_summary)
        result_text.insert(ctk.END, pain_summary)

        weight_reduction_factor = 0.7  # 통증 시 무게 감소 비율

        # 7. 운동 부위별 운동 목록 및 관련 관절 정보, 자극 부위 정보 추가
        workouts_data = {
            "가슴": {"exercises": [("벤치프레스", "가슴"), ("인클라인 덤벨 프레스", "윗가슴"), ("체스트 플라이 머신", "가슴 바깥쪽")], "joints": ["어깨", "팔꿈치", "손목"], "stretch": ["가슴 스트레칭"]},
            "등": {"exercises": [("데드리프트", "전신, 등 하부"), ("바벨 로우", "등 중앙"), ("랫풀다운", "광배근")], "joints": ["어깨", "팔꿈치", "손목", "허리"], "stretch": ["등 스트레칭"]},
            "하체": {"exercises": [("스쿼트", "대퇴사두근, 둔근"), ("레그프레스", "대퇴사두근, 햄스트링, 둔근"), ("런지", "대퇴사두근, 둔근, 햄스트링")], "joints": ["무릎", "고관절", "발목"], "stretch": ["허벅지 앞/뒤 스트레칭", "종아리 스트레칭"]},
            "어깨": {"exercises": [("오버헤드프레스", "전면, 측면 삼각근"), ("레터럴 레이즈", "측면 삼각근"), ("프론트 레이즈", "전면 삼각근")], "joints": ["어깨", "팔꿈치", "손목"], "stretch": ["어깨 스트레칭"]},
            "복부": {"exercises": [("크런치", "상복근"), ("러시안 트위스트", "외복사근"), ("플랭크", "전신 코어")], "joints": ["허리"], "stretch": ["복부 스트레칭"]},
            "전신": {"exercises": [("버피", "전신"), ("점프 스쿼트", "하체, 심폐"), ("마운틴 클라이머", "전신 코어, 심폐")], "joints": ["어깨", "팔꿈치", "손목", "무릎", "고관절", "발목", "허리"], "stretch": ["전신 스트레칭"]}
        }

        # 8. 운동 부위별 웜업 목록
        warmups = {
            "가슴": ["팔 돌리기", "푸시업 10회"],
            "등": ["밴드 로우", "슈퍼맨 10회"],
            "하체": ["스쿼트 10회", "런지 10회"],
            "어깨": ["숄더 서클", "암 스윙"],
            "복부": ["힙 서클", "고양이-소 자세"],
            "전신": ["가벼운 전신 스트레칭", "제자리 뛰기"]
        }

        # 9. 유산소 운동 목록 (체중 감량 시 추가)
        cardio = [
            "트레드밀 20분",
            "자전거 15분",
            "줄넘기 100회",
            "인터벌 러닝 15분",
            "스텝박스 운동 10분"
        ]

        # 10. 운동 목표에 따른 설정 (운동 부위, 반복 횟수, 세트 수, 식단 추천)
        if goal == "근육 증가":
            muscle_groups_all = ["가슴", "등", "하체", "어깨", "복부"]
            reps, sets, factor = 8, 4, 1.0
            diet_suggestion = (
                "\n\n💪 식단 추천 (근육 증가):\n"
                "- 아침: 오트밀, 계란 스크램블\n"
                "- 점심: 닭가슴살, 현미밥, 채소 샐러드\n"
                "- 저녁: 살코기, 퀴노아, 구운 채소\n"
                "- 간식: 그릭 요거트, 단백질 쉐이크"
            )
        elif goal == "지구력 향상":
            muscle_groups_all = ["전신", "하체", "어깨", "복부"]
            reps, sets, factor = 15, 2, 0.7
            diet_suggestion = (
                "\n\n🏃‍♀️ 식단 추천 (지구력 향상):\n"
                "- 아침: 통곡물 빵, 과일\n"
                "- 점심: 닭가슴살 샌드위치, 채소 샐러드\n"
                "- 저녁: 통곡물 파스타, 해산물, 채소\n"
                "- 간식: 에너지 바, 바나나"
            )
        elif goal == "체중 감량":
            muscle_groups_all = ["전신", "복부", "하체"]
            reps, sets, factor = 12, 3, 0.85
            diet_suggestion = (
                "\n\n🔥 식단 추천 (체중 감량):\n"
                "- 아침: 계란, 통곡물 빵\n"
                "- 점심: 닭가슴살 샐러드, 콩류\n"
                "- 저녁: 구운 생선, 찐 채소\n"
                "- 간식: 과일, 채소 스틱, 저지방 요거트"
            )
        else:  # 기본
            muscle_groups_all = list(workouts_data.keys())
            reps, sets, factor = 10, 3, 1.0
            diet_suggestion = "\n\n🥗 균형 잡힌 식단을 유지하세요."

        # 제외할 부위 필터링
        muscle_groups = [group for group in muscle_groups_all if not excluded_muscles[group]]

        if not muscle_groups:
            messagebox.showwarning("경고", "모든 운동 부위를 제외하셨습니다! 제외 설정을 다시 확인해주세요.")
            return

        # 11. 선택된 요일에 따라 운동 루틴 생성 및 텍스트 박스에 추가
        for i, day in enumerate(selected_days):
            muscle_group_name = muscle_groups[i % len(muscle_groups)]
            muscle_data = workouts_data[muscle_group_name]
            adjusted_weight = round_to_nearest_5(exercise_weight * factor)

            result_text.insert(ctk.END, f"\n📅 {day}요일 – {muscle_group_name} 운동\n")
            result_text.insert(ctk.END, "웜업:\n")
            for warmup in warmups[muscle_group_name]:
                result_text.insert(ctk.END, f" - {warmup}\n")
            result_text.insert(ctk.END, "본 운동:\n")
            for exercise, target_muscle in muscle_data["exercises"]:
                # 특정 관절에 부담이 가는 운동인지 확인하고 무게 조절
                exercise_joints = muscle_data["joints"]
                weight_to_use = adjusted_weight
                reduce_weight = False
                for painful_joint in painful_joints:
                    if painful_joint in exercise_joints:
                        reduce_weight = True
                        break # 하나라도 관련되면 무게 감소

                if reduce_weight:
                    weight_to_use = round_to_nearest_5(adjusted_weight * weight_reduction_factor)
                    result_text.insert(ctk.END, f" - {exercise} ({target_muscle}): {weight_to_use}kg (중량 감소) × {reps}회 × {sets}세트\n")
                else:
                    result_text.insert(ctk.END, f" - {exercise} ({target_muscle}): {weight_to_use}kg × {reps}회 × {sets}세트\n")

            if goal == "체중 감량":
                result_text.insert(ctk.END, f"유산소: {cardio[i % len(cardio)]}\n")

            # 마무리 스트레칭 추가
            result_text.insert(ctk.END, "마무리 스트레칭:\n")
            for stretch in muscle_data["stretch"]:
                result_text.insert(ctk.END, f" - {stretch}\n")

        # 12. 식단 추천 추가
        result_text.insert(ctk.END, diet_suggestion)

    except ValueError:
        messagebox.showerror("입력 오류", "숫자를 정확히 입력해주세요.")

def reset_fields(height_entry, weight_entry, age_entry, level_var, goal_var, day_vars,
    elbow_pain_var, shoulder_pain_var, wrist_pain_var, knee_pain_var,
    ankle_pain_var, back_pain_var, result_text, bmi_text,
    exclude_chest_var, exclude_back_var, exclude_legs_var,
    exclude_shoulders_var, exclude_abs_var, exclude_fullbody_var):
    """입력 필드와 결과 텍스트 박스, 통증 체크박스, 제외 체크박스를 초기화합니다."""
    height_entry.delete(0, ctk.END)
    weight_entry.delete(0, ctk.END)
    age_entry.delete(0, ctk.END)
    level_var.set("초급")
    goal_var.set("근육 증가")
    for var in day_vars.values():
        var.set(0)
    elbow_pain_var.set(0)
    shoulder_pain_var.set(0)
    wrist_pain_var.set(0)
    knee_pain_var.set(0)
    ankle_pain_var.set(0)
    back_pain_var.set(0)
    result_text.delete("1.0", ctk.END)
    bmi_text.configure(text="")
    exclude_chest_var.set(0)
    exclude_back_var.set(0)
    exclude_legs_var.set(0)
    exclude_shoulders_var.set(0)
    exclude_abs_var.set(0)
    exclude_fullbody_var.set(0)