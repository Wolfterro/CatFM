# Models

Este documento descreve os modelos usados em um projeto Django relacionado a streaming de áudio. Cada modelo é detalhado com suas respectivas propriedades e funcionalidades.

## **Modelos**

### **Genre**

Armazena os gêneros musicais.

- **Campos**:
  - `name`: Nome do gênero (único).

- **Métodos**:
  - `__str__`: Retorna o nome do gênero.
  - `populate`: Método estático para popular a tabela com gêneros musicais predefinidos.

---

### **Audio**

Armazena informações sobre arquivos de áudio.

- **Campos**:
  - `identifier`: Identificador único (UUID).
  - `name`: Nome do áudio.
  - `album`: Nome do álbum (opcional).
  - `artist`: Nome do artista (opcional).
  - `year`: Ano de lançamento.
  - `duration_in_seconds`: Duração em segundos.
  - `cover`: Arquivo da capa (opcional).
  - `cover_url`: URL da capa (opcional).
  - `genres`: Relacionamento *ManyToMany* com o modelo `Genre`.
  - `file`: Arquivo de áudio.
  - `format`: Formato do arquivo (ex.: mp3).
  - `md5`: Hash MD5 do arquivo para verificação de integridade.
  - `is_active`: Indica se o áudio está ativo.
  - `created_at`: Data de criação.
  - `updated_at`: Data da última atualização.

- **Métodos**:
  - `__str__`: Retorna uma string com o formato "Artista - Nome (Ano)".
  - `save`: Sobrescrito para calcular a duração e gerar o hash MD5 do arquivo, além de converter para o formato HLS.
  - **Propriedades**:
    - `folder`: Caminho completo da pasta onde o áudio está armazenado.
    - `cover_full_url`: URL completa da capa do áudio.
    - `file_stream_m3u8_url`: URL para transmissão HLS do áudio.
    - `genres_list`: Lista dos gêneros associados.

---

### **DownloadRequest**

Gerencia solicitações de download de áudios.

- **Campos**:
  - `audio`: Relacionamento com o modelo `Audio` (opcional).
  - `url`: URL do arquivo a ser baixado.
  - `title`: Título do áudio (opcional).
  - `requested_by`: Usuário que solicitou o download.
  - `status`: Status da solicitação (pendente, aprovado ou rejeitado).
  - `created_at`: Data de criação.
  - `updated_at`: Data da última atualização.
  - `approved_at`: Data de aprovação (opcional).

- **Métodos**:
  - `__str__`: Retorna uma string com o status e a URL da solicitação.
  - `register`: Registra o áudio baixado e associa à solicitação.
  - `set_info`: Obtém informações adicionais sobre a solicitação usando o serviço de download.
  - **Propriedades**:
    - `url_id`: Extrai o ID do vídeo da URL (se aplicável).

---

### **AdminRequest**

Gerencia requisições administrativas de download em massa.

- **Campos**:
  - `link_list`: Lista de links para download (como texto).
  - `link_list_file`: Arquivo contendo a lista de links (opcional).
  - `status`: Status da requisição (pendente, finalizado, erro ou em processo).
  - `link_status_description`: Descrição detalhada do status de cada link (opcional).
  - `created_at`: Data de criação.
  - `updated_at`: Data da última atualização.

- **Métodos**:
  - `__str__`: Retorna uma string com o status e a data de criação.
  - `save`: Sobrescrito para iniciar o serviço de download em segundo plano.
  - **Propriedades**:
    - `link_list_array`: Converte a lista de links em um array.

---

### **Playlist**

Armazena playlists de áudios.

- **Campos**:
  - `name`: Nome da playlist.
  - `identifier`: Identificador único (UUID).
  - `can_be_shared`: Indica se a playlist pode ser compartilhada.
  - `audios`: Relacionamento *ManyToMany* com o modelo `Audio`.
  - `owner`: Usuário dono da playlist (opcional).
  - `is_system_playlist`: Indica se a playlist é do sistema.
  - `created_at`: Data de criação.
  - `updated_at`: Data da última atualização.

- **Métodos**:
  - `__str__`: Retorna uma string com o status de compartilhamento e o nome da playlist.
  - `save`: Sobrescrito para configurar propriedades padrão para playlists do sistema.
  - **Propriedades**:
    - `cover`: Obtém a capa do primeiro áudio da playlist (se disponível).

---

## **Considerações**

Os modelos fornecem uma base robusta para gerenciar áudios, gêneros, solicitações de download, playlists e tarefas administrativas. Eles incluem lógica para automatizar tarefas, como processamento de arquivos e associação de dados, garantindo um fluxo de trabalho eficiente.
