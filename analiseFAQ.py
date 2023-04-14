import requests
from bs4 import BeautifulSoup
import pandas as pd

# ler arquivo CSV com as URLs
urls = pd.read_csv('urls.csv')

# criar listas vazias para os resultados
url_list = []
faq_list = []

# Loop pelas URLs
for url in urls['url']:
    # Fazer requisição HTTP
    response = requests.get(url)

    # Verificar se a resposta foi bem-sucedida
    if response.status_code == 200:
        # Extrair o conteúdo HTML da resposta
        html = response.content

        # Criar objeto BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Verificar se há dados estruturados de FAQ
        faq = soup.find_all('script', {'type': 'application/ld+json'})
        if faq:
            faq_list.append('Sim')
        else:
            # Verificar se há perguntas na página
            if soup.find_all(text='?'):
                faq_list.append('Não, mas há perguntas na página')
            else:
                faq_list.append('Não')

        # Adicionar a URL atual à lista de URLs
        url_list.append(url)

    else:
        print(f'Erro ao fazer requisição para a URL {url}')

# Criar o DataFrame com os resultados
resultados = pd.DataFrame({'URL': url_list, 'Dado Estruturado de FAQ?': faq_list})

# Exportar o DataFrame para um arquivo CSV
resultados.to_csv('resultados.csv', index=False)
