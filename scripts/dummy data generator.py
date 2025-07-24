import csv
import random
import datetime
import os

# --- Full client list from your example ---
clients = [
    # Client 1
    {"client_name": "Client 1", "vm_id": "C1VM1", "ip": "10.0.1.1", "os": "Windows Server 2019", "total_gb": 500},
    {"client_name": "Client 1", "vm_id": "C1VM2", "ip": "10.0.1.2", "os": "Windows Server 2019", "total_gb": 750},
    {"client_name": "Client 1", "vm_id": "C1VM3", "ip": "10.0.1.3", "os": "Windows Server 2019", "total_gb": 300},

    # Client 2
    {"client_name": "Client 2", "vm_id": "C2VM1", "ip": "10.1.1.1", "os": "Ubuntu 20.04 LTS", "total_gb": 250},
    {"client_name": "Client 2", "vm_id": "C2VM2", "ip": "10.1.1.2", "os": "Ubuntu 20.04 LTS", "total_gb": 300},
    {"client_name": "Client 2", "vm_id": "C2VM3", "ip": "10.1.1.3", "os": "Ubuntu 20.04 LTS", "total_gb": 200},
    {"client_name": "Client 2", "vm_id": "C2VM4", "ip": "10.1.1.4", "os": "Ubuntu 20.04 LTS", "total_gb": 150},

    # Client 3
    {"client_name": "Client 3", "vm_id": "C3VM1", "ip": "10.2.1.1", "os": "Amazon Linux 2", "total_gb": 400},
    {"client_name": "Client 3", "vm_id": "C3VM2", "ip": "10.2.1.2", "os": "Amazon Linux 2", "total_gb": 600},
    {"client_name": "Client 3", "vm_id": "C3VM3", "ip": "10.2.1.3", "os": "Amazon Linux 2", "total_gb": 350},
    {"client_name": "Client 3", "vm_id": "C3VM4", "ip": "10.2.1.4", "os": "Amazon Linux 2", "total_gb": 450},
    {"client_name": "Client 3", "vm_id": "C3VM5", "ip": "10.2.1.5", "os": "Amazon Linux 2", "total_gb": 700},

    # Client 4
    {"client_name": "Client 4", "vm_id": "C4VM1", "ip": "10.3.1.1", "os": "RHEL 8", "total_gb": 700},
    {"client_name": "Client 4", "vm_id": "C4VM2", "ip": "10.3.1.2", "os": "RHEL 8", "total_gb": 500},
    {"client_name": "Client 4", "vm_id": "C4VM3", "ip": "10.3.1.3", "os": "RHEL 8", "total_gb": 450},

    # Client 5
    {"client_name": "Client 5", "vm_id": "C5VM1", "ip": "10.4.1.1", "os": "Windows Server 2016", "total_gb": 350},
    {"client_name": "Client 5", "vm_id": "C5VM2", "ip": "10.4.1.2", "os": "Windows Server 2016", "total_gb": 300},
    {"client_name": "Client 5", "vm_id": "C5VM3", "ip": "10.4.1.3", "os": "Windows Server 2016", "total_gb": 400},
    {"client_name": "Client 5", "vm_id": "C5VM4", "ip": "10.4.1.4", "os": "Windows Server 2016", "total_gb": 250},

    # Client 6
    {"client_name": "Client 6", "vm_id": "C6VM1", "ip": "10.5.1.1", "os": "Ubuntu 18.04", "total_gb": 600},
    {"client_name": "Client 6", "vm_id": "C6VM2", "ip": "10.5.1.2", "os": "Ubuntu 18.04", "total_gb": 550},
    {"client_name": "Client 6", "vm_id": "C6VM3", "ip": "10.5.1.3", "os": "Ubuntu 18.04", "total_gb": 300},
    {"client_name": "Client 6", "vm_id": "C6VM4", "ip": "10.5.1.4", "os": "Ubuntu 18.04", "total_gb": 250},
    {"client_name": "Client 6", "vm_id": "C6VM5", "ip": "10.5.1.5", "os": "Ubuntu 18.04", "total_gb": 400},
    {"client_name": "Client 6", "vm_id": "C6VM6", "ip": "10.5.1.6", "os": "Ubuntu 18.04", "total_gb": 150},

    # Client 7
    {"client_name": "Client 7", "vm_id": "C7VM1", "ip": "10.6.1.1", "os": "Debian 10", "total_gb": 150},
    {"client_name": "Client 7", "vm_id": "C7VM2", "ip": "10.6.1.2", "os": "Debian 10", "total_gb": 200},
    {"client_name": "Client 7", "vm_id": "C7VM3", "ip": "10.6.1.3", "os": "Debian 10", "total_gb": 250},
    {"client_name": "Client 7", "vm_id": "C7VM4", "ip": "10.6.1.4", "os": "Debian 10", "total_gb": 100},

    # Client 8
    {"client_name": "Client 8", "vm_id": "C8VM1", "ip": "10.7.1.1", "os": "CentOS 8", "total_gb": 900},
    {"client_name": "Client 8", "vm_id": "C8VM2", "ip": "10.7.1.2", "os": "CentOS 8", "total_gb": 800},
    {"client_name": "Client 8", "vm_id": "C8VM3", "ip": "10.7.1.3", "os": "CentOS 8", "total_gb": 750},
    {"client_name": "Client 8", "vm_id": "C8VM4", "ip": "10.7.1.4", "os": "CentOS 8", "total_gb": 600},
    {"client_name": "Client 8", "vm_id": "C8VM5", "ip": "10.7.1.5", "os": "CentOS 8", "total_gb": 550},
    {"client_name": "Client 8", "vm_id": "C8VM6", "ip": "10.7.1.6", "os": "CentOS 8", "total_gb": 400},
    {"client_name": "Client 8", "vm_id": "C8VM7", "ip": "10.7.1.7", "os": "CentOS 8", "total_gb": 300},

    # Client 9
    {"client_name": "Client 9", "vm_id": "C9VM1", "ip": "10.8.1.1", "os": "Windows Server 2012", "total_gb": 450},
    {"client_name": "Client 9", "vm_id": "C9VM2", "ip": "10.8.1.2", "os": "Windows Server 2012", "total_gb": 500},
    {"client_name": "Client 9", "vm_id": "C9VM3", "ip": "10.8.1.3", "os": "Windows Server 2012", "total_gb": 400}
]

# Simulation parameters
num_days = 60
hours_per_day = 24
total_hours = num_days * hours_per_day

# Simulation start date (now minus 60 days)
start_time = datetime.datetime.now() - datetime.timedelta(days=num_days)

random.seed(42)  # for reproducibility

# Ensure directory exists
output_dir = '/Users/akashninave/Akash_Drive/JOB HUNTER/LUCIDITY/client outputs'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'time_series_data.csv')

# Open CSV file to write
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow([
        'timestamp', 'client_name', 'vm_id', 'ip', 'os', 'total_gb', 'used_gb', 'free_gb', 'used_percent'
    ])

    for client in clients:
        # Simulate initial disk usage between 30% and 60% full
        used_gb = random.uniform(client["total_gb"] * 0.3, client["total_gb"] * 0.6)
        trend = random.uniform(0.03, 0.20)  # avg GB growth per hour

        for h in range(total_hours):
            timestamp = start_time + datetime.timedelta(hours=h)
            # Random fluctuation: sometimes a cleanup, sometimes a spike
            if random.random() < 0.01:
                # Sudden spike (huge log file, backup, etc.)
                used_gb += random.uniform(client["total_gb"] * 0.05, client["total_gb"] * 0.15)
            elif random.random() < 0.05:
                # Occasional cleanup (log rotation, temp files)
                used_gb -= random.uniform(client["total_gb"] * 0.01, client["total_gb"] * 0.07)
                used_gb = max(used_gb, 0)
            else:
                # Regular slow growth
                used_gb += trend + random.uniform(-0.02, 0.04)

            # Don't exceed disk size, don't go negative
            used_gb = min(max(used_gb, 0), client["total_gb"])
            free_gb = client["total_gb"] - used_gb
            used_percent = round(used_gb / client["total_gb"] * 100, 1)

            writer.writerow([
                timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                client["client_name"],
                client["vm_id"],
                client["ip"],
                client["os"],
                int(client["total_gb"]),
                round(used_gb, 2),
                round(free_gb, 2),
                used_percent
            ])

print(f"\nData generation complete! File: {output_file}\n")