# 🎯 Automação de Emissão de Certificados — Caso Real

## Contexto

Este projeto foi desenvolvido de forma voluntária para resolver um problema operacional real em um grupo escoteiro.

Após cada atividade, era necessário emitir certificados de participação para todas as crianças.  
O processo era totalmente manual: abrir um documento, editar nome por nome e imprimir.

Isso gerava consequências frequentes:

- participantes esquecidos
- erros de digitação
- retrabalho
- tempo excessivo após eventos
- dependência de uma única pessoa atenta

O problema não era técnico — era humano.  
Portanto, a solução precisava priorizar **redução de erro operacional**, não apenas automação.

---

## Objetivo

Criar uma ferramenta:

- simples o suficiente para qualquer responsável utilizar **sem treinamento técnico**
- confiável o suficiente para garantir que **nenhum participante fosse omitido**

### Critérios definidos

- **zero dependência de software externo**
- uso por **usuários não técnicos**
- impedir esquecimentos
- execução rápida após atividades
- padronização visual dos certificados

---

## Decisões de Engenharia

### Desktop ao invés de Web

Optado por aplicação local porque:

- uso offline em locais sem internet
- evitar login/senha para usuários leigos
- reduzir fricção de uso
- instalação inexistente (executável direto)

### Banco SQLite local

Motivação:

- persistência sem servidor
- zero configuração
- confiável para pequeno volume
- evita perda de cadastro

### Interface orientada à prevenção de erro

O sistema não apenas gera certificados — ele **impede falhas humanas**.

Implementações:

- seleção por checkbox ao invés de digitação
- exibição de quem **NÃO participou** antes de gerar
- histórico automático de atividades
- pré-visualização antes da emissão
- ajuste automático de tamanho de texto
- data por extenso automática

**Prioridade do design:**

> Reduzir decisões humanas, não acelerar digitação.

### Geração de PDF programática

Uso do **ReportLab** para:

- layout fixo
- padronização
- múltiplos certificados por folha
- evitar alterações manuais em Word

### Empacotamento para usuário leigo

Aplicação distribuída como `.exe`:

- sem necessidade de Python
- sem instalação
- sem permissões administrativas
- executável portátil

Isso foi essencial para adoção real.

---

## Resultado

### Antes

Processo manual pós-evento demorado e sujeito a falhas.

### Depois

Geração em minutos com garantia de consistência.

**Impactos observados:**

- eliminação de esquecimentos
- redução completa de retrabalho
- padronização do documento
- qualquer responsável consegue operar

---

## Tecnologias

- Python
- Tkinter
- SQLite
- ReportLab
- OpenPyXL
- PyInstaller

---

## Aprendizados

Este projeto demonstrou na prática que:

- qualidade de software não é apenas ausência de bugs — é **prevenção de erro humano**
- o foco não foi apenas automatizar, mas desenhar uma experiência **segura** para usuários não técnicos

---

## Sobre o projeto

Projeto voluntário aplicado em ambiente real com usuários reais.

Criado para melhorar organização e reconhecimento das crianças participantes, garantindo confiabilidade no processo.

---

## Autor

**Fernando Ferraz**
