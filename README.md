# CatFM

CatFM é um pequeno projeto de software desenvolvido em Python utilizando o framework Django e tem como objetivo ser o backend principal do streaming de áudio.

Ele irá conter duas ferramentas principais:

- Radio
- Streaming 

## Radio

A aplicação de rádio irá ser responsável por fazer o streaming contínuo dos arquivos de áudio selecionados para serem transmitidos em um canal selecionado utilizando a tecnologia de WebSockets.

O administrador da rádio irá conseguir gerir os arquivos a serem adicionados ou removidos utilizando o CRM do Django. Haverá também a possibilidade de criar múltiplos canais de transmissão que serão responsáveis por transmitir diferentes tipos de música que forem selecionadas.

## Streaming

A aplicação de streaming irá ser responsável por fornecer sob demanda diferentes arquivos de áudio para o usuário.

O administrador ficará encarregado de baixar novas músicas utilizando ferramentas de gerenciamento internas e até mesmo aprovar solicitações de download de novas músicas para o serviço (uma API ficará responsável por isso, o usuário irá mandar o link do YouTube contendo o áudio desejado e o administrador irá aprovar ou recusar o pedido utilizando o CRM do Django).

O administrador também terá a possibilidade de desativar áudios que violem as regras estabelecidas pelo serviço, se assim for necessário.

## Funcionalidades Extras

### Cadastro de Músicas

As músicas poderão ser cadastradas pelo administrador do serviço ou requisitadas para download.

O administrador, em ambos os casos, ficará encarregado de cadastrar corretamente o título, o autor, o nome do álbum, a capa (se houver), o ano e os gêneros musicais daquele áudio.

O administrador terá todas as prerrogativas para aprovar ou recusar solicitações de download de novos arquivos de música. Caso a música seja aprovada, ela deverá constar na seção de novas mídias no front-end ou na aplicação Android.

### Aplicações

O backend irá servir aplicações desenvolvidas em Vue (catfm-frontend) e Android (catfm-android). Estas aplicações serão responsáveis por fazer a interface com o backend e com isso fornecer aos usuários o serviço de streaming e de rádio.

A aplicação Android deverá possuir a capacidade de utilizar a rádio e o streaming de músicas de forma que, se a tela do celular for bloqueada, ela deverá continuar a tocar.

### Login

O front-end e o aplicativo deverão implementar o login de usuário, que após o cadastro realizado diretamente pelo administrador utilizando o CRM do Django, deverão logar antes de utilizar os serviços.

As contas deverão possuir um e-mail e uma senha. Em caso de perda do e-mail ou da senha, o usuário deverá solicitar a alteração das credenciais ao administrador do sistema.

### Playlists

Os usuários terão a possibilidade de criar playlists baseadas em seus gostos, além de utilizar as playlists já criadas pelo administrador do serviço. Playlists poderão ser compartilhadas e configuradas como Pública (podendo assim ser compartilhada) ou Privada (sem compartilhamento, mesmo com link). Playlists compartilhadas serão copiadas para o usuário que requisitar, caso haja interesse.

## Existência do Projeto

<s>Mano, nem fudendo eu vou pagar R$ 21,90 pro YouTube Music pra ouvir música que eu já tenho kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk</s>

A razão principal da existência deste projeto é criar um projeto completo de serviço de streaming de músicas de forma simples e descomplicada de modo que eu futuramente possa utilizar, de modo inteiramente pessoal, e que também sirva como um grande portfólio de desenvolvimento de software.

Desta forma, eu estarei desenvolvendo em três diferentes camadas: Back-end, Front-end e Mobile.
