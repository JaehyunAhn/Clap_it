/*
 * http://sosal.tistory.com/
 * made by so_Sal
 */


/*
   * 리눅스 기반입니다.
   * TCP/IP AF_INET 외부 네트워크 도메인 기반입니다.
   * fork() 함수를 이용한 다중 프로세스 원리 기반 채팅방입니다.
   * 문자열이 자신이 입력한것인지, server가 입력한 것인지 구분하는 ID는 넣지 않았습니다.
   * exit를 입력하거나 받으면 종료됩니다.
   * 최대로 보낼수있는. 받을수 있는 문자열의 길이는 MAXLINE 메크로를 통하여 정하였습니다.
   * 프로그램의 매개변수는 argv[1]과 argv[2]로, 각각 ip와 port번호를 받습니다.
   * made by sosal. http://sosal.tistory.com/
*/


#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>

#include<arpa/inet.h> // AF_INET 외부 네트워크 도메인
#include<sys/types.h>
#include<sys/socket.h>

#define MAXLINE 511

int main(int argc,char *argv[]){
    int cli_sock;
    struct sockaddr_in serv_addr;
    int datalen;
    pid_t pid;

    char buf[MAXLINE+1];
    int nbytes;

    if(argc != 3){
        printf("Usage : %s <IP> <Port> \n", argv[0]);
        exit(0);
    }

    cli_sock = socket(PF_INET, SOCK_STREAM, 0); //cli_sock을 소켓 파일 서술자로 만듭니다.

    if(cli_sock == -1){
        perror("socket() error\n");
        exit(0);
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(argv[1]); //ip와
    serv_addr.sin_port = htons(atoi(argv[2])); //port의 입력

    if(connect(cli_sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) == -1){ //서버에게 접근 시도
        perror("connect() error\n");
        exit(0);
    }

    if((pid=fork()) ==1){ //다중 프로세스를 위한 fork함수. 자식 프로세스 생성
        perror("fork() error\n");
        exit(0);
    }
    else if(pid == 0) { //자식 프로세스 부분. stdin로 사용자가 입력한 문자를 buf에 저장하여 소켓에다
        while(1){        //write 시스템콜을 이용해 server에게 문자를 보낸다. exit 입력시 종료
            fgets(buf,sizeof(buf),stdin);
            nbytes = strlen(buf);
            write(cli_sock,buf,MAXLINE);
            if(strncmp(buf,"exit",4) == 0){
                puts("Good Bye.");
                exit(0);
            }
        }
        exit(0);

    }
    else if(pid>0){ //부모프로세스. server가 보낸 문자열을 받아 출력한다.
        while(1){    //역시 exit 를 받을시 종료
            if((nbytes = read(cli_sock,buf,MAXLINE)) <0){
                perror("read() error\n");
                exit(0);
            }
            printf("%s",buf);
            if(strncmp(buf,"exit",4) == 0)
                exit(0);
            }
    }

    close(cli_sock);
    return 0;
}
