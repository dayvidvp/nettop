import os
import time
import psutil
from rich.live import Live
from rich.table import Table

def bytes_to_mbps(value, duration):
    bits = value * 8
    mbps = bits / duration / 1_000_000
    return mbps

def get_network_data():
    net_data = psutil.net_io_counters(pernic=True)
    return net_data

def create_table():
    table = Table(title="🌐Nettop🌐", show_header=True, header_style="bold magenta")
    table.add_column("Interface", justify="left", style="cyan")
    table.add_column("Up (Mb/s)", justify="right", style="green")
    table.add_column("Down (Mb/s)", justify="right", style="red")
    table.add_column("Totaal (Mb/s)", justify="right", style="yellow")
    return table

def display_network_data():

    os.system("clear" if os.name == "posix" else "cls")
    duration = 1

    with Live(auto_refresh=False) as live:
        net_data_old = get_network_data()
        time.sleep(duration)

        while True:

            table = create_table()
            net_data_new = get_network_data()

            for interface in net_data_new:
                if interface not in net_data_old:
                    continue

                sent_old = net_data_old[interface].bytes_sent
                sent_new = net_data_new[interface].bytes_sent

                recv_old = net_data_old[interface].bytes_recv
                recv_new = net_data_new[interface].bytes_recv

                sent_mbps = bytes_to_mbps(sent_new - sent_old, duration)
                recv_mbps = bytes_to_mbps(recv_new - recv_old, duration)
                total_mbps = sent_mbps + recv_mbps

                if total_mbps == 0:
                    continue

                table.add_row(
                    f"{interface} 📶",
                    f"{sent_mbps:.2f} 🔼",
                    f"{recv_mbps:.2f} 🔽",
                    f"{total_mbps:.2f} 🔁"
                )

            live.update(table, refresh=True)

            time.sleep(duration)

            net_data_old = net_data_new

if __name__ == "__main__":

    try:
        display_network_data()
    except KeyboardInterrupt:
        pass
