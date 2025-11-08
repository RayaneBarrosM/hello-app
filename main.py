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