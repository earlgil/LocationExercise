FROM conda/miniconda3

ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt . 
RUN pip install -r requirements.txt
COPY . . 
CMD ["python", "app_geodata.py"]