#
## Objetivo
## Ferramentas
erminal Ubuntu, sistema op Windows10, Docker, Docker Hub, Python
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Rancher](https://img.shields.io/badge/Rancher-0075A8?style=for-the-badge&logo=rancher&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![ArgoCD](https://img.shields.io/badge/ArgoCD-EF7B4D?style=for-the-badge&logo=argo&logoColor=white)
![Docker Hub](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Ubuntu](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Rancher-0075A8?style=for-the-badge&logo=rancher&logoColor=white)

# 🎯Passo a passo 
 📑 **Sumario**
 
1. Criando repositorios hello-app
1) Crie uma pasta onde será inicializado o repositório `hello-app`
2) Crie a pasta `.github` e dentro dele a pasta `workflows`, isso ativara a aba actions dentro do github para cada arquivo.yaml
3) Dentro da pasta `workflows` adicione  um arquivo `registry.yaml`
- O registry será o workflow responsavel por fazer jobs de build e update das imagens.
```
**comentar cada comando**
```
4) Fora do .github crie o arquivo main.py com o seguinte texto que ira criar criar uma pagina escrita **hello-app**
```
from fastapi import FastAPI 

app = FastAPI() 

@app.get("/") 
async def root(): 
	return {"message": "Hello World"}
```
5) Dockerfile
   O docker file é responsavel por criar a imagem do site e posiveis verisionamentos dela que ficarão guardados no dockerhub
```
**Colocar o dockerhub**
```

Ao final o seu repositorio hello-app deve aparecer assim:
```
Repositorio hello-app
      |
       - --------.github
      |              |
      - main.py     	 -- workflows
      |-dockerfile     				 |
           				 -- registry.yaml
```
Faça um push na finalização de cada arquivo por meio da chave ssh
caso não saiba fazer a chave ssh clique aqui
colocar isso no outro readme
```
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github-actions
ssh -T git@github.com
git remote -v
git remote set-url origin git@github.com:RayaneBarrosM/hello-app.git
git push -u origin main
ou ssh-keygen -t ed25519 -f ~/.ssh/github_manifests_deploy 
```
2. Criando repositorio hello-manifests
Na pasta manifestos crie dois arquivos o `deployment.yaml` e `service.yaml`
Ao final o seu repositorio manifest deve aparecer assim:
```
hello-manifests/
├── deployment.yaml
├── service.yaml
└── kustomization.yaml
```
4.
No seu Docker hub na aba Repositories deve aparecer a imagem da seguinte forma:
