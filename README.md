# 🚀 Dhan-Laabh - Stock Price Prediction Application

<div align="center">
  <img src="https://dhan-laabh.onrender.com/static/logo.png" alt="Dhan-Laabh Banner" width="800"/>
  <h3>
    <a href="https://dhan-laabh.onrender.com" target="_blank"><strong>💻 Live Demo</strong></a>
    <span>&nbsp;&nbsp;|&nbsp;&nbsp;</span>
    <a href="#-getting-started"><strong>🔧 Setup Guide</strong></a>
    <span>&nbsp;&nbsp;|&nbsp;&nbsp;</span>
    <a href="#-features"><strong>✨ Features</strong></a>
  </h3>
</div>

<div align="center">
  
[![License: MIT](https://img.shields.io/github/license/tgarg535/Dhan-Laabh?color=blue)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![DVC](https://img.shields.io/badge/DVC-Enabled-9cf.svg)](https://dvc.org/)

</div>

## 📊 About The Project

**Dhan-Laabh** is a comprehensive, end-to-end machine learning application engineered to forecast stock prices with high accuracy. By integrating advanced time-series models, historical market data, and real-time sentiment analysis, this tool empowers investors to make data-driven decisions. The project demonstrates a full MLOps pipeline, from data ingestion and model training to deployment via a user-friendly web interface.

<br>

## ✨ Features

-   📈 **Real-time Stock Data**: Fetches and displays up-to-the-minute stock information for a wide range of companies.
-   📊 **Interactive Visualizations**: Leverages Plotly and Chart.js to create dynamic charts for historical price analysis and future predictions.
-   🧠 **Sentiment Analysis**: Gathers and processes market sentiment from news headlines and social media to provide qualitative insights.
-   💼 **Portfolio Management**: Allows users to track their investments and monitor performance in a centralized dashboard.
-   ⚙️ **Customizable Predictions**: Offers flexibility to adjust prediction timeframes to align with different investment strategies.
-   📱 **Fully Responsive**: Ensures a seamless user experience across all devices, including desktops, tablets, and mobile phones.

<br>

## 🛠️ Tech Stack

This project is built with a modern, robust technology stack:

| Category              | Technologies                                                                                                                                                                                                                                                                                                                                                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Frontend**          | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)                                                                                                                  |
| **Backend**           | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)                                                                                                                                                                                                                       |
| **Data & ML**         | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) ![Scikit-learn](https://img.shields.io/badge/ScikitLearn-F7931E?style=flat&logo=scikit-learn&logoColor=white) ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=tensorflow&logoColor=white) |
| **Visualization**     | ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white) ![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chart.js&logoColor=white)                                                                                                                                                                                                                |
| **Version Control**   | ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) ![DVC](https://img.shields.io/badge/DVC-945DD6?style=flat&logo=dvc&logoColor=white)                                                                                                                                                                                                                                     |

<br>

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### **Prerequisites**

-   Python 3.8 or higher
-   Git command-line tools

### **Installation & Setup**

1.  **Clone the Repository**
    ```
    git clone https://github.com/tgarg535/Dhan-Laabh.git
    cd Dhan-Laabh
    ```

2.  **Create a Virtual Environment**
    It's recommended to create a virtual environment to manage project dependencies.
    ```
    python -m venv venv
    ```
    Activate the environment:
    -   On **Windows**: `venv\Scripts\activate`
    -   On **macOS/Linux**: `source venv/bin/activate`

3.  **Install Dependencies**
    The core application dependencies are located in the `flask_app` directory.
    ```
    pip install -r flask_app/requirements.txt
    ```

4.  **Run the Application**
    Navigate to the Flask application directory and start the server.
    ```
    cd flask_app
    python app.py
    ```

5.  **Access the Application**
    Open your web browser and go to `http://localhost:5000`.

<br>

## 📂 Project Structure

The repository is organized to separate concerns, making it modular and maintainable.



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


<br>

## 💻 Contributing

Contributions are welcome! If you have suggestions for improving the project, please feel free to fork the repository and create a pull request.

1.  **Fork the Project**
2.  **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3.  **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4.  **Push to the Branch** (`git push origin feature/AmazingFeature`)
5.  **Open a Pull Request**

<br>

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---
<div align="center">
  © 2023 Dhan-Laabh | Created with ❤️ by <a href="https://github.com/tgarg535">tgarg535</a>
</div>
