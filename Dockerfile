FROM python:3.4
COPY src /app
WORKDIR /app
RUN pip install oauth2client
RUN pip install PyOpenSSL
RUN pip install gspread
RUN pip install oauth2client==1.5.2
RUN pip install python-dateutil
RUN pip install pandas
CMD python3 JenkinsJobStatus.py
