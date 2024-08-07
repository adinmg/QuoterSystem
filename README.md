# Deploy Async FastAPI Microservice on AWS EC2 🚀

This project demonstrates how to deploy an asynchronous microservice using **FastAPI**, **LangChain**, and **Nginx**. The microservice is designed to leverage asynchronous programming for high performance and scalability. **Nginx** is utilized for routing incoming requests to the **FastAPI** application, ensuring efficient load balancing and improved performance. This setup allows for a highly responsive and scalable service architecture. 🌐⚡

## Technologies Used 🛠️

- **FastAPI**: A modern, high-performance web framework for building APIs with Python.
- **Nginx**: A high-performance web server and reverse proxy.
- **LangChain**: A framework for building applications powered by language models.
- **OpenAI**: Provides state-of-the-art language models for NLP tasks.
- **FAISS**: A library for efficient similarity search and clustering of dense vectors.
- **Docker**: Containerization platform to build and run applications in isolated environments.

## 1. Testing Locally 🧪

### 1.1. Clone the Repository
First, clone this repository to your local machine:
```bash
$ git clone https://github.com/adinmg/QuoterSystem.git
```

### 1.2. Configure Environment Variables
Create a `.env` file in the root directory of the project and add your OpenAI API key:
```
OPENAI_API_KEY="your-openai-api-key"
```

### 1.3. Run Docker Compose
Start the services defined in the `docker-compose.yml` file:
```bash
$ docker-compose up -d
```

### 1.4. Access the Frontend
Open your web browser and go to:
```
http://localhost
```

### 1.5. Access API Documentation
You can view the API documentation and Redoc by navigating to:
```
http://localhost/api/v1/docs
http://localhost/api/v1/redoc
```

## Test Synchronous and Asynchronous Capabilities 🧪

To explore and test the synchronous and asynchronous capabilities of the microservice, follow these steps:

1. **Run Synchronous Tests**: Locate and execute the file `tests/sync_quoter_requests.py` to test the synchronous functionality of the microservice. This script contains various test cases that demonstrate how the microservice handles synchronous requests.

    ```bash
    $ python tests/sync_quoter_requests.py
    ```

2. **Run Asynchronous Tests**: Locate and execute the file `tests/async_quoter_requests.py` to test the asynchronous functionality of the microservice. This script includes test cases that showcase how the microservice processes asynchronous requests.

    ```bash
    $ python tests/async_quoter_requests.py
    ```

By running these tests, you can gain insights into the advantages of asynchronous programming and how it impacts the responsiveness and efficiency of the microservice.



## 2. Deployment on AWS EC2 ☁️

### 2.1. Accessing Your EC2 Instance via SSH
1. Open an SSH client.
2. Locate your private key file.
3. Run the following command to ensure your key is not publicly viewable:
```bash
$ chmod 400 your_pem_key.pem
```
4. Connect to your EC2 instance using its Public DNS:
```bash
$ ssh -i "your_pem_key.pem" ubuntu@IP.compute-1.amazonaws.com
```

### 2.2. Install Dependencies on Your EC2 Instance
Once connected to your EC2 instance, install the necessary dependencies:
```bash
$ sudo apt-get update
$ sudo apt install -y docker.io
$ sudo apt install -y docker-compose
```

### 2.3. Clone the Repository and Start the Services
1. Clone this repository to your EC2 instance:
```bash
$ git clone https://github.com/adinmg/QuoterSystem.git
$ cd QuoterSystem
```
2. Start the services using Docker Compose:
```bash
$ sudo docker-compose up -d
```

You can now access your frontend and documentation as described in the following sections:

- **Frontend:** http://your-ec2-public-dns
- **API Documentation:** http://your-ec2-public-dns/api/v1/docs
- **Redoc Documentation:** http://your-ec2-public-dns/api/v1/redoc

## 5. Contributing 🤝

We welcome contributions from the community to improve this project!

If you have any questions or need help, feel free to open an issue in the repository. We appreciate your interest in contributing! 🌟
