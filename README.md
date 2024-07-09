# [MarketPLace]

## Introdução
Este é o README do projeto de API web Market Place, desenvolvido para a disciplina Programação Web. A API é uma ferramenta para visualização de produtos, gestão de produtos, carrinho de compras e usuários.

## Funcionalidades
● **Visualização do Carrinho**: Permite que usuários visualizem os itens no carrinho de compras.

● **Adicionar ao Carrinho**: Adiciona um produto específico ao carrinho.

● **Remover do Carrinho**: Remove um produto específico do carrinho.

● **Atualizar Quantidade**: Atualiza a quantidade de um produto no carrinho.

● **Visualização de Categorias**: Permite a visualização de produtos por categoria.

● **Cadastro de Usuário**: Permite que novos usuários se cadastrem na plataforma.

● **Login de Usuário**: Permite que usuários registrados façam login.

● **Logout de Usuário**: Permite que usuários façam logout.

● **Controle de acesso**: Controla as seções da aplicação que o usuário é permitido de acordo com um token JWC que é armazenado nos cookies do navegador.

● **Criação de Produtos**: Permite que novos produtos sejam adicionados ao catálogo.

## Requisitos
● **Python 3.8+**: Necessário para rodar a API.
● **FastAPI**: Framework para construção da API.
● **SQLAlchemy**: Biblioteca de ORM para gerenciar o banco de dados.
● **Passlib**: Biblioteca para hashing de senhas.

## Instalação
### Requisitos pré-requisitos:
● **Python 3.8+**
● **pip**: Instalador de pacotes Python.

### Instalação da API:
1. Clone o repositório:
    ```bash
    git clone https://github.com/joaoplima04/Eternize_ProWeb.git
    cd Eternize_ProWeb
    ```
2. Crie um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4. Configure as variáveis de ambiente no arquivo `.env`.
     ```bash
    SECRET_KEY = "sua_secret_key"
    ```

## Uso da API
### Endpoints:
1. **Visualização do Carrinho**:
    ● Endpoint: `GET /cart/`  
    ● Parâmetros: Nenhum  
    ● Exemplo de uso:
    ```bash
    curl -X GET "http://localhost:8000/cart/"
    ```
    
2. **Adicionar ao Carrinho**:
    ● Endpoint: `POST /cart/add_to_cart/{produto_id}/`  
    ● Parâmetros: 
        - `produto_id`: ID do produto que será adicionado ao carrinho  
    ● Exemplo de uso:
    ```bash
    curl -X POST "http://localhost:8000/cart/add_to_cart/1/"
    ```

3. **Remover do Carrinho**:
    ● Endpoint: `POST /cart/remove_from_cart/{produto_id}/`  
    ● Parâmetros: 
        - `produto_id`: ID do produto que será removido do carrinho  
    ● Exemplo de uso:
    ```bash
    curl -X POST "http://localhost:8000/cart/remove_from_cart/1/"
    ```

4. **Atualizar Quantidade**:
    ● Endpoint: `POST /cart/update_quantity/{produto_id}/{quantity}`  
    ● Parâmetros: 
        - `produto_id`: ID do produto  
        - `quantity`: Nova quantidade do produto no carrinho  
    ● Exemplo de uso:
    ```bash
    curl -X POST "http://localhost:8000/cart/update_quantity/1/3"
    ```

5. **Cadastro de Usuário**:
    ● Endpoint: `POST /users/cadastro_user/`  
    ● Parâmetros: 
        - `cpf`: CPF do usuário  
        - `username`: Nome de usuário  
        - `nome`: Nome completo  
        - `email`: Email do usuário  
        - `telefone`: Telefone do usuário  
        - `data_nascimento`: Data de nascimento  
        - `password`: Senha  
    ● Exemplo de uso:
    ```bash
    curl -X POST "http://localhost:8000/users/cadastro_user/" -d "cpf=12345678900&username=johndoe&nome=John Doe&email=johndoe@example.com&telefone=1234567890&data_nascimento=2000-01-01&password=senha"
    ```

6. **Login de Usuário**:
    ● Endpoint: `POST /users/login_user/`  
    ● Parâmetros: 
        - `email`: Email do usuário  
        - `password`: Senha  
    ● Exemplo de uso:
    ```bash
    curl -X POST "http://localhost:8000/users/login_user/" -d "email=johndoe@example.com&password=senha"
    ```

7. **Logout de Usuário**:
    ● Endpoint: `GET /users/logout`  
    ● Parâmetros: Nenhum  
    ● Exemplo de uso:
    ```bash
    curl -X GET "http://localhost:8000/users/logout"
    ```

8. **Visualização de Categorias**:
    ● Endpoint: `GET /categoria/{categoria_name}/`  
    ● Parâmetros: 
        - `categoria_name`: Nome da categoria para filtragem de produtos  
    ● Exemplo de uso:
    ```bash
    curl -X GET "http://localhost:8000/categories/categoria/GUARDANAPO/"
    ```

9. **Criação de Produtos**:
    ● Endpoint: `POST /produtos/cadastro`  
    ● Parâmetros: 
        - `produto`: Objeto JSON contendo os detalhes do produto (nome, categoria, preço, quantidade em estoque, cor, estilo, publicado)  
    ● Exemplo de uso:
    ```bash
    curl -X POST "http://localhost:8000/produtos/" -H "Content-Type: application/json" -d '{
      "nome": "Produto 1",
      "categoria": "PRATO_RASO",
      "preco": 100.0,
      "quantidade_estoque": 50,
      "cor": "Branco",
      "estilo": "ELEGANTE",
      "publicado": true
    }'
    ```

## Testes
### Testes disponíveis:
● **Teste 1**: Teste de integração para verificar a adição de produtos ao carrinho.
● **Teste 2**: Teste unitário para validar a autenticação de usuários.
● **Teste 3**: Teste de performance para medir a resposta dos endpoints.

#### Autenticação

**auth.py**:
Contém funções para criação e verificação de tokens JWT, além de funções para hashing e verificação de senhas.

### Observações Adicionais
- Certifique-se de que as variáveis de ambiente, especialmente `SECRET_KEY`, estejam corretamente configuradas no arquivo `.env`.
- Para iniciar o servidor, execute:
    ```bash
    uvicorn main:app --reload
    ```

## Contribuição
● **Contribuidor 1**: João Lucas Pereira Lima

