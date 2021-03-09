# HEVEN_AutonomousCar_2017 (HEHE)
위 코드는 2017.05.18 예선 / 2017.05.19 본선으로 열린 '2017 KASA 국제 대학생 자율주행 대회' 를 진행한 프로젝트 결과입니다. <br><br>

|학교|성균관대학교 (Sungkyunkwan Univ.)| 
|:--------|:--------|
|소속 동아리|HEVEN (Hybrid Electronic Vehicle ENgineer)| 
|수상|은상 (2nd prize)| 
|팀장|나윤서 (Na Yoonseo)| 
|팀원|김동민 <br>장준배 <br>박지환 <br>김태하 <br>이충환 <br>김학준 <br>양호준 <br>이종국| 
|차명|HeHe(헤븐엔 헤븐카)| 

This project is on purpose to make out entire code for '2017 International graduate student, Self-Driving Car Competition'(held on 20170519). 

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
|**Planning**|Path Planning|```Localization```|양호준|
|"|LiDAR|```Localization```|김동민|
|"|Localization|```Localization```|김동민<br>이종국|
|**Control**|Car Speed/Steering Control|```Steering_.py```|박지환|
* Project Design & Management: 나윤서


# Competition 결과
## prize
## picture
## Report
