import pandas as pd
import os
from datetime import datetime

metrics = []
id=datetime.now().strftime("%Y%m%d_%H%M%S")

def log_metric(eou_delay, ttft, ttfb, total_latency):
    metrics.append({
        "Timestamp": datetime.now(),
        "EOU Delay": eou_delay,
        "TTFT": ttft,
        "TTFB": ttfb,
        "Total Latency": total_latency
    })

def save_to_excel():
    # Create metrics folder if it doesn't exist
    metrics_folder = "metrics"
    if not os.path.exists(metrics_folder):
        os.makedirs(metrics_folder)
    
    df = pd.DataFrame(metrics)
    
    if not df.empty:
        # Compute mean of all numeric columns
        avg_row = df.mean(numeric_only=True)
        avg_row["Timestamp"] = "Average"
        
        # Append average row
        df.loc[len(df)] = avg_row

    file_path = os.path.join(metrics_folder, f"session_metrics{id}.xlsx")
    df.to_excel(file_path, index=False)
