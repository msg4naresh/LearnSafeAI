# OpenWeb UI Local Setup

This guide will help you set up **OpenWeb UI** locally on your machine.

## Prerequisites

Before you start, ensure you have the following installed:

1. **Python 3.11** or higher
2. **pip** (Python package installer)
3. **Git** (for cloning the repository)
4. **Node.js** and **npm**

## Step-by-Step Installation

### 1. Clone the Repository

First, clone the OpenWeb UI repository to your local machine:

```bash
git clone https://github.com/open-webui/open-webui.git
cd open-webui
```

### 2. Set Up the Environment Configuration

Copy the `.env.example` file to `.env`:

```bash
copy .env.example .env    # On Windows
# or
cp .env.example .env      # On Linux/Mac
```

### 3. Install Frontend Dependencies and Build the Application

Install the required Node.js dependencies and build the frontend:

```bash
npm install
npm run build
```

### 4. Set Up the Backend

Navigate to the backend directory:

```bash
cd ./backend
```

### 5. (Optional) Set Up Conda Environment

If you prefer using Conda as your development environment, follow these steps:

- Create and activate a Conda environment with Python 3.11:

    ```bash
    conda create --name open-webui-env python=3.11
    conda activate open-webui-env
    ```

### 6. Install Python Dependencies

Install the required Python dependencies using `pip`:

```bash
pip install -r requirements.txt -U
```

### 7. Run the Application

To start the application, you can use the provided batch script on Windows:

```bash
start.bat
```

This will start the backend server.

### 8. Access the UI

Open your browser and navigate to:

```
http://localhost:5000
```

You should now see the OpenWeb UI interface.

## Get Started with Pipelines

Follow these steps to set up Pipelines for enhanced functionality:

### 1. Ensure Python 3.11 is Installed

Make sure you have Python 3.11 or higher installed on your machine.

### 2. Clone the Pipelines Repository

Clone the Pipelines repository to your local machine:

```bash
git clone https://github.com/open-webui/pipelines.git
cd pipelines
```

### 3. Install the Required Dependencies

Run the following command to install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 4. Start the Pipelines Server

Once the dependencies are installed, start the Pipelines server:

```bash
sh ./start.sh
```

### 5. Set the OpenAI URL to Pipelines

After the server is running, configure your client by setting the OpenAI URL to the Pipelines URL. This allows you to unlock the full capabilities of Pipelines, integrating any Python library and enabling the creation of custom workflows tailored to your needs.

## Additional Notes

- Ensure that both the backend and frontend are running successfully.
- Make sure your `python` and `pip` commands point to Python 3. If you are using multiple versions of Python, you might need to use `python3` and `pip3` instead.
- If you encounter any issues, check for missing dependencies and install them manually using `pip install <dependency_name>`.

## Troubleshooting

- **Port already in use:** If you get an error stating that the port is already in use, try running the app on a different port:

    ```bash
    python app.py --port 8080
    ```

- **Issues with dependencies:** If you encounter problems with dependencies, ensure you have the correct versions installed by reviewing `requirements.txt`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
