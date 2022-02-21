FROM python:3.8

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

RUN echo 'source /root/.cargo/env' >> /etc/profile
RUN /bin/bash -c "source /root/.cargo/env && rustup install 1.57.0"

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENV PYTHONPATH="/workspaces/mashumaro-pyo3-benchmark"
