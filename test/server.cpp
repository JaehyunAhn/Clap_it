/* 현재 다수의 클라이언트로 read는 되는데 broadcast가 안되는 상황
 * broadcast[BUFSIZE]; 있음
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/socket.h>

#define BUFSIZE 100

void error_handling(char *message);     // 에러핸들링
void z_handler(int sig);                // 시그핸들러

int main(int argc, char **argv)
{
	int serv_sock;                  // 서버 디스크립터
	int clnt_sock;                  // 클라이언트 디스크립터
	struct sockaddr_in serv_addr;   // 서버 주소포인터
	struct sockaddr_in clnt_addr;   // 클라이언트 주소포인터

	struct sigaction act;
	unsigned int addr_size;
	int str_len, state;
	pid_t pid;
	char message[BUFSIZE];
	char broadcast[BUFSIZE];


	if(argc != 2) {
		printf("Usage: %s <port>\n", argv[0]);
		printf("Default port is 8000, %s 8000 is working..\n", 
				inet_ntoa(serv_addr.sin_addr));
		argv[1] = (char *)"8000";
	}
	else {
		printf("Port %s is working..\n", argv[1]);
	}

	act.sa_handler = z_handler;
	sigemptyset(&act.sa_mask);      // 시그널 초기화
	act.sa_flags = 0;               // 플래그 초기화

	/* 시그널 핸들러 등록 */
	state = sigaction(SIGCHLD, &act, 0);
	if(state != 0)
	{
		puts("sigaction() error\n");
		exit(1);
	}

	serv_sock = socket(PF_INET, SOCK_STREAM, 0);
	memset(&serv_addr, 0, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_addr.sin_port = htons(atoi(argv[1]));

	if(bind(serv_sock, 
				(struct sockaddr*)&serv_addr, 
							sizeof(serv_addr)) == -1)
	{
		error_handling((char *)"bind() error");
	}
	if(listen(serv_sock, 5) == -1)
	{
		error_handling((char *)"listen() error");
	}

	while(1)
	{
		addr_size = sizeof(clnt_addr);
		clnt_sock = accept(serv_sock, 
							(struct sockaddr*)&clnt_addr, 
								&addr_size);
		if(clnt_sock == -1)
			continue;

		/* 클라이언트와의 연결을 독립적으로 생성 */
		if((pid = fork()) == -1)        // fork 실패 시
		{
			close(clnt_sock);
			continue;
		}
		else if(pid > 0)                // 부모 프로세스인 경우
		{ /*
			printf("[%s]: ", inet_ntoa(clnt_addr.sin_addr)); 
			// Client IP Addr 출력
			puts("Connected");
			close(clnt_sock);
			continue;*/
			close(serv_sock);
			while(1) {
				if((str_len = read(clnt_sock,
								message,
								BUFSIZE)) < 0) {
					printf("read() error!\n");
					exit(-1);
				}
				printf("%s\n", message);
				// same as write(1, message, str_len);
				if(strncmp(message,"exit",4)==0)
					break;
			}
		}
		else                            // 자식 프로세스인 경우
		{
			/*
			close(serv_sock);

			while(1)
			{
				if((str_len = read(clnt_sock, 
								message, 
								BUFSIZE)) == 0)
					break;
				 // 버퍼를 쭉 보면서 가능성 계산
				 // 버퍼가 없거나 가능성이 낮다면 2초 기다렸다가 다시 계산(내 위, 아래 버퍼 검색)
				 // 가능성 높다면 버퍼로부터 상대방 연락처 전송
				 //		write(clnt_sock, "A contact", strlen("A contact"));
				 // 버퍼 삭제
				 
				write(1, message, str_len);
				//fgets(broadcast,sizeof(broadcast),stdin);
				//write(clnt_sock,broadcast, strlen(broadcast));
			}
			puts("Disconnect");
			close(clnt_sock);
			exit(0);
			*/
			while(1) {
				fgets(broadcast,sizeof(broadcast),stdin);
				write(clnt_sock, broadcast, strlen(broadcast));
				if(strncmp(broadcast,"exit",4)==0) {
					puts("Goodbye");
					close(clnt_sock);
					break;
				}
				memset(broadcast,NULL,sizeof(broadcast));
			}
		}
	}
	return 0;
}

void z_handler(int sig)
{
	pid_t pid;
	int ret;

	pid = waitpid(-1, &ret, WNOHANG);
	printf("소멸된 좀비의 프로세스 ID: %d\n", pid);
	printf("리턴 된 데이터: %d\n\n", WEXITSTATUS(ret));
}

void error_handling(char *message)
{
	fputs(message, stderr);
	fputc('\n', stderr);
	exit(1);
}
