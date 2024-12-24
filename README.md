# Restaurant Microservice System

## Project Overview

This is a comprehensive microservice-based restaurant management system designed to streamline restaurant operations across multiple services.

## System Architecture

The system is composed of the following microservices:

1. **Frontend Service**: User interface and client-side interactions
2. **Kitchen Service**: Manages kitchen operations and food preparation
3. **Notification Service**: Handles communication and alerts
4. **Order Service**: Processes and manages customer orders
5. **Web Service**: Additional web-related functionalities

## Prerequisites

- Docker
- Docker Compose
- Python 3.8+
- gRPC (Protocol Buffers)

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/RestoranMicroservice.git
cd RestoranMicroservice
```

### 2. Start Services
```bash
docker-compose up --build
```

## Service Descriptions

### Frontend Service
- Handles user interface
- Provides interactive client-side experience
- Dockerized for consistent deployment

### Kitchen Service
- Manages food preparation workflows
- Tracks kitchen inventory and orders
- Communicates with Order Service

### Notification Service
- Sends alerts and notifications
- Supports multiple communication channels
- Integrates with other services

### Order Service
- Processes customer orders
- Manages order lifecycle
- Communicates with Kitchen and Notification services

### Web Service
- Provides additional web-related functionalities
- Supports API endpoints
- Handles web-specific interactions

### Contribution Guidelines
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Technologies Used
- Python
- gRPC
- Docker
- Docker Compose
- Protocol Buffers

