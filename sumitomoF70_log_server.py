# suggested Setup is to set up a python virtual environment and then install all of the packages below
import time
import random
from threading import Thread, Lock
from loguru import logger
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from sumitomo_f70 import SumitomoF70

# Customizable parameters
# Live data range (samples)
live_data_limit = 1000
# Polling period (ms)
interval_time = 1000
# Configure Loguru to log data to a file
log_file = "C:\Coding\Python\F70_serial_monitor\logs\F70_LTSPM3_data.log"
# How often to rotate to new log file
log_rotation = "5 MB"
# Port
comPort = "COM11"
polling_thread_started = False
thread_lock = Lock()

# Initialize Dash app
app = Dash(__name__)


logger.add(log_file, rotation=log_rotation)

# Initialize an in-memory DataFrame to store recent data points
data_df = pd.DataFrame(columns=["timestamp", "value"])


def sumitomo_get():

    with SumitomoF70(com_port=comPort) as f70:
        he_T, out_H20_T, in_H20_T, _ = f70.read_all_temperatures()
        he_Pressure, _ = f70.read_all_pressures()
        id_info = f70.read_id()
        status_bits, status_dict = f70.read_status_bits()

        f_70_data = {
            "timestamp": time.time(),
            "he_T": he_T,
            "out_H20_T": out_H20_T,
            "in_H20_T": in_H20_T,
            "he_Pressure": he_Pressure,
            "id_info": id_info,
            "status_bits": status_bits,
            "status_dict": status_dict
        }

    return f_70_data
# Function to simulate polling equipment and logging data


def poll_equipment():
    global data_df
    while True:
        try:
            equipment_data = sumitomo_get()
        except Exception as e:
            logger.error(f"Error polling equipment: {e}")

        # Log data with Loguru
        # logger.info(f"Timestamp: {equipment_data['timestamp']}, Value: {equipment_data['value']}")
        logger.info(equipment_data)
        print("Logging")
        # Append new data to the DataFrame
        data_df = pd.concat([data_df, pd.DataFrame(
            [equipment_data])], ignore_index=True)

        # Keep only the last x points in the DataFrame for efficiency
        if len(data_df) > live_data_limit:
            data_df = data_df.iloc[-live_data_limit:]

        # Poll every second
        time.sleep(round(interval_time/1000))


def start_polling():
    global polling_thread_started
    with thread_lock:
        if not polling_thread_started:
            polling_thread_started = True
            Thread(target=poll_equipment, daemon=True).start()
            print("Polling thread started")

# Start polling in a background thread
start_polling()

# Define Dash layout with a real-time graph
app.layout = html.Div([
    html.H1("Real-Time Equipment Data"),
    dcc.Graph(id="live-graph-1", config={"scrollZoom": True}),
    dcc.Graph(id="live-graph-2", config={"scrollZoom": True}),
    dcc.Interval(id="interval-component", interval=interval_time,
                 n_intervals=0)  # Update every second
])

# Update the graph at each interval


@app.callback(
    [Output("live-graph-1", "figure"), Output("live-graph-2", "figure")],
    Input("interval-component", "n_intervals")
)
def update_graph(n):
    try:
        # Convert the timestamp to a datetime format for better readability
        data_df["datetime"] = pd.to_datetime(data_df["timestamp"], unit="s")

        # Create the figure with Plotly
        fig1 = {
            "data": [
                {
                    "x": data_df["datetime"],
                    "y": data_df["he_T"],
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "Helium Discharge Temperature"
                },
                {
                    "x": data_df["datetime"],
                    "y": data_df["in_H20_T"],
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "Inlet Water Temperature"
                },
                {
                    "x": data_df["datetime"],
                    "y": data_df["out_H20_T"],
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "Outlet Water Temperature"
                }
            ],
            "layout": {
                "title": "Temperatures",
                "xaxis": {"title": "Time"},
                "yaxis": {"title": "Celsius"},
                "uirevision": "true"
            }
        }
        fig2 = {
            "data": [
                {
                    "x": data_df["datetime"],
                    "y": data_df["he_Pressure"],
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "Compressor Return He Pressure"
                }
            ],
            "layout": {
                "title": "Helium Pressure",
                "xaxis": {"title": "Time"},
                "yaxis": {"title": "PSIG"},
                "uirevision": "true"
            }
        }
        return fig1, fig2


    except Exception as e:
        print(e)
        return dash.no_update, dash.no_update


print(app.callback_map)
if __name__ == "__main__":
    time.sleep(4)
    print(app.callback_map)
    app.run_server(debug=True, host='0.0.0.0', port=8050, use_reloader=False)
