import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Iniciar o ChromeDriver
driver = webdriver.Chrome()

# Ler o arquivo CSV com as URLs
urls = pd.read_csv('urls.csv')

# Criar listas vazias para os resultados
url_list = []
faq_list = []

# Loop pelas URLs
for url in urls['url']:
    # Acessar a URL com o ChromeDriver
    driver.get(url)

    # Esperar até que o conteúdo seja carregado
    wait = WebDriverWait(driver, 10)
    try:
        faq_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    except:
        faq_list.append('Não foi possível carregar a página')
        url_list.append(url)
        continue

    # Extrair o conteúdo HTML da página renderizada
    html = driver.page_source

    # Criar objeto BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Verificar se há dados estruturados de FAQ
    faq = soup.find_all('script', {'type': 'application/ld+json'})
    faq_count = 0
    for script in faq:
        if 'FAQPage' in script.string:
            faq_count += 1
    if faq_count > 0:
        faq_list.append('Sim')
    else:
        # Verificar se há perguntas na página
        if '?' in soup.text:
            faq_list.append('Não, mas há perguntas na página')
        else:
            faq_list.append('Não')

    # Adicionar a URL atual à lista de URLs
    url_list.append(url)

# Fechar o ChromeDriver
driver.quit()

# Criar o DataFrame com os resultados
resultados = pd.DataFrame({'URL': url_list, 'Dado Estruturado de FAQ?': faq_list})

# Exportar o DataFrame para um arquivo CSV
resultados.to_csv('resultados.csv', index=False)
