# stayWefolio
![staywefolio_logo (1)](https://user-images.githubusercontent.com/66218824/97653516-4fc1ed00-1aa4-11eb-9566-2defcbfa8405.png)
- 팀명 : stayWefolio
- 팀원 : 신은선(Product Manager), 김지훈, 민지연, 김보라, 서수연

## 프로젝트 소개
 숙박 예약 사이트인 stayfolio의 주요 기능을 구현하였습니다. 
 
### 주요기능 
- slick slider 라이브러리를 이용한 슬라이더 기능
- 동적 라우팅을 이용한 페이지 이동 기능
- 로그인/회원가입 기능
- 달력 기능 
- 예약 사항에 따른 금액 계산 기능
- 예약 및 예약 확인 기능
- google map API를 이용한 지도 기능

## 기술스택
### front-end
- React
- Javascript
- HTML, SASS
- CRA, npm
- git
- prettier
- ESLint
- trello
![staywefoliotrello](https://user-images.githubusercontent.com/66218824/97659837-56a42c00-1ab3-11eb-9580-b9c7a41123ca.png)

### back-end
- Python
- Django
- MySQL

### 추가 설치 라이브러리
- slick
- react-router
- node-sass
- react-daterangepicker
- google-map-react
- font-awesome

## 영상
- 메인 화면
![staywefolioscreenshot](https://user-images.githubusercontent.com/66218824/97659783-34121300-1ab3-11eb-9c92-80319daab3cf.png)
- 유튜브
 : https://youtu.be/qz6dKgsI0Ds

## 멤버소개

1. 신은선
- Role : Team Leader
- Position : Front-end
- Stack : React / Java Script / Sass / Router 
- Works : 
 1) 라이브러리와 CSS를 이용한 디자인 구현
 2) component 구현과 관련 AP! 연결
 - 상품리스트 나열 페이지 및 예약 페이지 구현
 - 상품리스트 페이지 - 상품 정보 나열
 - 검색 필터 기능 - 조건 선택에 따른 필터링 기능
 - pagination - query string을 이용한 paging 기능
 - 달력 라이브러리를 이용한 날짜 계산 및 금액 산출 기능
 - 유동라우터를 이용한 화면 전환 기능
 ---
2. 김보라
- Role : Team Member
- Position : Front-end
- Stack : React
- Works :
1) 라이브러리와 css를 이용한 디자인 구현
2) 메인 페이지, booking detail 페이지, 예약 확인 페이지 컴포넌트화 및 API 연결
3) Main page
 -  메인 상단 배너 - slick slider 사용하여 배너 이미지 자동 슬라이드 구현
4) Booking Detail
 - slick slider 사용하여 각 방 정보 슬라이딩 기능 구현
 - Google map react API 사용하여 호텔 위치 보여주는 지도 구현
5) 예약 상세 페이지
 - 예약이 완료되면 해당 정보가 담긴 API를 받아와 화면에 띄워주는 예약 확인 페이지 구현
6) 네비게이션바 로그인/로그아웃
 - 로컬 스토리지에 저장된 토큰의 유무에 따라 로그인/로그아웃 시 네비게이션 바 문구 변경 기능 구현
 ---
3. 민지연
- Role : Team Member
- Position : Front-end
- Stack : React / Javascript / Sass / Router
- Works : 
1) 디자인을 바탕으로 Component 설계CSS를 이용한 디자인 구현
2) Component 구현과 관련 API 연결
3) 로그인 - 조건식에 따른 경고 메세지 구현, 로그인 활성화 반영
4) 회원가입 - 조건식에 따른 경고 메세지 구현, toggle 버튼을 이용한 펼치기/숨기기 기능 구현, 전체동의 checkbox 자동 반영
5) Booking main - API로 받은 이미지, 텍스트 데이터 반영
6) 예약페이지 약관동의 - contents data로 분리 및 관리, map methods를 사용하여 data 렌더
---
4. 서수연
 - Role : team member
 - Position : front-end
 - Stack : React
 - Works : Navigation, Footer, Resevervation
1) CRA를 이용한 초기세팅 진행
2) Layout 및 sass 구현
3) component 구현과 관련 API 연결
 - router를 이용한 Link 연결
 - query string을 이용한 가격 정보 산출 구현
 - 추가옵션 선택에 따른 가격 총합 산출 변경 구현
 - 인원 추가에 따른 가격 변경 구현
 - 체크인, 체크아웃 날짜에 따른 일박 나타내기 구현
---
5. 김지훈
- Role : team member
- Position : back-end
- Stack : Django, Python
- Works : 
1) 데이터 모델링을 통한 데이터베이스 구축
2) API 구현
- 회원가입 - 정규표현식을 활용한 회원가입 validation 및 bcrypt로 비밀번호 암호화
- 로그인 - jwt를 사용하여 로그인 후 token 발급
- 호텔 리스트 페이지 - 모든 호텔에 대한 정보를 리턴하고, 필터링이 걸리면 그에 맞는 조건의 호텔만 리턴
- 호텔 상세 페이지 - 호텔에 대한 구체적인 정보를 데이터베이스에서 가져오고, 방의 최대 가격과 최소 가격을 계산하여 리턴
- 예약 페이지 - 프론트엔드에서 준 날짜를 기준으로 그 달의 모든 예약일정과 사용자가 지정한 날짜의 가격 합계를 리턴
- 예약 확인 페이지 - 예약 후 예약 id를 통해 사용자의 예약 정보를 리턴하여 사용자가 예약을 확인하는 페이지에 띄워줌
- backend github: https://github.com/wecode-bootcamp-korea/13-stayWefolio-backend
---
![Image from iOS](https://user-images.githubusercontent.com/66218824/97805950-7a769600-1c9c-11eb-8981-dea62d98af94.jpg)
❤stayWefolio팀과 함께해서 너무나 행복했습니다❤
