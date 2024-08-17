FROM python:3.9-slim

WORKDIR /HottelTravel

COPY . .

RUN apt-get update && apt-get install -y locales \
    && locale-gen en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install streamlit --upgrade

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl --fail http://localhost:8501 || exit 1

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]