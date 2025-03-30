# 두 폴더의 경로를 받아서 차집합 파일을 삭제해주는 스크립트트


import os

def get_filenames(folder_path):
    """폴더 내 모든 파일 이름을 집합(set)으로 반환"""
    return set(os.listdir(folder_path))

def delete_extra_files(folder1, folder2):
    """한 폴더에는 있지만 다른 폴더에는 없는 파일을 삭제"""
    files1 = get_filenames(folder1)
    files2 = get_filenames(folder2)
    
    # folder1에는 있지만 folder2에는 없는 파일 삭제
    for file in files1 - files2:
        file_path = os.path.join(folder1, file)
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    
    # folder2에는 있지만 folder1에는 없는 파일 삭제
    for file in files2 - files1:
        file_path = os.path.join(folder2, file)
        os.remove(file_path)
        print(f"Deleted: {file_path}")

if __name__ == "__main__":
    folder1 = "C:\\Users\\dodookmung\\github\\Datasets\\face_crop"  # 첫 번째 폴더 경로 입력
    folder2 = "C:\\Users\\dodookmung\\github\\Datasets\\face_crop_segmentation"  # 두 번째 폴더 경로 입력
    
    delete_extra_files(folder1, folder2)
