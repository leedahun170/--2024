#github
import cv2
import mediapipe as mp

# Mediapipe 초기화
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils


# 웹캠 열기
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # 성능 향상을 위해 이미지를 쓰기 전에 BGR에서 RGB로 변환합니다.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 이미지의 플래그를 쓰기 금지로 설정합니다.
    image.flags.writeable = False
    
    # 이미지 처리
    results = face_mesh.process(image)
    
    # 이미지를 쓰기 가능으로 다시 설정합니다.
    image.flags.writeable = True
    
    # 이미지를 RGB에서 BGR로 다시 변환합니다.
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # 얼굴 메시 그리기
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1))
            h, w, _ = image.shape
            landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in face_landmarks.landmark]

            # 바운딩 박스 계산
            x_min = min(landmarks, key=lambda x: x[0])[0]
            y_min = min(landmarks, key=lambda x: x[1])[1]
            x_max = max(landmarks, key=lambda x: x[0])[0]
            y_max = max(landmarks, key=lambda x: x[1])[1]

            # 바운딩 박스 그리기
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

            face_width = x_max - x_min
            face_height = y_max - y_min
            face_area = face_width * face_height

            cv2.putText(image, f'Area: {face_area}', (x_min, y_min), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)
        
            # 바운딩 박스 그리기
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 1)

            # 코 끝 점 시각화
            if len(face_landmarks.landmark) > 1:
                left_pupil_x = int(face_landmarks.landmark[1].x * image.shape[1])
                left_pupil_y = int(face_landmarks.landmark[1].y * image.shape[0])
                cv2.circle(image, (left_pupil_x, left_pupil_y), 5, (0, 255, 255), -1)  # 코 끝점을 노란색으로 표시
                cv2.putText(image, f'Left Pupil: ({left_pupil_x}, {left_pupil_y})', (left_pupil_x, left_pupil_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv2.LINE_AA)
                print(f'nose: ({left_pupil_x}, {left_pupil_y})')  # 콘솔에 출력
            
        
    # 결과 이미지 출력
    cv2.imshow('MediaPipe FaceMesh', image)
    
    # ESC 키를 누르면 루프를 종료
    if cv2.waitKey(5) & 0xFF == 27:
        break

# 웹캠과 모든 창 닫기
cap.release()
cv2.destroyAllWindows()

print(face_area,left_pupil_x,left_pupil_y)
