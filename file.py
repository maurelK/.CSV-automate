import csv
import subprocess

# It's here that we willstock our IP_address and the Location
liste_pi_address = []
Location = []

# Read our CSV file in function of our delimitor(try to chech if the delimitor is ';' or ',')
with open('ip_house.csv', mode='r', newline='', encoding='utf-8') as fichier:
    reader = csv.DictReader(fichier)
    for ligne in reader:
        region = ligne['ip_address']
        name = ligne['server_name']
        liste_pi_address.append(region)
        Location.append(name)

# You know this part where in function of your parameter(IP_address and the Location) you will test your ping
def ping_server(ip_address, server_name):
    print(f"Pinging {server_name} ({ip_address})...")
    try:
        # Ping command execution
        result = subprocess.run(['ping', '-c', '10', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(f" {server_name} is reachable ({ip_address})\n")
        else:
            print(f"{server_name} unreachable ({ip_address})\n")
    except Exception as e:
        print(f"Erreur lors du ping de {server_name} : {e}")

for ip, name in zip(liste_pi_address, Location):
    ping_server(ip, name)
