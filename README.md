# Benzinga Parser

## Overview
Benzinga Parser is a web application with a Python backend and a JavaScript frontend, running a MongoDB database. It is fully containerized using Docker.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Docker and Docker Compose are installed on your machine. For installation instructions, see [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/).

## Setup and Running the Application

### Clone the Repository
Clone this repository to your local machine:
```
git clone https://github.com/cherkiral/BenzingaParser
cd BenzingaParser
```

### Environment Variables
Create a `.env` file in the root directory and add the necessary environment variables:
```
DB_URL=mongodb://db:27017/news
```

### Building and Starting the Application
Run the following command to build and start all services (backend, frontend, and MongoDB):
```
docker-compose up --build
```

### Accessing the Application
- The frontend is available at: `http://localhost:3000`
- The backend is accessible at: `http://localhost:8000`
- The API docs are accessibli at: `http://localhost:8000/docs`

### Stopping the Application
To stop the application, run:
```
docker-compose down
```

## Connecting to MongoDB with Compass
To connect to the MongoDB database using MongoDB Compass:
1. Open MongoDB Compass.
2. Connect using the following connection string: `mongodb://localhost:27018`
3. If authentication is required, provide the necessary credentials.

## How it works
- The app first parses last 100 articles from https://www.benzinga.com/markets and then shows them in frontend
- If articles already were in db it shows last 10 of them
- Then you can choose time interval to parse the website again
- if new articles were found they will show in green bordered block
- You can click view details to see the body of an article, then you can also hide it
- All articles save in mongo DB


