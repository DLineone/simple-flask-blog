FROM python:3.10

COPY requirements.txt .

# RUN pip install --upgrade pip && pip install -r requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 5000