# CatFM - Um Projeto Simples de Serviço de Streaming de Música em Python

![Badge Estático](https://img.shields.io/badge/Python-3.9_%7C_3.10_%7C_3.11_%7C_3.12-blue)
![Badge Estático](https://img.shields.io/badge/Licença-Licença_MIT-green)
![Badge Estático](https://img.shields.io/badge/Cobertura_de_Testes-29_%25-red)

# CatFM

CatFM é um projeto simples de serviço de streaming de música com Python, que usa o
framework Django e Django Channels. O projeto é dividido em três apps principais:
`catuser`, `radio` e `streaming`. O app `catuser` é responsável por gerenciar a
autenticação e a gestão de usuários, o app `radio` é responsável por criar streams
de rádio ao vivo e o app `streaming` é responsável por criar playlists e reproduzir
músicas.

O projeto ainda está em desenvolvimento e não deve ser usado em produção.

## Visão Geral dos Apps

### catuser

O app `catuser` é responsável por gerenciar a autenticação e a gestão de usuários.
Ele fornece a infraestrutura necessária para o registro de usuários, login e
gerenciamento de credenciais de usuários. O app integra com o sistema de
autenticação do Django e o estende como necessário para atender aos requisitos
específicos do projeto CatFM. Ele inclui modelos para armazenar dados de usuários
e APIs para lidar com operações de usuário.

### radio

O app `radio` facilita a criação e o gerenciamento de streams de rádio ao vivo.
Ele usa tecnologia WebSocket para transmitir arquivos de áudio continuamente por
canais selecionados. O app permite que os administradores gerenciem arquivos de
áudio, adicionem ou removam arquivos usando a interface de administração do
Django e criem vários canais de rádio. Esses canais podem transmitir diferentes
gêneros ou tipos de música. O app inclui modelos para representar streams de rádio
e seus atributos, bem como serviços para lidar com a lógica de transmissão e
conexões WebSocket.

### streaming

O app `streaming` é projetado para reprodução de música on-demand. Ele fornece
aos usuários a capacidade de solicitar e reproduzir diferentes arquivos de áudio
conforme necessário. O app inclui funcionalidades para gerenciar conteúdo de
áudio, baixar novas faixas e lidar com solicitações de música. Os administradores
podem aprovar ou rejeitar essas solicitações por meio de uma API e gerenciar a
visibilidade do conteúdo. O app também suporta a criação de playlists, permitindo
que os usuários criem playlists com base em suas preferências. Os modelos no app
armazenam metadados sobre os arquivos de áudio e playlists, e as APIs permitem
interação com o serviço de streaming.

## Capturas de Tela

![Audio Streaming](https://github.com/Wolfterro/CatFM/blob/master/docs/screenshots/screenshot01.png?raw=true)

![Radio List](https://github.com/Wolfterro/CatFM/blob/master/docs/screenshots/screenshot02.png?raw=true)

![Radio Stream List](https://github.com/Wolfterro/CatFM/blob/master/docs/screenshots/screenshot03.png?raw=true)

![Radio Broadcast Info](https://github.com/Wolfterro/CatFM/blob/master/docs/screenshots/screenshot04.png?raw=true)

![Admin Requests](https://github.com/Wolfterro/CatFM/blob/master/docs/screenshots/screenshot05.png?raw=true)

## Licença

```txt
MIT License

Copyright (c) 2024 Wolfgang Almeida

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

Para mais informações sobre o projeto, visite o repositório do GitHub:
https://github.com/Wolfterro/CatFM