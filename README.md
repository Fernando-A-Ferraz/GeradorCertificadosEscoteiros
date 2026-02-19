🎖️ Gerador de Certificados Escoteiros

Sistema desktop desenvolvido em Python para automatizar a emissão de certificados de participação em atividades escoteiras.

Projeto voluntário criado para apoiar o grupo escoteiro da minha filha, eliminando falhas humanas no processo manual de emissão de certificados e garantindo que todas as crianças participantes sejam reconhecidas corretamente.

📌 Problema

A geração dos certificados era feita manualmente:

Digitação nome por nome

Risco de esquecer participantes

Erros de ortografia

Retrabalho constante

Processo demorado após cada atividade

Isso impactava diretamente a organização e a experiência das crianças.

💡 Solução

Foi desenvolvido um aplicativo desktop simples e direto ao ponto que:

✔ Controla cadastro de membros
✔ Permite selecionar quem participou da atividade
✔ Gera múltiplos certificados automaticamente
✔ Garante que ninguém fique de fora
✔ Reduz o tempo de emissão de horas para minutos

🖥️ Interface

O usuário apenas:

Marca quem participou

Preenche dados da atividade

Clica em gerar

O sistema faz todo o resto.

⚙️ Funcionalidades
Cadastro

Cadastro de membros por seção

Busca rápida

Remoção com duplo clique

Participação

Seleção por checkbox

Marcar todos / desmarcar todos

Evita esquecimentos

Certificados

Geração automática (3 por folha A4)

Ajuste automático de tamanho do nome

Data por extenso

Layout padronizado

Produtividade

Histórico de atividades (dropdown automático)

Pré-visualização antes de gerar

Importação de membros via Excel/CSV

Exportação dos participantes da atividade

Distribuição

Aplicação empacotada em .exe

Usuários não precisam instalar Python

🧠 Tecnologias utilizadas

Python 3

Tkinter (interface gráfica)

ReportLab (geração de PDF)

SQLite (banco local)

OpenPyXL (importação Excel)

PyInstaller (empacotamento)

📁 Estrutura
app.py
membros.db
logo_grupo.png
Certificado_limpo.png
historico_atividades.txt

🚀 Como executar
Usuário comum

Basta abrir:

Certificados_Escoteiros.exe


Nenhuma instalação necessária.

Desenvolvedor
pip install -r requirements.txt
python app.py

🏗️ Motivação

Esse projeto nasceu de uma necessidade real.

Em trabalhos voluntários, tempo e organização são limitados.
Automatizar esse processo permitiu que os responsáveis focassem no mais importante: a experiência das crianças, não em tarefas repetitivas.

📈 Resultado

Antes:

Processo manual

Alto risco de erro

Tempo longo após cada evento

Depois:

Geração em minutos

Nenhum participante esquecido

Processo padronizado

🤝 Contribuição

Projeto aberto para melhorias futuras:

Assinatura digital

Envio automático por e-mail

Integração com planilhas online

Multi-grupos

👨‍💻 Autor

Desenvolvido por Fernando Ferraz
Projeto voluntário para apoio educacional e organizacional.