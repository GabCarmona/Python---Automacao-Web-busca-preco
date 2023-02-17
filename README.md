# Projeto Automação - Web Scraping
#### Desafio por HashtagTreinamentos
## DESCRIÇÃO DO PROJETO:
####
- Imagine que você trabalha na área de compras de uma empresa e precisa fazer uma comparação de fornecedores para os seus insumos/produtos.

- Nessa hora, você vai constantemente buscar nos sites desses fornecedores os produtos disponíveis e o preço, afinal, cada um deles pode fazer promoções em momentos diferentes e com valores distintos.

### Objetivo
####
- Definir uma faixa de preço - para cada produto - que lhe interesse, coletar todos os produtos que se encaixem nela e atualizar isso em uma planilha, porém realizando esse processo de forma automática, por meio de Web Scraping.
- Em seguida, enviar um e-mail com a lista dos produtos abaixo do seu preço máximo de compra.

- Nesse caso, faremos com produtos comuns em sites como Google Shopping e Buscapé, mas a ideia é a mesma para outros sites.

### Arquivos 

- Buscas.xlsx -> Planilha de Produtos, com os nomes dos produtos, o preço máximo, o preço mínimo (para evitar produtos "errados" ou "baratos de mais para ser verdade" e os termos que vamos querer evitar nas nossas buscas.

### Funcionamento

- Procurar cada produto no Google Shopping e pegar todos os resultados que tenham preço dentro da faixa e sejam os produtos corretos
- O mesmo para o Buscapé
- Enviar um e-mail (no caso da empresa seria para a área de compras por exemplo) com a notificação e a tabela com os itens e preços encontrados, junto com o link de compra.

### Bibliotecas Utilizadas:
- Pandas
- Selenium (webdriver, By, Keys)
- Time
- smtplib
- email.message

### Anexo do Email Enviado
![image](https://user-images.githubusercontent.com/118035572/219525759-e3ad6db7-3bcb-4c74-a6cd-1f8c557531dc.png)


### Considerações Finais
#### O programa digita o nome do produto no google e "aperta" enter para buscar, após isso, clica na aba de "shopping" e coleta todos os produtos que estão na faixa de custo pré-definida e com seu nome de acordo com os termos necessários e termos banidos. Os resultados são salvos em um planilha. Após isso, o programa abre o site do Buscapé e realiza o mesmo procedimento, tudo de forma automática, rápida e eficiente, utilizando o Selenium. Ao final, temos uma tabela com todas as ofertas encontradas, que é enviada para o e-mail desejado. Um vídeo do funcionamento do programa estará disponível no meu perfil do LinkedIn: https://www.linkedin.com/in/gabrielcarmona1/
