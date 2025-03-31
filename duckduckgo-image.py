import os
import requests
import re
from duckduckgo_search import DDGS

def safe_filename(filename):
    # 파일명에 사용할 수 없는 문자를 밑줄(_)로 교체
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def download_images(query, num_images=10, save_dir="images"):
    os.makedirs(save_dir, exist_ok=True)
    
    with DDGS() as ddgs:
        results = ddgs.images(query, max_results=num_images)
        
        for i, result in enumerate(results):
            image_url = result["image"]
            try:
                response = requests.get(image_url, stream=True)
                response.raise_for_status()
                
                # 파일 확장자 추출 (URL에서 확장자를 안전하게 가져옴)
                # 확장자가 없거나 비정상적으로 길 경우 기본값 사용
                file_ext = "jpg"  # 기본 확장자
                
                # URL에서 확장자 추출 시도
                url_parts = image_url.split(".")
                if len(url_parts) > 1:
                    possible_ext = url_parts[-1].split("?")[0].split("/")[0]
                    # 일반적인 이미지 확장자 길이는 3-4글자
                    if 2 <= len(possible_ext) <= 4 and possible_ext.isalnum():
                        file_ext = possible_ext
                
                # 안전한 파일명 생성
                safe_query = safe_filename(query)
                file_name = f"{safe_query}_{i}.{file_ext}"
                file_path = os.path.join(save_dir, file_name)
                
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                        
                print(f"Downloaded: {file_path}")
                
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {image_url}: {e}")
                
    print(f"Image download completed. Attempted to download {num_images} images.")

if __name__ == "__main__":
    search_query = "연예인 마스크"  # 검색할 키워드
    num_images = 100  # 다운로드할 이미지 수 (2000에서 조정)
    download_images(search_query, num_images=num_images)