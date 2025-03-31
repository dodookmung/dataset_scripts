import os

def delete_gif_files(directory: str):
    """지정된 디렉토리 내의 모든 .gif 파일을 삭제"""
    if not os.path.exists(directory):
        print(f"경로가 존재하지 않습니다: {directory}")
        return
    
    count = 0
    for filename in os.listdir(directory):
        if filename.lower().endswith(".gif"):
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
                print(f"삭제 완료: {file_path}")
                count += 1
            except Exception as e:
                print(f"삭제 실패: {file_path}, 오류: {e}")
    
    print(f"총 {count}개의 .gif 파일 삭제 완료")

# 사용 예시
directory_path = 'C:\\Users\\dodookmung\\github\\Datasets\\kpop-celeb\\'  # 삭제할 디렉토리 경로 입력
delete_gif_files(directory_path)
