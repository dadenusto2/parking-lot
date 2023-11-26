# start by pulling the python image
FROM python:3.10-slim-buster
# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt
# switch working directory
WORKDIR /app
# install the ffmpeg libsm6 libxext6
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt
# copy every content from the local file to the image
COPY . /app
EXPOSE 4565
# configure the container to run in an executed manner
ENTRYPOINT ["python"]
CMD ["app.py"]