import os

# 파일이 있는 폴더 경로를 지정하세요
folder_path = 'C:\\Users\\dodookmung\\github\\Datasets\\kpop-celeb2_bin'

prefix_str = '2_'



# 폴더 내의 모든 파일 이름을 가져옵니다
for filename in os.listdir(folder_path):
    old_path = os.path.join(folder_path, filename)

    # 디렉터리는 건너뜁니다
    if os.path.isfile(old_path):
        new_filename = prefix_str + filename
        new_path = os.path.join(folder_path, new_filename)
        
        os.rename(old_path, new_path)
        print(f'Renamed: {filename} -> {new_filename}')
