# PDF Chat with Amazon Bedrock

A Retrieval-Augmented Generation (RAG) based application that allows users to chat with their PDF documents using Amazon Bedrock, LangChain, Docker, and Streamlit.

![Architecture Diagram](https://raw.githubusercontent.com/uniabhi/PDF-Chat-with-Bedrock/main/architecture-diagram.svg)

## Architecture

This project consists of two separate applications:

### Admin Application
- Allows administrators to upload PDF documents
- Splits PDF text into manageable chunks
- Uses Amazon Titan Embedding Model to create vector representations
- Stores vector embeddings in FAISS format
- Uploads vector indices to Amazon S3

### User Application
- Downloads vector indices from S3
- Processes user queries using Amazon Titan Embedding Model
- Performs similarity search to find relevant document chunks
- Uses retrieved context with LLama 3 (8B) to generate responses
- Presents answers through a user-friendly Streamlit interface

![Complete Application Flow Diagram](https://raw.githubusercontent.com/uniabhi/PDF-Chat-with-Bedrock/main/diagram%20(2).png)

## Technical Overview

The application implements a Retrieval-Augmented Generation (RAG) pattern:

1. **Document Processing**: PDFs are split into chunks and converted to vector embeddings
2. **Vector Storage**: Embeddings are stored in FAISS and saved to S3
3. **Query Processing**: User questions are converted to vectors and matched with document chunks 
4. **Context-Enhanced Generation**: Relevant document chunks are provided as context to the LLM
5. **Response Generation**: LLM generates answers based on the retrieved context

## Features

- 📄 Upload and process PDF documents
- 🔍 Semantic search across document content
- 🤖 LLM-powered responses based on document context
- 🌐 Containerized deployment with Docker
- ☁️ AWS integration (S3, Bedrock)
- 🔗 Efficient retrieval using FAISS vector store

## Prerequisites

- AWS account with access to Amazon Bedrock
- AWS IAM role with appropriate permissions:
  - S3 read/write access
  - Bedrock model access (Titan Embeddings, LLama 3)
- Docker installed locally

## Setup and Deployment

### Environment Variables

Both applications require the following environment variables:
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: AWS region (e.g., "us-east-1")
- `BUCKET_NAME`: S3 bucket name for storing vector indices

### Admin Application

1. Navigate to the Admin directory
2. Build the Docker image:
   ```bash
   docker build -t pdf-reader-admin .
   ```
3. Run the container:
   ```bash
   docker run -e BUCKET_NAME=your-s3-bucket-name -v ~/.aws:/root/.aws -p 8083:8083 -it pdf-reader-admin
   ```
4. Access the admin interface at http://localhost:8083

### User Application

1. Navigate to the User directory
2. Build the Docker image:
   ```bash
   docker build -t pdf-reader-client .
   ```
3. Run the container:
   ```bash
   docker run -e BUCKET_NAME=your-s3-bucket-name -v ~/.aws:/root/.aws -p 8084:8084 -it pdf-reader-client
   ```
4. Access the user interface at http://localhost:8084

> **Note**: The Docker volume mount (`~/.aws:/root/.aws`) is only needed for local development. In production environments like ECS or EKS, use IAM roles instead.

## Production Deployment

For production deployment:

1. Push Docker images to Amazon ECR or another container registry
2. Deploy containers using ECS, EKS, or other container orchestration services
3. Use IAM roles instead of environment variables for AWS authentication
4. Configure appropriate security groups and network access controls

## AWS Services Used

- **Amazon Bedrock**: For LLM inferencing and embeddings generation
- **Amazon S3**: For storing vector indices
- **AWS IAM**: For securing API access

## Models Used

- **Amazon Titan Embedding G1 - Text**: For generating document and query embeddings
- **Meta LLama 3 (8B)**: For generating responses based on retrieved context

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- LangChain for providing the RAG framework
- FAISS for efficient vector search capabilities
