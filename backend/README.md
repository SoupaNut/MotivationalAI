# How to set up JSON file on Google Cloud:

## 1. Install cloud storage 
    - pip install google-cloud-storage

## 2. Create a bucket in Google Cloud console and then upload/create history.json
    - Navigation Menu (left) -> Cloud Storage -> Buckets -> Create +
    - Name the bucket "motivation-chatbot-history"

## 3. Create a Service Account Key
    - Navigation Menu (left) -> IAM & Admin -> Service Accounts -> Create Service Account
    - Assign Role as Storage Admin
    - Go back to the first bullet's page
    - Click on 3 dots on the right -> Manage Keys -> Add Keys -> Create New Key
    - Select JSON as the key type and click Create
    - Add this .json file to the "credentials" folder


# Deploy Python Applications - Google Cloud Run with Docker

This guide is based on the YouTube video [Deploy Python Applications - Google Cloud Run with Docker](https://www.youtube.com/watch/sqUuofLBfFw). Follow along to deploy a Python application to Google Cloud Run using Docker.

---

## Overview

In this tutorial, we'll deploy a Python Flask application (a to-do list app) to **Google Cloud Run** using **Docker**. The app will be hosted on the cloud and accessible via a public URL.

---

## Steps

### 1. Prepare the Application

Ensure your Flask application is set to run on **port 8080** (required by Google Cloud Run). Example Flask app structure:

- `app.py`: The main application file.
- `requirements.txt`: Specifies Python dependencies.

---

### 2. Create the `requirements.txt` File

Add all non-core Python packages your app requires. For example:

```txt
flask
3. Create the Dockerfile
Write a Dockerfile to containerize your application:

dockerfile
Copy code
# Use a base Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /to-do-app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Run the application
CMD ["python", "app.py"]
4. Build and Test Locally
Build the Docker image:

bash
Copy code
docker build -t todo-app .
Run the Docker container:

bash
Copy code
docker run -p 8080:8080 todo-app
Verify the app is working locally by visiting http://localhost:8080.

Deploying to Google Cloud Run
1. Set Up Google Cloud
Go to the Google Cloud Console.
Create a new project:
Example name: todo-app-deploy.
Enable APIs:
Cloud Run API
Cloud Build API
2. Install Google Cloud CLI
Install the CLI to interact with Google Cloud from your terminal:

Installation guide: gcloud CLI Documentation.
Or install using Snap (Linux):

bash
Copy code
snap install google-cloud-cli --classic
3. Authenticate and Initialize
Authenticate with your Google account:

bash
Copy code
gcloud auth login
Initialize the CLI:

bash
Copy code
gcloud init
4. Deploy to Google Cloud Run
Build and deploy the Docker image directly from the Cloud:

bash
Copy code
gcloud run deploy
Follow the prompts to:

Select your project.
Specify the region.
Choose "Allow unauthenticated invocations".
5. Access Your App
Once deployed, Google Cloud Run will provide a public URL for your application.

Notes
The app must listen on port 8080 and bind to 0.0.0.0 instead of localhost.
You can use the Cloud Console for a graphical interface if you prefer over the CLI.
For more details and the example code, visit the GitHub repository.