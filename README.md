![image](https://github.com/TAEHOONLIMKOREA/Practice_Flask_Vue/assets/87262811/bda548d3-36b4-4185-a400-808ce2fd7da3)
# 프로젝트 구성
- 먼저 프로젝트명으로 폴더를 만든 후 하위에 frontend와 backend 폴더 구성을 해주어야한다.<br/>
- frontend 폴더는 vue/cli를 이용하여 프로젝트를 생성해 줄 때 만들면 됨 <br/>
  (ex. vue create frontend) <br/>
- 이후 backend 폴더를 만들고 각 서비스 단의 세부 생성 과정은 아래 참고<br/>

### 폴더 구조 예시 사진 
![image](https://github.com/TAEHOONLIMKOREA/Practice_Flask_Vue/assets/87262811/8f4f5459-c9c4-4593-a33b-2bbb7731e9d8)
<hr/>

# backend

## python flask web framework

### vscode에서 python 실행환경 구성
#### 가상환경 설정
- 터미널 창 실행 <br/>
- python -m venv venv <br/>
#### 인터프리터 설정
- [ Ctrl + Shift + P ] 키를 눌러 ">select Interpreter"를 검색해서 선택 <br/>
![image](https://github.com/TAEHOONLIMKOREA/Practice_Flask_Vue/assets/87262811/e3dfa28f-9f1d-4016-9f08-4d36bd249900)

- 생성한 venv가상 환경 이름과 동일한 것을 선택 <br/>
![image](https://github.com/TAEHOONLIMKOREA/Practice_Flask_Vue/assets/87262811/c0d6be6e-3782-4cdf-9482-6a8106bbf731)

- 이후 기존에 열려있던 터미널 창을 닫고, 다시 터미널 창을 열어준다 (Ctrl + Shift + `)
![image](https://github.com/TAEHOONLIMKOREA/Practice_Flask_Vue/assets/87262811/a3df9935-ce23-48e2-ba1b-c6e50244f56f)

<hr/>

# frontend

###  vscode에서 vue 개발환경 구성:
Window 11<br/>
node.js 20.10.0 <br/>
- vue/cli 설치<br/>
(npm install -g @vue/cli) <br/>
(npm이 안되면 yarn 1.xx으로 대체 하여 설치, yarn 설치 방법은 Mac과 Window가 다르니 참고) <br/>

Visual Studio Code<br/>
- Extensions (Vetur, HTML CSS Support, vue 3 snippets)

### 프로젝트 생성 및 실행
 - vue create "프로젝트명" <br/>
 - npm run serve (개발 서버 실행)<br/>

 ## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

# 기타 추가 사항
#### git
- vue를 통해 프로젝트를 생성하면 gitignore가 forntend 폴더 안에 만들어진다. 이것을 .git 폴더가 존재하는 상위 폴더로 옮긴다<br/>
- gitignore 에 (venv/, frontend/dist/) 를 추가한다<br/>
#### pip
- pip freeze > requirements.txt 를 이용하여 패키지 저장목록을 만들어 놓는다
- 설치할 때는 pip install -r requirements.txt 명령어를 이용하면 됨

# frontend와 backend 연동
- 기존의 vue 사용법 바로 npm run serve 명령어를 이용해 개발 서버를 실행시키는 것이 아님
- npm run build 명령어를 이용하여 vue형식의 파일을 html, js, css 파일로 변환 시켜서 flask에서 사용해야함
  
## Edit frontend/vue.config.js
![image](https://github.com/TAEHOONLIMKOREA/Practice_Flask_Vue/assets/87262811/c8102962-cb6b-4dcc-996e-bbe6001d8726)

## Frontend Build
- cd frontend<br/>
- npm run build<br/>

## Edit backend/main.py
![image](https://github.com/TAEHOONLIMKOREA/Practice_Flask_Vue/assets/87262811/8d4e36fd-968d-4f59-9dd9-1179cad347cc)

## Execute & Access
- cd backend<br/>
- python main.py<br/>


