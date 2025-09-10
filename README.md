# 🚀 Dhan-Laabh - Stock Price Prediction Application

<div align="center">
  
  ![Dhan-Laabh Banner](https://github.com/tgarg535/Dhan-Laabh/raw/main/flask_app/static/logo.png)
  
  <h3>
    <a href="https://dhan-laabh.onrender.com" target="_blank">💻 Live Demo</a>
    <span> | </span>
    <a href="#installation-and-setup">🔧 Setup Guide</a>
    <span> | </span>
    <a href="#features">✨ Features</a>
  </h3>
  
  [![GitHub license](https://img.shields.io/github/license/tgarg535/Dhan-Laabh?color=blue)](LICENSE)
  [![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
  [![DVC](https://img.shields.io/badge/DVC-Enabled-9cf.svg)](https://dvc.org/)
  
</div>

## 📊 Project Overview

<p align="justify">
  <strong>Dhan-Laabh</strong> is an end-to-end Machine Learning project designed to predict stock prices using advanced time-series forecasting techniques. The application leverages historical stock data, sentiment analysis, and statistical models to provide accurate price predictions that help investors make informed decisions.
</p>

<details open>
  <summary><h2>✨ Features</h2></summary>
  
  - 📈 **Real-time Stock Data**: Get up-to-date stock information for various companies
  - 📊 **Interactive Charts**: Visualize historical price trends and predicted values
  - 🔍 **Sentiment Analysis**: Analyze market sentiment from news and social media
  - 💼 **Portfolio Tracking**: Monitor your investments in one place
  - ⏱️ **Customizable Timeframes**: Adjust prediction horizons based on your investment strategy
  - 📱 **Responsive Design**: Access from any device - desktop, tablet, or mobile
</details>

<details>
  <summary><h2>🛠️ Tech Stack</h2></summary>
  
  ### Frontend
  - ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) HTML
  - ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) CSS
  - ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) JavaScript
  
  ### Backend
  - ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) Python
  - ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) Flask
  
  ### Data Processing & ML
  - ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) Pandas
  - ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) NumPy
  - ![Scikit-learn](https://img.shields.io/badge/ScikitLearn-F7931E?style=flat&logo=scikit-learn&logoColor=white) Scikit-learn
  - ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=tensorflow&logoColor=white) TensorFlow
  
  ### Visualization
  - ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white) Plotly
  - ![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chart.js&logoColor=white) Chart.js
  
  ### Version Control
  - ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) Git
  - ![DVC](https://img.shields.io/badge/DVC-945DD6?style=flat&logo=dvc&logoColor=white) DVC (Data Version Control)
</details>

## 📂 Project Structure

```
Dhan-Laabh/
│
├── exception/          # Custom exception handling
├── flask_app/          # Web application
│   ├── artifacts/      # Model artifacts and saved models
│   ├── sentiment_analysis/ # Sentiment analysis components
│   ├── static/         # CSS, JavaScript, and images
│   ├── templates/      # HTML templates
│   ├── app.py          # Main Flask application
│   └── requirements.txt # Flask app dependencies
│
├── logger/             # Logging configuration
├── stock_prediction/   # Core ML pipeline components
├── notebook.ipynb      # Development notebook with analysis
├── dvc.yaml           # Data Version Control configuration
├── params.yaml        # Model parameters
├── setup.py           # Package setup configuration
└── README.md          # Project documentation
```

## 🚀 Installation and Setup

<details open>
  <summary><h3>Prerequisites</h3></summary>
  
  - Python 3.8 or higher
  - pip (Python package manager)
  - Git
</details>

### Setup Instructions

1️⃣ Clone the repository
```bash
git clone https://github.com/tgarg535/Dhan-Laabh.git
cd Dhan-Laabh
```

2️⃣ Create and activate a virtual environment (optional but recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3️⃣ Install the required dependencies for the Flask application
```bash
cd flask_app
pip install -r requirements.txt
```

4️⃣ Run the application
```bash
python app.py
```

5️⃣ Open your browser and navigate to `http://localhost:5000`

## 🏃‍♂️ Running the Application

<div align="center">
  
  ### The application is straightforward to run:
  
</div>

1. Ensure you have installed all dependencies from the `flask_app/requirements.txt` file
2. Navigate to the flask_app directory
3. Run the application using: `python app.py`
4. The application will start and be accessible at `http://localhost:5000`

## 💻 Development

To contribute to the development:

1. Create a new branch for your feature
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them
```bash
git add .
git commit -m "Add your meaningful commit message"
```

3. Push your changes to GitHub
```bash
git push origin feature/your-feature-name
```

4. Create a Pull Request on GitHub

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Data provided by various financial APIs
- Special thanks to all contributors and maintainers



---

<div align="center">
  
  © 2023 Dhan-Laabh | Created with ❤️ by <a href="https://github.com/tgarg535">tgarg535</a>
  
</div>
