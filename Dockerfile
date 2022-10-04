FROM python:3.10-slim

# receive build arguments
ARG PIPENV_EXTRA_ARGS

# change working directory
WORKDIR /app/

# copy project file
COPY ./ ./

# Install deps
RUN pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile $PIPENV_EXTRA_ARG

# RUN python manage.py migrate

# CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
CMD sleep 3 \
    && python src/manage.py migrate \
    && python src/manage.py runserver 0.0.0.0:80