import dearpygui.dearpygui as dpg
import os
import cv2
import numpy as np
import json
import math

# 전역 변수
image_texture_id = None  # 이미지 텍스처 ID
selected_points = []  # 클릭한 두 점의 좌표
original_image = None  # 원본 이미지


def load_image_callback():
    """텍스트 필드에서 입력받은 이미지 경로 로드"""
    global image_texture_id, original_image

    # 이미지 경로 가져오기
    image_path = dpg.get_value("image_path_input")
    if not os.path.isfile(image_path):
        dpg.set_value("output_text", "Error: Invalid file path. Please enter a valid image path.")
        return

    # OpenCV로 이미지 읽기
    original_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if original_image is None:
        dpg.set_value("output_text", "Error: Could not load image.")
        return

    # OpenCV 이미지를 RGB로 변환
    image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGBA)

    # 텍스처 데이터 준비
    texture_data = np.array(image, dtype=np.float32) / 255.0
    height, width, channels = texture_data.shape

    # 텍스처 크기와 데이터 크기 확인
    assert texture_data.size == width * height * channels, "Data size does not match texture dimensions!"

    # 기존 텍스처 삭제
    if image_texture_id is not None:
        dpg.delete_item(image_texture_id)

    # 텍스처 생성
    image_texture_id = dpg.add_dynamic_texture(width, height, texture_data.flatten(), parent="texture_registry")

    # 드로잉 레이어에 이미지 추가
    dpg.delete_item("drawing_layer", children_only=True)
    dpg.draw_image(image_texture_id, (0, 0), (width, height), parent="drawing_layer")

    # 출력 메시지 업데이트
    dpg.set_value("output_text", f"Image loaded: {image_path}")


def mouse_click_callback(sender, app_data):
    """이미지 클릭 시 좌표 기록"""
    global selected_points

    # 현재 마우스 위치 가져오기
    mouse_pos = dpg.get_mouse_pos()

    # 클릭 지점에 점 표시
    dpg.draw_circle(mouse_pos, 5, color=(255, 0, 0, 255), fill=(255, 0, 0, 255), parent="drawing_layer")

    # 두 점이 선택되면 벡터 계산
    if len(selected_points) < 2:
        selected_points.append(mouse_pos)
        if len(selected_points) == 2:
            draw_arrow_and_calculate_vector()


def draw_arrow_and_calculate_vector():
    """두 점 사이의 화살표를 그리기 및 벡터 계산"""
    global selected_points

    # 두 점 추출
    p1, p2 = selected_points

    # 화살표 그리기
    dpg.draw_arrow(p2, p1, color=(0, 255, 0, 255), thickness=3, size=10, parent="drawing_layer")

    # 벡터 계산
    vector = (p2[0] - p1[0], p2[1] - p1[1])

    # 방향각 계산
    angle = math.atan2(vector[1], vector[0])  # 라디안 값
    angle_deg = math.degrees(angle)  # 각도로 변환

    # 벡터와 방향각 저장
    save_vector_and_angle(vector, angle_deg)

    # 선택 초기화
    selected_points = []


def save_vector_and_angle(vector, angle_deg):
    """계산된 벡터와 방향각을 JSON 파일로 저장"""
    vector_file_path = "vector.json"
    data = {
        "vector": vector,
        "angle_deg": angle_deg
    }
    with open(vector_file_path, "w") as file:
        json.dump(data, file)
    dpg.set_value("output_text", f"Vector saved: {vector}, Angle: {angle_deg:.2f} degrees")


def save_image_callback():
    """점과 화살표가 그려진 이미지를 저장"""
    global original_image, selected_points

    if original_image is None:
        dpg.set_value("output_text", "Error: No image loaded.")
        return

    # 이미지 복사
    output_image = original_image.copy()

    # 점과 화살표 그리기
    for i, point in enumerate(selected_points):
        cv2.circle(output_image, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1)

    if len(selected_points) == 2:
        p1 = (int(selected_points[0][0]), int(selected_points[0][1]))
        p2 = (int(selected_points[1][0]), int(selected_points[1][1]))
        cv2.arrowedLine(output_image, p1, p2, (0, 255, 0), 3, tipLength=0.2)

    # 이미지 저장
    output_path = "annotated_image.png"
    cv2.imwrite(output_path, output_image)
    dpg.set_value("output_text", f"Annotated image saved to {output_path}")


# DearPyGui 초기화
dpg.create_context()

# 텍스처 레지스트리 생성
with dpg.texture_registry(tag="texture_registry"):
    pass

# GUI 레이아웃
with dpg.window(label="Image Vector Drawer", width=512, height=512):
    dpg.add_text("Enter the image path below and click 'Load Image' to view it.")
    dpg.add_input_text(label="Image Path", tag="image_path_input", hint="Enter image file path here")
    dpg.add_button(label="Load Image", callback=load_image_callback)
    dpg.add_button(label="Save Image", callback=save_image_callback)
    dpg.add_text("", tag="output_text", wrap=500)

    # 드로잉 레이어 생성
    with dpg.drawlist(width=512, height=512, tag="drawing_layer", callback=mouse_click_callback):
        pass

# DearPyGui 실행
dpg.create_viewport(title="Image Vector Drawer", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
