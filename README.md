
# Real-Time Stock Data Streaming Pipeline 🚀

This project demonstrates a **real-time data streaming pipeline** using **Apache Beam (Python SDK)**, **Google Pub/Sub**, and **YFinance** to simulate stock market data from the **NSE (National Stock Exchange)**. The pipeline is designed to compute **percentage change** in stock prices over a **fixed time window (5 minutes)** using event-time windowing and stream processing.

---

## 📌 Project Overview

- **Source**: YFinance API (mocked real-time using historical stock data).
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
| Data Source          | YFinance API (simulated)       |
| Cloud Environment    | Google Cloud Platform (GCP)    |
| Optional Deployment  | Google Cloud Dataflow          |

---

## 📂 Project Structure

```
RealTimeStreamingProject/
│
├── pubsub_publisher.py              # Publishes stock data to Pub/Sub every 30s
├── process_5min.py                  # Beam pipeline to process and window the stream
├── requirements.txt                 # Python dependencies
├── demo1-454518-XXXXXXX.json        # GCP service account credentials
├── utils/                           # Any helper functions (optional)
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

## 📈 Example Output

Every 5 minutes, Beam emits the percentage change in stock prices like:

```python
['RELIANCE.NS', 0.8312]
['TCS.NS', -0.1173]
['HDFCBANK.NS', 1.0456]
```

---

## 🧠 Key Concepts Covered

- ✅ Apache Beam with event-time and fixed windowing
- ✅ Google Pub/Sub integration with Beam
- ✅ Real-time simulation using historical stock data
- ✅ Percentage price change calculation
- ✅ Grouping, sorting, and custom transforms in Beam
- ✅ Streaming pipeline ready for GCP Dataflow

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
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "demo1-454518-XXXXXXX.json"
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
python pubsub_publisher.py
```

This sends simulated stock data every 30 seconds to the Pub/Sub topic.

### Step 2: Start the Beam Pipeline

```bash
python process_5min.py
```

This starts a streaming pipeline that:
- Processes every message from the subscription
- Groups by stock every 5 minutes
- Calculates % price change
- Logs output

---

## 🌐 Optional: Deploy to Google Cloud Dataflow

Set your GCP project, region, and storage:

```bash
python process_5min.py \
  --runner DataflowRunner \
  --project=demo1-454518 \
  --region=us-central1 \
  --temp_location=gs://your-bucket/tmp \
  --staging_location=gs://your-bucket/staging
```

---

## 💡 Real-World Use Cases

- 📊 Stock market monitoring
- 📉 Real-time price fluctuation alerts
- 🔄 Streaming ETL pipelines
- 🧮 Sliding or tumbling window analytics

---

## 📃 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## 🙋 Author

**[Your Name]**  
Data Engineer | Real-time Streaming Enthusiast  
📫 [LinkedIn Profile](https://linkedin.com/in/yourprofile)

---
