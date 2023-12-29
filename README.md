# CodeAuditWeb

CodeAuditWeb is a robust web application designed for developers and coders to test and analyze the performance of their code. Built on FastAPI, it provides an intuitive interface to execute code snippets, analyze execution time, memory usage, and detailed profiling, with additional graphically analysis. Additionally, it features an endpoint testing tool allowing users to test various HTTP methods.

## Features

### Code Testing and Analysis

- **Execution Time Measurement**: Analyze the execution time of code snippets, useful for optimizing code performance.
- **Memory Usage Analysis**: Measure the memory footprint of code execution, crucial for resource-intensive applications.
- **Detailed Profiling**:
  - **Basic Profiling**: General code profiling to identify bottlenecks.
  - **Advanced Profiling**: Line-by-line profiling for more in-depth analysis.
- **Graph Generation**:
  - **DotGraph**: Generate graphical representations of code execution flow.
  - **FlameGraph**: Create flame graphs for performance visualization.

### Endpoint Testing

- Supports various HTTP methods: GET, PUT, DELETE, PATCH, POST.
- Customizable requests with URL, header, and body inputs.

## Demo

#### Code Testing

![Code Testing Demo](/static/demo/code-analysis-demo.gif)

#### Endpoint Testing

![Endpoint Testing Demo](/static/demo/endpoint-demo.gif)

## Getting Started

### Prerequisites

Before running CodeAuditWeb, ensure you have the following installed:

- Python 3.x
- pip (Python package manager)
- Graphviz (for graph generation)
- Other Python dependencies listed in `requirements.txt`

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/JoshCap20/CodeAuditWeb.git
   cd CodeAuditWeb
   ```
2. Install Python dependencies (recommended in a virtual environment):

   ```bash
   pip install -r requirements.txt
   ```
3. Run the setup script to check and install additional requirements:

   ```bash
    python setup.py
    ```
4. Run the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```
   OR 
   ```bash
    python main.py
    ```
    (uses default host and port settings from `config.py`)

### Usage

#### Code Testing

1. Access the web interface at `http://localhost:8000/`.
2. Enter the code snippet in the provided code editor.
3. Choose the desired performance analysis strategies (time, memory, profiling).
4. Click 'Run Code' to execute and analyze the code.

#### Endpoint Testing

1. Switch to the Endpoint tab at `http://localhost:8000/endpoint`.
2. Enter the URL, select the HTTP method, and provide headers and body if necessary.
3. Click 'Send Request' to test the endpoint.

## Modularity and Customization
The application is modular, allowing easy addition of new analysis strategies in the `measures` directory. These are used to populate the options in the web interface.  
Configuration settings in config.py can be modified as per requirements.