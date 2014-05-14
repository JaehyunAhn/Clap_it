#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <time.h>

#define BUFSIZE 100

// socket error handling
void error_handling(char *message);
// for timestamp
char* timeToString(struct tm *t);

int main(int argc, char **argv)
{
	// socket
	int sock;
	pid_t pid;
	char message[BUFSIZE];
	char stamp[BUFSIZE];
	int str_len, recv_len, recv_num;
	struct sockaddr_in serv_addr;

	// time.h
	struct tm *t;
	time_t timer;

	if(argc != 3)
	{
		printf("Usage: %s <IP> <port>\n", argv[0]);
		exit(1);
	}

	sock = socket(PF_INET, SOCK_STREAM, 0);
	memset(&serv_addr, 0, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = inet_addr(argv[1]);
	serv_addr.sin_port = htons(atoi(argv[2]));

	if(connect(sock, 
				(struct sockaddr*)&serv_addr, 
							sizeof(serv_addr)) == -1)
	{
		error_handling((char*)"connect() error!");
	}

	pid = fork();
	if(pid == 0)
	{
		while(1)
		{
			fputs("전송할 메시지를 입력 하세요.(q to quit): """, 
					stdout);
			fgets(message, BUFSIZE, stdin);
			timer = time(NULL);		// get a current time
			t = localtime(&timer);	// struct
			
			if(!strcmp(message, "q\n"))
			{
				shutdown(sock, SHUT_WR);
				close(sock);
				exit(0);
			}

			// cat strings
			strcat(stamp, timeToString(t));
			strcat(stamp, message);
			write(sock, stamp, strlen(stamp)); 
			// send [timestamp]: message
			memset(stamp,NULL,BUFSIZE);
		}
	}
	else
	{
		while(1)
		{
			int str_len = read(sock, message, BUFSIZE);
			if(str_len == 0)
			{
				exit(0);
			}
			message[str_len] = 0;
			printf("서버로부터 전송된 메시지: %s\n", message);
		}
	}

	close(sock);
	return 0;
}

void error_handling(char *message)
{
	fputs(message, stderr);
	fputc('\n', stderr);
	exit(1);
}

char* timeToString(struct tm *t){
	static char s[20];
	sprintf(s, "[%04d-%02d-%02d %02d:%02d:%02d]: ",
			t->tm_year + 1900, t->tm_mon + 1, t->tm_mday,
			t->tm_hour, t->tm_min, t->tm_sec
		   );
	return s;
}
