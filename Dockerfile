FROM liblouis/liblouis
WORKDIR /home

# 점자 txt 파일 : 호스트 -> 도커 컨테이너로 복사 
COPY input.txt /home/

COPY run.sh /home/run.sh

# 실행 권한 부여
RUN chmod +x /home/run.sh 

# docker시작과 동시에 실행시킬 CMD 명령어 설정
CMD ["/home/run.sh"]