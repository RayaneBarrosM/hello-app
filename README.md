# Projeto de CI/CD no GitActions
## Objetivo
Automatizar completamente o ciclo de desenvolvimento, build, entrega e deploy (CI/CD) de uma aplicação web em Python (FastAPI).
## Ferramentas
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![ArgoCD](https://img.shields.io/badge/ArgoCD-EF7B4D?style=for-the-badge&logo=argo&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Hub](https://img.shields.io/badge/Docker_Hub-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Rancher](https://img.shields.io/badge/Rancher-0075A8?style=for-the-badge&logo=rancher&logoColor=white)

### **📚 Versionamento e Aplicação**
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

### **💻 Sistemas Operacionais dos terminais**
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

# 🎯Passo a passo 
 📑 **Sumário**
1. [Criação do Repositório hello-app](#1-criação-do-repositório-hello-app)
2. [Criação do Repositório hello-manifests](#2-criação-do-repositório-hello-manifests)
3. [Configuração de Chaves SSH e Secrets](#3-configuração-de-chaves-ssh-e-secrets)
4. [Configuração do ArgoCD](#4-configuração-do-argocd)
5. [Teste do Pipeline CI/CD](#5-teste-do-pipeline-cicd)

## 1. Criando repositórios hello-app
Esta etapa consiste em criar a aplicação FastAPI e configurar a automação de CI/CD.

1) Crie uma pasta onde será inicializado o repositório `hello-app`
2) Crie a pasta `.github` e dentro dele a pasta `workflows`, isso ativará a aba actions dentro do github para cada arquivo.yaml
3) Dentro da pasta `workflows` adicione  um arquivo `registry.yaml`
- O registry será o workflow responsável por fazer jobs de build e update das imagens.
```
name: workflow

# Trigger: executa automaticamente a cada push na branch main
on: 
  push: 
    branches:
      - main

# Variáveis de ambiente reutilizáveis no workflow
env:
  DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
  DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
  TAG: ${{ github.sha }}

jobs:
  # Job 1: Build e push da imagem Docker
  build-dockerhub:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: . 
    steps:
      - name: Checkout app code
        uses: actions/checkout@v4   # Baixa o código do repositório
        
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ env.DOCKER_USERNAME }}   
          password: ${{ env.DOCKER_PASSWORD }}
          
      - name: Build and push Docker image    
        uses: docker/build-push-action@v5
        with:
          push: true			    # Habilita o push para Docker Hub
          tags: ${{ env.DOCKER_USERNAME }}/hello-app:${{ env.TAG }} # Tag da imagem

  # Job 2: Atualização dos manifests Kubernetes
  update-manifest:       
    runs-on: ubuntu-latest
    needs: build-dockerhub			# Executa apenas após o build
    defaults:
      run:
        working-directory: .  
    env:    
      SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }} #Chave SSH para acesso ao repo de manifests
      
    steps:
      - name: Setup SSH Agent
        uses: webfactory/ssh-agent@v0.9.0
        with:
          ssh-private-key: ${{ env.SSH_PRIVATE_KEY }}
          
      - name: Checkout manifests repo
        uses: actions/checkout@v4
        with:
          repository: usuario_github/hello-manifests # Repositório destino 
          ref: main
          ssh-key: ${{env.SSH_PRIVATE_KEY}}
          
      - name: Update image tag in kustomization
        run: |
          sed -i 's|newTag:.*|newTag: ${{ env.TAG }}|' kustomization.yaml
          
      - name: Commit and push changes
        run: |
          git config user.name "github-actions"
          git config user.email "github-actions@github.com"
          git add kustomization.yaml
          git commit -m "Update image tag to ${{ env.TAG }}"
          git push
```

4) Fora do `.github` crie os arquivos:

 **main.py** 
```
from fastapi import FastAPI 
from fastapi.responses import HTMLResponse

app=FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <html>
        <head>
            <title>Sobre o projeto</title>
            <style>
                body {
                    background-color: #A6A3A1;
                    color: #403C3A;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-family: Manrope, sans-serif;
                }
                h1 {
                    font-size: 2rem;
                }
                .square{
                    padding: 1rem;
                    background-color: #F2ECE4;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    text-align: center;
                    border-radius: 20px;
                }
            </style>
        </head>
        <body>    
            <div class="square">
                <h1>Projeto CI/CD no GitActions</h1>
                <p>Este projeto tem como objettivo utomatizar o ciclo de desenvolvimento, build, entrega e deploy (CI/CD) de uma aplicação web em Python (FastAPI)</p>
                <p><strong>Tecnologias utilizadas:</strong> FastAPI, Docker, GitHub Actions, Kubernetes, ArgoCD</p>
            </div>
        </body>
    </html>
    """
    return html_content    
```
**Dockerfile**

```
# Imagem base do Python 3.11
FROM python:3.11-slim

# Definir diretório dentro do container
WORKDIR /app

# Copiar arquivo de dependências 
COPY requirements.txt .

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Expor a porta que a aplicação vai rodar
EXPOSE 8000

# Comando para iniciar a aplicação com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
**requiriments.txt**

Crie o arquivo requirements.txt, ele ajudará com as dependências
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
```
Ao final a estrutura do seu repositório hello-app deve aparecer assim:
```
hello-app/
├── .github/
│   └── workflows/
│       └── registry.yaml          # Pipeline de CI/CD
├── main.py                        # Aplicação FastAPI
├── Dockerfile                     # Configuração do container
└── requirements.txt               # Dependências do Python
```

## 2. Criando repositorio hello-manifests
Na pasta manifestos crie três arquivos:

**deployment.yaml**:
```
# Define o tipo de recurso
apiVersion: apps/v1
kind: Deployment
metadata:
  # Nome do seu deployment
  name: hello-app-deployment
  labels:
    app: hello-app
spec:
  # O ArgoCD (ou a Action) irá alterar este valor (tag)
  replicas: 1 
  selector:
    matchLabels:
      app: hello-app
  template:
    metadata:
      labels:
        app: hello-app
    spec:
      containers:
      - name: hello-app-container
        # IMPORTANTE: Esta imagem será atualizada pela sua GitHub Action!
        # Use 'latest' como placeholder inicial, mas a Action o substituirá pelo SHA do commit.
        image: rayane001/hello-app:latest 
        ports:
        - containerPort: 8000 # A porta que o FastAPI (uvicorn) expõe no container
        # Você pode adicionar variáveis de ambiente aqui, se necessário
        env:
        - name: PYTHONUNBUFFERED
          value: "1"
```
**service.yaml**:
```
# Define o tipo de recurso
apiVersion: v1
kind: Service
metadata:
  # Nome do seu Service (usado para acesso interno)
  name: hello-app-service
  labels:
    app: hello-app
spec:
   # Seleciona os pods com o label app: hello-app
  selector:
    app: hello-app 
  ports:
    # Porta que o Service expõe internamente
    - protocol: TCP
      port: 8080 # Porta que você acessará via 'port-forward' (Etapa 5)
      targetPort: 8000 # A porta real exposta pelo container (containerPort no Deployment)
  # Tipo de Service. ClusterIP é o padrão para acesso interno. 
  # Você usará 'port-forward' para acessar de fora.
  type: ClusterIP
```
**kustomization.yaml**:
```
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- deployment.yaml
- service.yaml
images:
- name: rayane001/hello-app
  newTag: latest  # ← Será atualizado automaticamente
```
Ao final o seu repositorio manifest deve aparecer assim:
```
hello-manifests/
├── deployment.yaml
├── service.yaml
└── kustomization.yaml
```

🔗 **[Clique aqui para ver o repositório de manifests completo](https://github.com/RayaneBarrosM/hello-app)**
## 3. Chaves ssh
Nesta seção geraremos e colocaremos as chaves de acesso no repositório
### 3.1 Criando uma chave 
Para criar uma chave ssh execute os seguintes comandos:
```
ssh-keygen -t ed25519 -f ~/.ssh/github_manifests_deploy
```
### 3.2 Deploy Key
1) Nas configurações do repositorio `hello-manifests`
2) Clique no menu lateral em `Deploy keys` -> `Add deploy key`
<img width="644" height="642" alt="image" src="https://github.com/user-attachments/assets/10020259-637e-4655-bdcb-b862be4ca10f" />
3) Execute `cat ~/.ssh/github_manifests_deploy.pub`
4) Nomeie a chave como `ManifestDeployment-key` e cole a chave copiada no comando anterior
5) Marque allow write access
6) Add key

### 3.3 Secrets
1) Vá na aba Secrets and variables no menu lateral 
2) clique em `New repository secret`
<img width="644" height="244" alt="image" src="https://github.com/user-attachments/assets/99b32404-3b2e-4d85-b5eb-e976d08d1726" />

3) Execute o comando `cat ~/.ssh/github_manifests_deploy` para pegar o conteudo da chave
4) Nomeie como SSH_Private_Key e cole a chave no secret
<img width="644" height="360" alt="image (1)" src="https://github.com/user-attachments/assets/468f9085-619f-4256-b37c-1fc645ceba09" />

5) Adicione um novo secret e nomeie como `DOCKER_USERNAME`
6) Secret: coloque seu usuario do DockerHub
7) Adicione um novo secret e nomeie como docker `DOCKER_PASSWORD`
8) Va nas configurações do seu perfil do DockerHub
9) Clique em **Personal access tokens** -> Generate new token
10) Nomeie e de permissão de `Read, Write, Delete`
11) `Generate`
12) Secret: Cole o token gerado

- Ao final voce deve ter DOCKER_PASSWORD, DOCKER_USERNAME e SSH_PRIVATE_KEY
<img width="633" height="243" alt="image" src="https://github.com/user-attachments/assets/9660c697-32ba-48dd-9e19-c78226689f6a" />

🔍Caso de erro `**Error:** Command failed: ssh-add - Enter passphrase for (stdin)` ao dar **push** no repositório é porque  a sua chave **tem senha** e o git não tem capacidade de autenticá-la. Para resolver execute no terminal o comando `ssh-keygen -p -f ~/.ssh/github_manifests_deploy`

- Coloque a senha atual e de enter nas próximas perguntas.
- Atualize a SSH_PRIVATE_KEY nas actions
- Va em **Deploy keys** e delete a chave antiga
- Cole o conteúdo do arquivo `.pub`
- Marque allow write access

## 4. Aplicação
1) Abra o Rancher Desktop e o powershell e espere 5 minutos para inicialização completa
2) Verifique se esta funcionando com `kubectl get nodes`
3) Execute no terminal
```
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String((kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}")))
``` 
- Este comando te permitirá pegar a senha de login do ArgoCD
5) Execute `kubectl port-forward svc/argocd-server -n argocd 8080:443`
6) Acesse: [https://localhost:8080](https://localhost:8080/)
7) Ao abrir a tela do argocd logue com admin e utilize a senha que foi apresentada anteriormente
8) clique no botão `create application`
9) Configuração da aplicação:
- Application Name: hello-app
- Project: default
- Sync Policy: Automatic

Source:
- Repository URL: https://github.com/SEU_USUARIO/hello-manifests
- Revision: HEAD
- Path: .

Destination:
- Cluster URL: https://kubernetes.default.svc
- Namespace: default

9) Clique em "Create"
10)  Após criação, clique em **Sync** -> **Synchronize**
11)  Verifique se o aplicativo aparece como "Healthy" e "Synced"
<img width="425" height="320" alt="image" src="https://github.com/user-attachments/assets/2aaeaf75-0ed7-4659-88d4-b8055c2dbcef" />

- Ou pelo comando `kubectl get application -n argocd`
- <img width="545" height="32" alt="image" src="https://github.com/user-attachments/assets/6f77cbce-d650-4c50-88f2-7e36176d1fa3" />

📢Caso esteja Unhealthy verifique os logs com `kubectl logs -l app=hello-app`

## 5. Teste
1) Para parar o Argo aperte  `Ctrl+C`
1) Para verificar o funcionamento execute `kubectl get svc hello-app-service`
2) Para acessar a aplicação execute `kubectl port-forward svc/hello-app-service 8000:8080`
3) Acesse: http://localhost:8000 
<img width="1125" height="348" alt="image" src="https://github.com/user-attachments/assets/66dd0db7-4201-4421-97a3-b2335aa476d3" />

## 📝Como deve estar funcionando ao final:
1. Push no código → Dispara o GitHub Actions
2. Build da imagem → Cria container com a aplicação
3. Push para Docker Hub → Armazena a imagem no registry
4. Atualização de manifests → Modifica o kustomization.yaml
5. ArgoCD detecta mudanças → Faz deploy automático no Kubernetes
