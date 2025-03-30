# 원하는 사이즈로 resize한 이미지를 지정한 폴더 경로에 생성



import os
import time
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
from functools import partial

def resize_image(file_path, output_folder, size=(120, 160)):
    """단일 이미지 리사이징 함수"""
    try:
        # 이미지 열기
        with Image.open(file_path) as img:
            # 출력 파일 경로 생성
            file_name = os.path.basename(file_path)
            output_path = os.path.join(output_folder, file_name)
            
            # 이미지 리사이징 및 저장
            img_resized = img.resize(size)
            img_resized.save(output_path)
            
            return True, file_path
    except Exception as e:
        return False, f"{file_path}: {str(e)}"

def resize_images_in_folder(input_folder, output_folder=None, size=(120, 160), max_workers=None):
    """폴더 내 모든 이미지 리사이징 함수 (멀티프로세싱 활용)"""
    start_time = time.time()
    
    # 출력 폴더가 지정되지 않은 경우, 입력 폴더 내에 'resized' 폴더 생성
    if output_folder is None:
        output_folder = os.path.join(input_folder, 'resized')
    
    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 이미지 파일 목록 구하기
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
    image_files = []
    
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            if ext in image_extensions:
                image_files.append(file_path)
    
    total_images = len(image_files)
    print(f"총 {total_images}개의 이미지 파일을 찾았습니다.")
    
    # 멀티프로세싱으로 이미지 리사이징
    resize_func = partial(resize_image, output_folder=output_folder, size=size)
    
    successful = 0
    failed = 0
    errors = []
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(resize_func, image_files))
        
        for success, result in results:
            if success:
                successful += 1
            else:
                failed += 1
                errors.append(result)
    
    # 처리 결과 출력
    elapsed_time = time.time() - start_time
    print(f"처리 완료: {successful}개 성공, {failed}개 실패")
    print(f"소요 시간: {elapsed_time:.2f}초")
    
    if errors:
        print("\n실패한 파일 목록:")
        for error in errors:
            print(error)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="폴더 내 모든 이미지를 리사이징합니다.")
    parser.add_argument('input_folder', help="입력 이미지 폴더 경로")
    parser.add_argument('--output_folder', help="출력 이미지 폴더 경로 (기본값: 입력폴더/resized)")
    parser.add_argument('--width', type=int, default=120, help="리사이징할 이미지 너비 (기본값: 120)")
    parser.add_argument('--height', type=int, default=160, help="리사이징할 이미지 높이 (기본값: 160)")
    parser.add_argument('--workers', type=int, help="프로세스 수 (기본값: CPU 코어 수)")
    
    args = parser.parse_args()
    
    resize_images_in_folder(
        args.input_folder,
        args.output_folder,
        size=(args.width, args.height),
        max_workers=args.workers
    )



'''
C:\Users\dodookmung\github\Datasets>python image_resize.py C:\Users\dodookmung\github\Datasets\mix_bin --output_folder C:\Users\dodookmung\github\Datasets\resized_mix_bin
총 13619개의 이미지 파일을 찾았습니다.
처리 완료: 13619개 성공, 0개 실패
소요 시간: 10.75초

C:\Users\dodookmung\github\Datasets>python image_resize.py C:\Users\dodookmung\github\Datasets\mix_color --output_folder C:\Users\dodookmung\github\Datasets\resized_mix_color
총 13619개의 이미지 파일을 찾았습니다.
처리 완료: 13619개 성공, 0개 실패
소요 시간: 16.47초

'''