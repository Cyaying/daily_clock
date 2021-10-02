docker build -t dc .
docker run -idt --name DC -e TZ=Asia/Shanghai --restart=always dc
