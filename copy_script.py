# 흔히 폴더 별로 카테고리 라벨링 되어 있는 데이터셋을 위해
# 지정한 경로의 모든 하위 디렉토리의 이미지들을 한 폴더에 복사



import os
import shutil
from pathlib import Path
import argparse

def collect_images(source_dir, target_dir, extensions=None):
    """
    특정 디렉토리와 그 하위 디렉토리에 있는 모든 이미지 파일을 대상 디렉토리로 복사합니다.
    
    Args:
        source_dir (str): 이미지를 검색할 원본 디렉토리 경로
        target_dir (str): 이미지를 복사할 대상 디렉토리 경로
        extensions (list, optional): 복사할 이미지 파일 확장자 목록. 기본값은 ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    
    Returns:
        int: 복사된 이미지 파일 수
    """
    # 기본 이미지 확장자 설정
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    
    # 대상 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"대상 디렉토리 생성됨: {target_dir}")
    
    copied_count = 0
    duplicate_count = 0
    error_count = 0
    
    # 원본 디렉토리와 모든 하위 디렉토리 순회
    for root, _, files in os.walk(source_dir):
        for file in files:
            # 파일 확장자가 지정된 확장자 목록에 있는지 확인
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in extensions:
                source_path = os.path.join(root, file)
                
                # 대상 경로 생성
                # 파일명 충돌을 피하기 위해 하위 디렉토리 이름을 접두사로 추가
                rel_path = os.path.relpath(root, source_dir)
                if rel_path != '.':
                    # 특수문자를 언더스코어로 변경
                    prefix = rel_path.replace('/', '_').replace('\\', '_').replace(' ', '_')
                    target_filename = f"{prefix}_{file}"
                else:
                    target_filename = file
                
                target_path = os.path.join(target_dir, target_filename)
                
                # 이미 파일이 존재하고 내용이 다른 경우 번호를 추가하여 새 이름 생성
                counter = 1
                base_name, ext = os.path.splitext(target_filename)
                while os.path.exists(target_path):
                    if os.path.getsize(source_path) == os.path.getsize(target_path):
                        # 파일 크기가 같으면 중복으로 간주하고 복사하지 않음
                        print(f"중복 파일 건너뜀: {source_path} -> {target_path}")
                        duplicate_count += 1
                        break
                    target_path = os.path.join(target_dir, f"{base_name}_{counter}{ext}")
                    counter += 1
                
                # 새 파일이거나 다른 내용의 파일인 경우 복사
                if not os.path.exists(target_path):
                    try:
                        shutil.copy2(source_path, target_path)
                        print(f"파일 복사됨: {source_path} -> {target_path}")
                        copied_count += 1
                    except Exception as e:
                        print(f"오류: {source_path} 복사 실패 - {str(e)}")
                        error_count += 1
    
    print(f"\n작업 완료!")
    print(f"복사된 파일: {copied_count}")
    print(f"중복 건너뜀: {duplicate_count}")
    print(f"오류 발생: {error_count}")
    
    return copied_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='여러 디렉토리에서 이미지 파일을 수집하여 한 곳에 복사합니다.')
    parser.add_argument('source_dir', help='이미지를 검색할 원본 디렉토리 경로')
    parser.add_argument('target_dir', help='이미지를 복사할 대상 디렉토리 경로')
    parser.add_argument('--extensions', nargs='+', help='복사할 이미지 파일 확장자 (예: .jpg .png)')
    
    args = parser.parse_args()
    
    # 확장자가 지정된 경우 처리
    extensions = None
    if args.extensions:
        extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in args.extensions]
    
    collect_images(args.source_dir, args.target_dir, extensions)