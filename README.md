
# Real-Time Stock Data Streaming Pipeline ⌛📈

This project demonstrates a **real-time data streaming pipeline** using **Apache Beam (Python SDK)**, **Google Pub/Sub**, and **YFinance** to simulate stock market data from the **NSE (National Stock Exchange)**.

The pipeline is designed to compute the **percentage change** in stock prices over **fixed time windows of 5 and 10 minutes** using event-time windowing and stream processing. Every 5 and 10 minutes after the start, the pipeline outputs the computed data for the respective windows.

Only the **top 15 NSE stocks** have been selected for this project. Their details are listed in the following sections.


---

## 📌 Project Overview

- **Source**: YFinance API.
- **Ingestion**: Google Cloud Pub/Sub.
- **Stream Processor**: Apache Beam with event-time and fixed windows.
- **Sink**: Console output (for simulation/demo purposes).
- **Cloud Ready**: Built for local execution, easily deployable on **Google Cloud Dataflow**.

---

## 🛠️ Technologies Used

| Component            | Technology                    |
|---------------------|-------------------------------|
| Stream Ingestion     | Google Pub/Sub                 |
| Processing Engine    | Apache Beam (Python SDK)       |
| Data Source          | YFinance API                   |
| Cloud Environment    | Google Cloud Platform (GCP)    |

---

## 📂 Project Structure

```
RealTimeStreamingProject/
│
├── publisher.py                     		# Publishes stock data to Pub/Sub every 30s
├── process_5min.py                  		# Beam pipeline to process and window the stream (every 5 minutes)
├── process_10min.py                  		# Beam pipeline to process and window the stream (every 10 minutes)
├── requirements.txt                 		# Python dependencies
├── GoogleApplicationCreadentialsFile.json      # GCP service account credentials
└── README.md                        # Project documentation
```

---

## 🔁 Pipeline Flow

```
YFinance (Historical Data)
        ↓
publisher.py → Publishes each stock row every 60s to Pub/Sub
        ↓
Google Cloud Pub/Sub Topic
        ↓
process_5min.py → Apache Beam Pipeline:
    - Decode and parse rows
    - Extract necessary columns
    - Add event timestamp
    - Apply fixed window (5 minutes)
    - Group by stock symbol
    - Compute percentage price change
        ↓
    Output to console


Google Cloud Pub/Sub Topic
        ↓
process_10min.py → Apache Beam Pipeline:
    - Decode and parse rows
    - Extract necessary columns
    - Add event timestamp
    - Apply fixed window (10 minutes)
    - Group by stock symbol
    - Compute percentage price change
        ↓
    Output to console
```
---
## Top 15 NSE stocks list

```
nse_top_15_tickers = [
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "HINDUNILVR.NS",
    "INFY.NS",
    "SBIN.NS",
    "BHARTIARTL.NS",
    "SUNPHARMA.NS",
    "ITC.NS",
    "BAJFINANCE.NS",
    "KOTAKBANK.NS",
    "LT.NS",
    "AXISBANK.NS",
    "ASIANPAINT.NS"
]
```
I will monitor only these 15 NSE stocks in this project. You can modify this as per your needs. You can add more tickers or delete any. You can easily find the ticker name for the said stock online.

---

## 📈 Example Output

Publisher output:

![image](https://github.com/user-attachments/assets/cc686043-a710-40e9-b8d0-04b0eb2b59e1)


Every 5 minutes, Beam emits the source, percentage change, gain, first_open, last_closed, all_time_high, all_time_low in stock prices like:

![image](https://github.com/user-attachments/assets/5a5d2d6e-a425-4dec-872c-09312abee6d6)


Every 10 minutes, Beam emits the source, percentage change, gain, first_open, last_closed, all_time_high, all_time_low in stock prices like:

![image](https://github.com/user-attachments/assets/79958f07-0c78-46db-aa1b-10632ffb9f39)

Understanding the output:

| Parameter           | What it means?                    
|---------------------|----------------------------------------------------------------------|
| Source              | The ticker name or the stock name                                    |
| Percentage change   | Percentage change over the past 5 or 10 minutes                      |
| Gain                | If percentage change is positive then gain is True else False        |
| First open          | Stock openining value for that window ( 5 or 10 minute window)       |
| Last closed         | Stock closing value for that window ( 5 or 10 minute window)         |
| All time high       | All time high for that particluar window ( 5 or 10 minute window)    |
| All time low        | All time low for that particluar window ( 5 or 10 minute window)     |


---

## 🧠 Key Concepts Covered

- ⭐ Apache Beam with event-time and fixed windowing
- ⭐ Google Pub/Sub integration with Beam
- ⭐ Real-time simulation using historical stock data
- ⭐ Percentage price change calculation
- ⭐ Grouping, sorting, and custom transforms in Beam
- ⭐ Streaming pipeline ready for GCP Dataflow

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/RealTimeStreamingProject.git
cd RealTimeStreamingProject
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure GCP Credentials

Ensure your **Google Cloud service account JSON** key is in the project directory.

```python
# Inside process_5min.py
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "file_name.json"
```

### 4. Create Pub/Sub Topic & Subscription

Use Google Cloud Console or CLI:

```bash
gcloud pubsub topics create RealTimeStreamingProject
gcloud pubsub subscriptions create RealTimeStreamingProject-sub --topic=RealTimeStreamingProject
```

---

## ▶️ Run the Project Locally

### Step 1: Start the Publisher

```bash
python publisher.py
```

This sends simulated stock data every 60 seconds to the Pub/Sub topic.

### Step 2: Start the Beam Pipeline

```bash
python process_5min.py
```

```bash
python process_10min.py
```

This starts a streaming pipeline that:
- Processes every message from the subscription
- Groups by stock every 5 minutes and 10 minutes
- Calculates % price change and other parameters
- Logs output

---

## 💡 Real-World Use Cases

- 📊 Stock market monitoring
- 📉 Real-time price fluctuation alerts (coming soon..!)
- 🔄 Streaming ETL pipelines
- 🧮 Tumbling window analytics

---

## 🔮 Future Scope

- I have already deployed this to google dataflow. You can easily deploy it from the command prompt.
- Deploy the output to a sink like BigQuery for further analysis. For this we need timestamp attribute.
  We can add the current timestamp when the stock was processed in the `calculate_percentage_change` function inside process_5min.py and process_10min.py
  
--- 

**Explore my other projects**

- [Airflow Batch Processing project](https://github.com/Sharathjagadeesh/AirflowBatchProcessingProject.git)

---

## 🙋 Author

**Sharath**  
Data Engineer | Real-time Streaming Enthusiast  | ETL | Batch Processing
📫 [LinkedIn Profile](https://www.linkedin.com/in/sharath-j-503382219/)

---

**Thank you for reading!**

---
