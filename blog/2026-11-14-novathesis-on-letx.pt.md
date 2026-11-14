---
title: O template já abre no letx
date: 2026-11-14
summary: O letx aloja o novathesis e compila-o — a primeira via para o template que é gratuita e de um clique ao mesmo tempo.
image:
image_alt:
---

O [letx](https://letx.app/templates/universities/novathesis/) passou a ter o
**nova**thesis, e compila-o.

A frase é curta, por isso aqui fica o que justifica um post. Até agora as vias
para abrir o template no browser eram de dois tipos, e cada uma pedia-te
alguma coisa:

* O **Overleaf** e o **Inscrive** importam o repositório da tua escola num
  clique — e depois não o compilam sem plano pago. O template não cabe nos 20
  segundos que o plano gratuito do Overleaf permite.
* O **ScienHub** é gratuito, mas não consegue importar a partir de um link, por
  isso descarregas o ZIP da tua escola e carrega-lo à mão num projeto vazio.

O letx é o primeiro que é as **duas** coisas. É gratuito, abre o template num
clique, compila, e a única coisa que te pede é uma conta.

## Uma coisa que fica para ti

O projeto que o letx guarda é o template geral, não o repositório da tua
escola. Por isso o passo que as outras vias de um clique fazem por ti é aqui
teu: abre o `0-Config/1_novathesis.tex` e indica a tua escola.

```latex
\ntsetup{school=nova/fct}
```

Não tens de andar à procura do identificador. N’[A tua
escola](https://novathesis.org/pt/schools), cada linha tem agora um botão
**letx**, e a caixa que ele abre diz-te a linha exacta para essa escola —
incluindo aquelas em que o identificador não é simplesmente o nome
do repositório com os hífenes trocados por barras.

## Não leves o ZIP para lá

O conselho habitual para um serviço que não importa a partir de um link —
descarregar o ZIP, carregá-lo, definir o documento principal — é exactamente
aquilo que não funciona no letx. O template precisou de adaptação para compilar
no sistema deles, e o que eles adaptaram é o projeto que está por trás daquele
link. Um ZIP carregado por ti não compila.

Ou seja: a entrada é aquele link, e a cópia que está por trás dele é deles para
manterem actualizada — pode estar atrás da versão mais recente. Se precisas de
alguma coisa que entrou no template a semana passada, compila localmente ou
leva o repositório da tua escola a um dos outros serviços.

## Obrigado

O trabalho de adaptação foi feito no letx pelo **Shihab Shahriar**, que pôs o
template a compilar no sistema deles e o mantém lá gratuitamente. Os outros
dois nomes dos nossos
[agradecimentos](https://novathesis.org/pt/support) lá estão por contas que nos
emprestaram; este está lá por trabalho.
