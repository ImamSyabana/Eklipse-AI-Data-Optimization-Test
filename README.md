# AI-Powered Game Data Enhancement

This project uses the Google Generative AI API to enrich a CSV file of video games. It automatically generates the genre, a short description, and the player mode for each game title based on its name.

---

## Prerequisites

Before you begin, ensure you have **Anaconda** or **Miniconda** installed on your system to manage the virtual environment.

* [Download Anaconda](https://www.anaconda.com/download)

---

## ⚙️ Installation and Setup

Follow these steps to set up the project environment.

### 1. Clone the Repository

First, clone this repository to your local machine.

```bash
git clone https://github.com/ImamSyabana/Eklipse-AI-Data-Optimization-Test.git
```

### 2. Create a conda virtual environment

Copy this to anaconda prompt

# Create the environment named 'task_2' with Python 3.13.5
conda create --name task_2 python=3.13.5

# Activate the newly created environment
conda activate task_2

### 3. Install Required Libraries

This project's dependencies are listed in the requirements.txt file. Create this file in your project directory with the following content: requirements.txt

pandas
numpy
python-dotenv
google-generativeai

Now, install these libraries using pip:

```bash
pip install -r requirements.txt
```
