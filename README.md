# simple-HTTP-comm
- 국민대학교 2023년도 2학년 겨울학기 컴퓨터네트워크 과제
## Overview
- 소켓 통신, HTTP을 이용하여 Client에서 Server읠 txt파일을 관리 생성. 
- CLI형식으로 구현하였으며, 좀 더 명령어에 친숙함을 느끼기 위해, 리눅스 몇개의 명령어(ls, echo, rm, more)을 모방. 

## Requirements
- Python 3.8
- Ubuntu 20.04 LTS

## User Command Explanation
- Client에서 수행할 수 있는 명령어는 총 4개로, echo, ls, more, rm이 있습니다. 아래에 각 명령어 사용법이 있습니다. 
- 해당 명령어는 Linux 명령어 format을 사용했습니다.

### echo
- 설명1 : Server의 DB에 새로운 txt 파일을 하나 생성합니다.
- 예시1 : 내용이 “hello world”인 text1.txt 파일 생성.
- CMD : echo “hello world” > test1 
- 결과1 :
- 설명2 : 만약 DB에 이미 파일이 있다면, 파일 내용을 수정합니다.
- 예시2 : 내용이 “hello world”인 text1.txt 파일의 내용이 “hi”로 변경.
- CMD : echo “hi” > test1
- 결과2 :
### ls
- 설명 : DB에 있는 file list을 출력합니다.
- 예시 : DB에 있는 날짜순(오름차순)으로 정렬된file list가 response온다. Client는 출력.
- CMD : ls
- 결과 :

### more
- 설명 : 파일의 내용을 출력합니다.
- 예시 : sunwoo.txt의 내용인 “20203039 Kim Sun Woo”을 Client에서 출력.
- CMD : more test1
- 결과 :
### rm
- 설명 : 입력한 하나의 파일을 제거합니다.
- 예시 : DB에 있는 file “test1.txt”을 제거한다. 
- CMD : rm test1
- 결과 : 

