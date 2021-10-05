FROM selenium/standalone-chrome
USER root
ENV TZ=Asia/Shanghai \
    DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install python3-pip -y \
    && pip install selenium -i https://pypi.tuna.tsinghua.edu.cn/simple \ 
    && mkdir /data
COPY ./* /xh_data/
CMD /usr/bin/python3 /xh_data/main.py
