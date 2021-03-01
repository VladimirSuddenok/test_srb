FROM python:3.8-slim-buster
COPY test_sbr /opt/project

ENV work_dir=/opt/project \
    log_setting=/opt/project/supports/log_config.json \
    app_setting=/opt/project/supports/app_config.ini \
    db=/opt/project/foo.db

WORKDIR ${work_dir}

RUN pip install -r requirements.txt
RUN python3 ./supports/build_db.py