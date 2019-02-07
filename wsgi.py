'''
아파치 서버가 이 파일을 구동하여 flask 가동시킴
여기서는 Flask 객체를 가져와서 참조
'''

import sys 
import os 

# 경로설정 
CUR_DIR = os.getcwd()
# 에러의 출력방향과 동일하게 일반 출력 방향 설정 
sys.stdout = sys.stderr
# path 추가 
sys.path.insert(0, CUR_DIR)

# 서버 가져오기 ( # run이 뭐가 있고 Flask 객체를 가져옴 run.py 9번은 작동을 안함)
from run import app as application
