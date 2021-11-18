import datetime
import json
import random
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from matplotlib.backends.backend_qt5agg import *
import requests as req
import matplotlib.pyplot as plt


TOKEN = "TBE4NQ8ZDNFIV2KI4CPNE6GPWQVR8NCFGJ"
CL_TOKEN = "77f1b9d3d2912dd0b4bd668a9b271bed"

window = None

def show_window():
    global window
    app = QApplication(sys.argv)
    window = QWidget()

    histories = []

    for d in range(1, int(datetime.datetime.now().date().today().day)):
        day_val = str(d)
        if d < 10:
            day_val = "0" + str(d)
        print("http://api.coinlayer.com/2021-11-"+str(day_val)+"?access_key=" + CL_TOKEN);
        histories.append(req.get("http://api.coinlayer.com/2021-11-"+str(day_val)+"?access_key=" + CL_TOKEN))

    eth_price = req.get("https://api.etherscan.io/api?module=stats&action=ethprice&apikey=" + TOKEN)

    eth_historical_vals = []
    eth_historical_dates = []
    for eth_val in histories:
        eth_h = json.loads(eth_val.text) # Etherium history
        print(histories.index(eth_val), eth_h)
        date = eth_h["date"]
        eth_values = eth_h["rates"]

        eth_historical_vals.append(eth_values["ETH"])
        eth_historical_dates.append(date)

    fig, ax = plt.subplots(constrained_layout=True)  # Create a figure containing a single axes.
    fig.figsize = (400, 200)
    plt.step = 2000
    plt.xlabel('DATE(DAY)')
    plt.title("Etherium price for this current month")
    plt.ylabel('VALUE(USD)')
    ax.autoscale(True)
    ax.xaxis_date()
    ax.set_xscale("linear")
    ax.autoscale_view(True, True, True)

    ax.plot(eth_historical_dates, eth_historical_vals)

    canvas = FigureCanvasQTAgg(fig)
    form_layout = QFormLayout()
    form_layout.addWidget(canvas)
    window.setLayout(form_layout)
    # Eth data unparsed
    eth_data = json.loads(eth_price.text)
    eth_values = eth_data["result"] # Parsed eth data
    for key in eth_data:
        if key == "message" and eth_data[key] == "OK":
            eth_btc = QLabel(window)
            eth_btc.move(10, 25)
            eth_btc.setFocus()
            eth_btc.setText("1 eth is " + str(eth_values["ethbtc"]) + " bitcoin.")
            eth_usd = QLabel(window)
            eth_usd.setFocus()
            eth_usd.move(10, 50)
            eth_usd.setText("1 eth is " + str(eth_values["ethusd"]) + " usd.")
            break


    window.setGeometry(0, 0, 800, 400)
    window.setWindowTitle("Crypto Value Tracker")
    window.show()

    sys.exit(app.exec_())

show_window()

while True:
    print(window.cursor().pos())
