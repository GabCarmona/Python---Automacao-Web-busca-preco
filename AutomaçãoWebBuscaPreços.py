from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from  webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from time import sleep
import smtplib
import email.message

#Criar um Navegador
navegador = webdriver.Chrome()

#importar/visualizar a Base de Dados
produtos_df = pd.read_excel("buscas.xlsx")

def busca_google_shooping(navegador, produto, palavras_eliminatorias, valor_minimo, valor_maximo):
    #Entrar no google
    navegador.get("https://www.google.com.br/")

    #Tratar as informações que vieram da tabela
    produto = produto.lower()
    palavras_eliminatorias = palavras_eliminatorias.lower()
    lista_palavras_eliminatorias = palavras_eliminatorias.split(' ')
    lista_pala_chave_produto = produto.split(' ')
    valor_maximo = float(valor_maximo)
    valor_minimo = float(valor_minimo)

    #Pesquisar o nome do produto
    navegador.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(produto, Keys.ENTER)

    #Clicar na aba shopping
    lista = navegador.find_elements(By.CLASS_NAME, 'hdtb-mitem')
    for elemento in lista:
        if 'Shopping' in elemento.text:
            elemento.click()
            break
    #href = navegador.find_element(By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').get_attribute('href')
    #navegador.get(href)   --> o google muda a ordem dos botões de acordo com o tipo de pesquisa, buscar o href por meio do XPATH pode não ser a melhor opção

    
    # pegar a lista de resultados da busca no google shopping
    lista_resultados = navegador.find_elements(By.CLASS_NAME, 'sh-dgr__grid-result')

    # para cada resultado, verificar as condições e tratar as informações
    lista_ofertas = [] #lista de retorno
    for resultado in lista_resultados:
        nome = resultado.find_element(By.CLASS_NAME, 'tAxDx').text
        nome = nome.lower()

    # Tratando e verificando o nome do produto
        tem_termos_banidos = False
        for palavra in lista_palavras_eliminatorias:
            if palavra in nome:
                tem_termos_banidos = True
        
        tem_termos_produtos = True
        for palavra in lista_pala_chave_produto:
            if palavra not in nome:
                tem_termos_produtos = False
        
        if tem_termos_banidos == False and tem_termos_produtos:
            try:
                preco = resultado.find_element(By.CLASS_NAME, 'a8Pemb').text
                preco = preco.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
                preco = float(preco)

            #Verificando se o preço está entre os limites pré-definidos
                if valor_minimo <= preco <= valor_maximo:
                    elemento_link = resultado.find_element(By.CLASS_NAME, 'aULzUe')
                    elemento_pai = elemento_link.find_element(By.XPATH, '..') # Extraindo o link por meio do "parent" do elemento que foi possível acessar
                    link = elemento_pai.get_attribute('href')
                    lista_ofertas.append((nome, preco, link))
            except:
                continue

    return lista_ofertas
    
def busca_buscape(navegador, produto, palavras_eliminatorias, valor_minimo, valor_maximo):
    #Tratar valores
    valor_maximo = float(valor_maximo)
    valor_minimo = float(valor_minimo)
    produto = produto.lower()
    palavras_eliminatorias = palavras_eliminatorias.lower()
    lista_palavras_eliminatorias = palavras_eliminatorias.split(' ')
    lista_pala_chave_produto = produto.split(' ')

    #Entrar no buscape
    navegador.get("https://www.buscape.com.br/")
    navegador.find_element(By.CLASS_NAME, 'AutoCompleteStyle_textBox__MXJXH').send_keys(produto, Keys.ENTER)
    sleep(1)

    lista_resultados = navegador.find_elements(By.CLASS_NAME, 'SearchCard_ProductCard_Inner__7JhKb')
    lista_ofertas = []

    for resultado in lista_resultados:
        try:
            nome = resultado.find_element(By.CLASS_NAME, 'Text_DesktopLabelSAtLarge__baj_g').text
            nome = nome.lower()
            preco = resultado.find_element(By.CLASS_NAME, 'Text_MobileHeadingS__Zxam2').text   
            link = resultado.get_attribute('href')

            # Tratando e verificando o nome do produto
            tem_termos_banidos = False
            for palavra in lista_palavras_eliminatorias:
                if palavra in nome:
                    tem_termos_banidos = True
            
            tem_termos_produtos = True
            for palavra in lista_pala_chave_produto:
                if palavra not in nome:
                    tem_termos_produtos = False

            if tem_termos_banidos == False and tem_termos_produtos:
                    preco = preco.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
                    preco = float(preco)
                    if valor_minimo <= preco <= valor_maximo:
                        lista_ofertas.append((nome, preco, link))
        except:
            pass
    return lista_ofertas


tabela_ofertas = pd.DataFrame()
for linha in produtos_df.index:
    produto = produtos_df.loc[linha, 'Nome']
    palavras_eliminatorias = produtos_df.loc[linha, 'Termos banidos']
    valor_minimo = produtos_df.loc[linha, 'Preço mínimo']
    valor_maximo = produtos_df.loc[linha, 'Preço máximo']

    resultados_google = busca_google_shooping(navegador, produto, palavras_eliminatorias, valor_minimo, valor_maximo)
    if resultados_google:
        tabela_google_shopping = pd.DataFrame(resultados_google, columns=['Produto','Preço','Link'])
        tabela_ofertas = tabela_ofertas.append(tabela_google_shopping)
    else:
        tabela_google_shopping = None

    resultados_buscape = busca_buscape(navegador, produto, palavras_eliminatorias, valor_minimo, valor_maximo)
    if resultados_buscape:
        tabela_buscape = pd.DataFrame(resultados_buscape, columns=['Produto','Preço','Link'])
        tabela_ofertas = tabela_ofertas.append(tabela_buscape)
    else:
        tabela_buscape = None
    
#Exportar a tabela de ofertas para o excel
tabela_ofertas = tabela_ofertas.reset_index(drop=True)
tabela_ofertas.to_excel("Ofertas.xlsx", index=False)

#Enviar email --> só haverá envio se houver alguma oferta
if len(tabela_ofertas.index) > 0:
    corpo_email = f""" 
    <p>Alguns produtos desejados foram encontrados na faixa de preço pré-estabelecida. Segue tabela com detalhes</p>
    {tabela_ofertas.to_html(index=False)}
    """
    msg = email.message.Message()
    msg ['Subject'] = 'Produto(s) encontrado(s) na faixa de preço desejada'
    msg ['From'] = '<inserir email remetente'
    msg['To'] = '<inserir email destinatário'
    password = '<senha do gmail remetente>'

    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')

    
navegador.quit()
