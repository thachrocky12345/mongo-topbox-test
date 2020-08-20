FROM python:3.7-alpine
WORKDIR /web
ENV FLASK_APP app/app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY setup.py setup.py
RUN pip install -e .
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
