# python 
FROM python:3.13.5

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app1

# Install dependencies
COPY requirement.txt /app1/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirement.txt
 
# Copy the application project files
COPY . /app1/

# Expose the port the app runs on
EXPOSE 8000 

# Command to run the application
CMD ["gunicorn", "yourprojectname.wsgi:application", "--bind", "0.0.0.0:8000"]