FROM python:3.10-slim

# change working directory
WORKDIR /app/

# copy project file
COPY . .

# Install deps
RUN pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile --dev

# RUN python manage.py migrate

# CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
CMD sleep 3 \
    && python manage.py migrate \
    && python manage.py runserver 0.0.0.0:80