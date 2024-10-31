import csv
from ping3 import ping
from django.shortcuts import render
from django.http import HttpResponse
from io import StringIO

def index(request):
    if request.method == 'POST' and 'button1' in request.POST:
        # Vérifier si le fichier est bien un CSV
        uploaded_file = request.FILES.get('file')
        if not uploaded_file.name.endswith('.csv'):
            return HttpResponse('Veuillez télécharger un fichier .csv')

        # Lire le contenu du fichier CSV
        file_data = uploaded_file.read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(file_data)

        # Variables pour stocker les résultats
        ping_results = []

        # Ping chaque adresse IP dans le fichier CSV
        for row in csv_reader:
            address = row['ip_address']
            server_name = row['server_name']
            
            try:
                # Utilisation de ping3 pour effectuer le ping
                response_time = ping(address, timeout=4)  # 4 secondes de timeout
                
                if response_time is not None:
                    ping_results.append({
                        'server_name': server_name,
                        'ip_address': address,
                        'reach': 'Yes',
                        'unreach': 'No',
                        'response_time': f'{response_time:.2f} ms'  # Temps de réponse en millisecondes
                    })
                else:
                    ping_results.append({
                        'server_name': server_name,
                        'ip_address': address,
                        'reach': 'No',
                        'unreach': 'Yes',
                        'response_time': 'N/A'
                    })
            except Exception as e:
                ping_results.append({
                    'server_name': server_name,
                    'ip_address': address,
                    'reach': 'No',
                    'unreach': 'Yes',
                    'response_time': 'N/A'
                })

        # Stocker les résultats dans la session pour les utiliser dans le téléchargement
        request.session['ping_results'] = ping_results

        # Renvoyer les résultats à la page HTML
        return render(request, 'app/index.html', {'ping_results': ping_results})
        
    return render(request, 'app/index.html')


def download_csv(request):
    # Récupérer les résultats de ping stockés dans la session
    ping_results = request.session.get('ping_results', [])
    
    # Créer une réponse HTTP avec le bon type MIME
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ping_results.csv"'

    # Créer l'écrivain CSV
    writer = csv.writer(response)
    
    # Écrire les en-têtes de colonnes
    writer.writerow(['Nom du serveur', 'Adresse IP', 'Atteignable', 'Non Atteignable', 'Temps de réponse'])

    # Écrire les données de chaque ligne
    for result in ping_results:
        writer.writerow([
            result['server_name'],
            result['ip_address'],
            result['reach'],
            result['unreach'],
            result['response_time']
        ])

    return response
