# HEVEN_AutonomousCar_2017 (HEHE)
위 코드는 2017.05.19 예선 / 2017.05.20 본선으로 열린 '2017 KASA 국제 대학생 자율주행 대회' 를 진행한 프로젝트 결과입니다. <br><br>

|학교|성균관대학교 (Sungkyunkwan Univ.)| 
|:--------|:--------:|
|**소속 동아리**|HEVEN (Hybrid Electronic Vehicle ENgineer)| 
|**수상**|**은상 (2nd prize)**| 
|**팀장**|나윤서 (Na Yoonseo)| 
|**팀원**|김동민 <br>장준배 <br>박지환 <br>김태하 <br>이충환 <br>김학준 <br>양호준 <br>이종국| 
|**차명**|HeHe(헤븐엔 헤븐카)| 

This project is on purpose to make out entire code for '2017 International graduate student, Self-Driving Car Competition'(held on 2017.05.19-20). 

The name of the Car was HeHe(It means HevenCar for Heven. Because our crew's name was Heven).

As team leader, I prepared the competition with our HeHe Car and 8 people of team member. 

With this code, our team got 2nd place at the competition.

# Outline
## Architecture
```
Integrated_Main_Code.py
├ Vision_.py
│ 
├ Steering_.py
│ 
├ Localization_.py
│ 
└ Goal_selection_.py
```

## Role Structure
|Category|Role|Code|Developer|
|:--------|:--------|:--------|:-----------:|
|**Vision**|Lane Tracing|```Vision_.py```|나윤서|
|"|Image Processing|```Vision_.py```|장준배|
|"|Parking|```Vision_.py```|김태하|
|"|Sign Detect|```Vision_.py```|이충환<br>김학준|
|**Planning**|Path Planning|```Goal_selection_.py```|양호준|
|"|LiDAR|```Localization```|김동민|
|"|Localization|```Localization```|김동민<br>이종국|
|**Control**|Car Speed/Steering Control|```Steering_.py```|박지환|
* Project Design & Management: 나윤서

# Development
## Vehicle
### 외장 제작
* 외장 제작을 위해 CAD 로 차량 외장을 역설계 진행  
<img src="https://user-images.githubusercontent.com/35250492/110467036-dacd8680-8119-11eb-8af3-d3d588813009.png" width="500">
<br>
* 외장설계를 바탕으로 PC를 덮을 커버외장 설계
<img src="https://user-images.githubusercontent.com/35250492/110467039-db661d00-8119-11eb-9e06-638ce0b2c5ef.png" width="500">  
<br>
* 몰드 제작 후 FRP 제작  
<img src="https://user-images.githubusercontent.com/35250492/110467741-b6be7500-811a-11eb-8fdf-4aaae04dbc25.png" width="500">  
<img src="https://user-images.githubusercontent.com/35250492/110467587-8c6cb780-811a-11eb-9c50-1a5048fefc98.png" width="500">  
<br>
* 완성  
<img src="https://user-images.githubusercontent.com/35250492/110467929-f2593f00-811a-11eb-96d1-ff9a70a1945b.png" width="500">  



# Competition 결과
## prize
**Ranked 2nd (Sliver Prize)**  
<img src="https://user-images.githubusercontent.com/35250492/110468814-25500280-811c-11eb-8004-636d81aee30c.png" width="500">

## Result
[대회 영상 2:19 부터](https://youtu.be/0pAzOlpB0sQ?t=139)
<br>
|Mission|Competition|Pass/Fail|R/M|
|:--------:|:--------:|:--------:|:--------:|
|**횡단보도**|예선|Pass| |
|"|본선|Pass| |
|**협로구간**|예선|Pass| |
|"|본선|Pass| |
|**동적장애물**|예선|Pass| |
|"|본선|Fail| 본선과 예선 시간이 달라, <br>햇빛 조도에 따라 Image 다르게 인식 <br>(햇빛조도 변경에 따른 이미지 처리 필요)|
|**정적장애물**|예선|Pass| |
|"|본선|Pass| |
|**곡선코스**|예선|Pass| |
|"|본선|Pass| |
|**U턴**|예선|Pass| |
|"|본선|Fail|U턴 바깥 차선 5cm 침범|
|**자동주차**|예선|Fail|차선 침범으로 주차|
|"|본선|Fail|"|

## Report
[최종_결과_보고서](https://github.com/jungAcat/HEVEN_AutonomousCar_2017/files/6108269/WE-UP.docx)  


# The End
<img src="https://user-images.githubusercontent.com/35250492/110469023-719b4280-811c-11eb-8fc0-312c9755f2cb.jpg" width="500">  
<img src="https://user-images.githubusercontent.com/35250492/110469046-7829ba00-811c-11eb-87fe-1b8f53267837.jpg" width="500">  
  

