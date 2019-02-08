# zhfhldp1
최초 app flask 서버 관리 

배포 관련 사항 
deloy.json : 도메인, 아이피등 정보
             형식이 JSON이라서 주석 불가 
fabfile.py : 페브릭 작업 내용 기술 
fabgile_comment.py : 주석 버전 
wsgi.py  : entrt파일, 서버 구동시 시작점 
requirements.txt : 서버 구동시 필요한 모듈을 기술 (버전포함)

# 서버 로그 확인
접속로그
>tail -f/var/log/apache2/access.log
> ctrl + c
에러로그 ( 500에러 발생시, interanl server erooro  )
tail -f/var/log/apache2/error.log
> ctrl + c