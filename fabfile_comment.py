'''
로컬 개발 PC에서 원격 서버의 환경부터~운용까지 모든
세팅을 진행한다.
'''
from fabric.contrib.files import append, exists, sed, put
from fabric.api import local, run, sudo, env
import os 
import json 

# 프로젝트 디렉토리 ( 디렉토리 불러오기)
#print(__file__)
#print(os.path.abspath(__file__ ))
#print(os.path.dirname(os.path.abspath(__file__ )))
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__ ))
print(PROJECT_DIR)
#c:\Users\student\Downloads\py_projects\zhfhldp1 

# 2. 환경변수 로드 
# json.load()  json파일을 읽어서 그 구조를 유지하여 리턴 
envs = json.load( open( os.path.join(PROJECT_DIR,'deploy.json')) )
print(envs)
'''
'REPO_URL': 'https://github.com/zhfhldp/zhfhldp1.', 'PROJECT_NAME': 'zhfhldp1', 
'REMOTE_HOST': 'ec2-52-78-86-72.ap-northeast-2.compute.amazonaws.com', 
'REMOTE_HOST_SSH': '52.78.86.72', 'REMOTE_USER': 'ubuntu'}
'''

# 3. 로드한 환경변수를 상수(변하지 않는)의미로 설정 
REPO_URL    = envs['REPO_URL']
PROJECT_NAME  = envs ['PROJECT_NAME']
REMOTE_HOST    = envs ['REMOTE_HOST']
REMOTE_HOST_SSH  = envs ['REMOTE_HOST_SSH']
REMOTE_USER    = envs  ['REMOTE_USER']

# 4. fabric의 환경변수 env에 필요한 부분 추가 
env.user = REMOTE_USER 
env.hosts = [
    REMOTE_HOST_SSH,
]
# 4-1 pem파일로 로그인 하기 위해 
env.use_ssh_config = True
env.key_filename = 'zhfhldp1.pem' # 동일폴더위치

# 5. 원격지에 세팅될 디렉토리 지정
# /home/ubuntu/first
project_folder = '/home/{}/{}'.format(env.user,PROJECT_NAME)
print(project_folder)

# 6. 리눅스에 설치될 기본 패키지 목록을 정리 
apt_requirements=[
    'curl', #리눅스에서 명령 get,post 가능
    'git',
    'python3-pip',
    'python3-dev',
    'bulid-essential',
    'apache2',
    'libapache2-mod-wsgi-py3',
    'python3-setuptools',
    'libssl-dev',
    'libffi-dev',




]

# 패브릭 구동시 fab 함수명
# 이중에서 _ 함수명은 구동 불가 

'''
작성이 모두 끝난 후 
> fab new initServer 
소스가 변경된 후 
> fab update
'''
# 7. 기본 신규 서버 세팅 함수 
def new_initServer():
    _setup()
    update()

# 7-1. 리눅스 셋업 
def _setup():
    # 리눅스 패키지 업데이트 주소 or 패키지 목록 세팅
    _init_apt() 
    # 필요한 패키지 설치 
    _install_apt_packages( apt_requirements )
    # 가상환경 구축
    _making_virtualenv()
    # 목표: 운영체계에는 가장 기본만 파이썬만 서맃 
    # 프로젝트 별로 필요한 패키지를 설치하여 상호 프로젝트간 영향을 
    # 받지 않게 만드는 방식(가상환경)
    # pip install virtualenv 
    # 가상환경위치로 이동 
    # virtualenv env
    # cd env/ scripts 
    # activate or. activate 
    # 프럼프트가 새로 열림 
    # (env)> pip list 
    # (env)> pip install flask 
    # 구동 
    # C:\~\py_project\env\scripts\python run.py 


# 7-2. apt(우분트상) 패키지를 업데이트 여부 확인 및 업데이트 
def _init_apt():
    yn = input('ubuntu linux update ok?: [y/n]')
    if yn == 'y': # 사용자가 업데이트를 원했다면 
        # sudo => root권한으로 실행할 떄 
        # sudo apt-get update 
        # sudo apt-get upgrade
        sudo('apt-get update && apt-get -y upgrade ')


#7-3 리눅스 상에 필요한 패키지 설치 
def _install_apt_packages( requires ):
    # 설치할 패키지 목록 나열 
    reqs = '' 
    for req in requires:
        reqs += ' ' + req
    # curl git python3-pip.. 이런식으로 문자열이 진행
    # 수행 
    # sudo apt-get install curl 
    sudo('apt-get -y install' + reqs )

# 7-4. 가상환경구축 
def _making_virtualenv(): 
    # 설치 여부 확인 => 파일 여부체크 
    if not exists('~/.virtualenvs')


        # 가상환경 폴더
        # run 구동 => ubuntu 소유 ( 퍼미션 )
        # sudo 구동 => root 소유  ( 퍼미션 )
          
        run('mkdir ~/.virtualenvs')
        #패키지 설치 
        sudo('pip3 install virtualenvwrapper')
        # 환경변수 반영및 쉘(윈도우의 배치) 구동  가상환경 구축 ({} 중괄호붙으면 .format나와얗함)
        cmd =''' 
            "# python virtualenv global setting
            export WORKON_HOME=~/.virtualenvs
            # python location
            export VIRTUALENVWRAPPER_PYTHON="$(command \which python3)"
            # shell 실행 
            source /usr/local/bin/virtualenvwrapper.sh"
        '''
       
        run('echo {} >> ~/.bashrc'.format(cmd) )



# 8. 소스 수정후 서버에 반영 할 때 사용하는 함수 
def update():
    # 8-1 소스를 최신으로 github를 통해 통해서 받는다 
    _git_update()
    # 8-2 가상환경 필요한 패키지 설치 (1회만 수행)
    _virtualenv_update()
    # 8-3 아파치에 가상 호스트를 세팅 (1회만 수행) 
    _virtualhost_make()
    # 8-4 아파치가 프로젝트를 access 할 수 있게 권한 처리 (1회만 수행)
    #                   신규파일에 대한 검토 필요 -> 그냥 매번 수행 
    _grant_apache()
    # 서버 재가동(아파치)
    _restart_apache()

# 8-1 저장소에서 최신 소스로 반영 
def _git_update():
    if exists(project_folder + '/.git'): # 깃트가 존재하면 ㅇ
        # first 폴더로 이동 그리고 저장소로부터 fetch를 해서 최신 정보를 가져온다ㅣ 
        run('cd %s && git fetch' % (project_folder,))
    else: # 깃트가 존재하지 않으면 
        # 저장소로부터 최초로 프로젝트를 받아온다.
        run('git clone %s %s' % (REPO_URL, project_folder))
    # 기트의 커밋된 로그를 최신으로 한개 가져온다 그것의 번호를 리턴 
    # local : git log -n --format=%H => 238473278223543
    current_commit = local("git log -n 1 --format=%H", capture=True)
    # first 폴더로 이동 그리고 reset --hard 238473278223543
    # 최신 커밋사항으로 소스 반영 
    run('cd %s && git reset --hard %s' % (project_folder, current_commit))
# 8-2 본 프로젝트에 해당되는 가상환경 구축 
#    그환경에 그 프로젝트에서 사용하는 모듈설치
def _virtualenv_update():
    #/home/ubunt/.virtualenvs/first 라는 가상환경 위치
    virtualenv_folder = project_folder + '/../.virtualenvs/{}'.format(PROJECT_NAME)
    
    #/home/ubunt/.virtualenvs/first/bin/pip가 존재하지 않으면
    if not exists(virtualenv_folder + '/bin/pip'):
        # /home/ubunt/.virtualenvs로 이동하고 그리고 
        # virtualenv first 가상환경 하나 샟성 
        run('cd /home/%s/.virtualenvs && virtualenv %s' % (env.user, PROJECT_NAME))
    
    #상관없이 수행
    #/home/ubunt/.virtualenvs/first//bin/pip install 
    #    -r /home/ubunt/first/requirements.txt
    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, project_folder
    ))

def _ufw_allow():
    # ufw 에서 80포트를 오픈
    sudo("ufw allow 'Apache Full'") 
    #리로드
    sudo("ufw reload")
#8-3 아파치 서버와 flask로 구성된 파이썬 서버간의 연동파트(핵심)
def _virtualhost_make():
    script = """'<VirtualHost *:80>
    ServerName {servername}
    <Directory /home/{username}/{project_name}>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    WSGIDaemonProcess {project_name} python-home=/home/{username}/.virtualenvs/{project_name} python-path=/home/{username}/{project_name}
    WSGIProcessGroup {project_name}
    WSGIScriptAlias / /home/{username}/{project_name}/wsgi.py
    
    ErrorLog ${{APACHE_LOG_DIR}}/error.log
    CustomLog ${{APACHE_LOG_DIR}}/access.log combined
    
    </VirtualHost>'""".format(
        username=REMOTE_USER,
        project_name=PROJECT_NAME,
        servername=REMOTE_HOST,
    )

    # 아파치 사이트 목록 설정 파일에 first.conf 파일을 하나 생성해서 둔다
    sudo('echo {} > /etc/apache2/sites-available/{}.conf'.format(script, PROJECT_NAME))
    #반영 
    sudo('a2ensite {}.conf'.format(PROJECT_NAME))

# 8-4 아파치 서버가 파이썬 웹을 액세스 할 수 있게 처리 
def _grant_apache():
    # 파일의 소유주나 소유그룹을 변경하기 위한 리눅스 명령어 
    # 아파치쪽 웹에 소유주와 프로젝트 소유주를 일치시킴 
    sudo('chown -R :www-data ~/{}'.format(PROJECT_NAME))
    # 프로젝트에 폴더의 권한을 775로 변경 
    # 권한(쓰기w 읽기 r 실행x)
    # 775루트, 소유주는 다 사용가능, 누구나 경우는 읽기만 가능 
    sudo('chmod -R 775 ~/{}'.format(PROJECT_NAME))

#8-5 아파치 서버 재가둥
def _restart_apache():
    sudo('service apache2 restart')