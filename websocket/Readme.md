##현재상황
1. index.html -> openWS(/chat) -> websocket
2. elementById 로 메시지 전달
3. Json으로 ws.send <- index.html
4. index.html -> ip address 제대로 고쳐주어야 연결됨

## 해야할일
0. 받아야 할 자료구조 정리
	* 상태/excgcnt/보낸사람id / 보낸시간/기타정보/메시지(개인정보)
1. 메시지 받기
	룩업테이블에 올리기
	좀 기다리기
	테이블 보면서{
		가능성 계산하기
		if 있다면(match 확률 일정 기준 넘는 모든 녀석들)
			내 상태 커플, 상대 상태 커플로 만듦
			excg count ++
			상대 연락처 받음
	}
	if (내 상태 == 싱글) {

2. 룩업 테이블 보기

https://medium.com/marojuns-android/3a027af7a601
https://medium.com/marojuns-android/84974c7fde3
