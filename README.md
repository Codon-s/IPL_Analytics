# **IPL_Analytics**

View Dashboard: [iplmetrics.streamlit.app](https://iplmetrics.streamlit.app/)

An interactive and in-depth IPL (Indian Premier League) Analytics Dashboard build with Python and Streamlit. This project provides a comprehensive analysis of IPL match data, offering insights at multiple levels: individual match breakdowns, overall series trends, and team-specific performance analysis.

The dashboard leverages a modern data science stack, including **Pandas** for data manipulation and a combination of **Plotly, Matplotlib, and Seaborn** to create rich, interactive visualizations.

!['Screenshot of first page'](screenshots/screenshot_page1.png)

## **Features**

This dashboard is structured into three main analytical sections, allowing users to explore the data from different perspectives:

### **1\. Match-Level Analysis**

Dive deep into the specifics of any single match.

* **Detailed Scorecards:** View complete batting and bowling scorecards for both innings.
* **Performance Metrics:** Analyze team totals, run rates, and balls faced.
* **Dismissal Analysis:** Visualize the types of dismissals (e.g., caught, bowle, LBW) for each team with interactive pie charts.
* **Boundary Breakdown:** Compare the number of fours and sixes hit by each team.
* **Fielder Impact:** See which fielders took catches against which batsmen.

### **2.\. Series-Wide Analysis**

Zoom out to uncovere trends and patterns across the entire IPL series.

* **Venue Insights:** Compare average first and second innings scores for each stadium to understand pitch behavior.
* **Toss Strategy:** Analyze team and venue-specific toss decisions (bat vs. field) and their outcomes.
* **Team Standings:** View a summary of matches won and lost by each team throughout the tournament.
* **Top Performers:** Identify key players and standout performances across the series.

### **3\. Team-Specific Performance**

Focus on a single team to analyze its structure and performance.

* **Squad Composition:** Get a breakdown of a team's squad by playyer role (Batsman, Bowler, All-Rounder) and nationality (domestic vs overseas).
* **City-wise Performane:** Visualize a team's win-loss record across different host cities.

## **Tech Stack**

* **Core Language:** Python
* **Dashboard Framework:** Streamlit
* **Data Manipulation:** Pandas
* **Data Visualization:** Plotly, Matplotlib, Seaborn

## **Project Structure**
```
.
├── data/                     \# Contains the raw data files  
|   ├── squad/
|   |   └── \*.csv
│   ├── scorecard/  
│   |   └── \*.json
|   └── \*.csv  
├── notebooks/                \# Jupyter notebooks for exploratory
│   ├── match_analysis.ipynb  
│   ├── series_analysis.ipynb  
│   └── team_performance_analysis.ipynb  
├── app.py                    \# The main Streamlit application script  
├── requirements.txt          \# Project dependencies  
└── README.md
```

## **Getting Started**

Follow these instructions to set up and run the project on your local machine.

### **Prerequisites**

* Python 3.13 or higher

### **Installation & Setup**

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Codon-s/IPL_Analytics.git
    cd IPL_Analytics
    ```

2. **Create a virutal environment (recommended):**

    \# For Windows
    ```bash
    python -m venv venv  
    venv/Scripts/activate
    ```
    \# For macOS/Linux
    ```bash  
    python3 \-m venv venv  
    source venv/bin/activate
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

5. Open your web browser and navigate to http://localhost:8501 to view the dashboard.

## **Data Source**

The data for this project was sourced from [cricketdata.org](https://cricketdata.org/) using their official APIs. The raw data, including detailed scorecard information for each match, was fetched programmatically and then stored in local JSON and CSV files for easier access and improved performance within the application.
