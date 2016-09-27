# WEB2CLINIC

Sistema para gerenciamento de clínicas médicas. Com funcionalidades que vão desde um simples cadastro de pacientes, até criação de uma consulta com possibilidade de inserção de atestados, exames, fichas e prescrições.


### Gerenciamento de pacientes:

No menu `Pacientes` > `Novo cadastro` você pode cadastrar as informações de uma paciente. Informações obrigatórias:
- Nome
- Telefone
- Data de nascimento

Informações opcionais:

- Tipo atendimento
- CPF
- Profissão
- Endereço
- Cidade
- UF
- CEP
- Sexo
- Escolaridade
- Estado Civil
- Cor
- Foto
- Observações

No menu `Pacientes` > `Todos cadastros` você pode ver uma lista paginada de todos os pacientes cadastrados, também é possível fazer uma pesquisa para encontrar um paciente em específico. Para cada registro de paciente, existem três botões:
- Visualizar
- Editar
- Deletar

Na página de visualização de um paciente em específico, você pode conferir todas as informações de cadastro. E também pode ver informações adicionais, como:
- Agendamentos
- Atestados
- Consultas
- Exames
- Prescrições


### Gerenciamento de agendamento

Através do menu `Agendamentos` > `Novo agendamento`, é possível fazer o agendamento de uma consulta para um paciente. A tela de `Novo agendamento` é parecida com a tela de `Todos cadastros`, porém ao invés de retornar os botões Visualizar, Editar e Apagar, a tela `Novo Agendamento` traz apenas um botão `Agendar` por paciente, que ao ser clicado vai redirecionar o usuário para um tela onde podem ser preenchidas informações sobre a data, hora e o tipo de agendamento(Consulta, Retorno).

Na tela `Agendamento` > `Ver todos agendamentos` é possível ver todos os agendamentos divididos por dia, semana e mês. Os agendamentos são exibidos num formato de calendário, exibindo para cada agendamento a hora de início e o nome do paciente. É possível selecionar um agendamento em específico apenas clicando no nome do paciente. Ao efetuar essa ação, o usuário é redirecionado para uma página onde constam informações sobre o paciente, o agendamento, e um formulário onde é possível salvar dados de uma pré-consulta(pressão, peso). Também é possível `Apagar` ou `Editar` um agendamento, assim como alterar o status do agendamento para `Paciente não compareceu`, e desta forma o agendamento deixa de ser exibido.


### Gerenciamento de consultas

É possível iniciar uma nova consulta através da página de agendamento ou do menu `Consultas` > `Nova consulta`. Sendo que neste último caso, a consulta **não** é atrelada a um agendamento, então o usuário deve selecionar o paciente que receberá a consulta.

Um consulta, no escopo do sistema, é uma tela onde é possível adicionar e listar as seguinter informações:
* **Atestados**: Um documento pré-definido e pronto para ser impresso com as informações do paciente e do médico responsável. Faltando apenas a assinatura do médico.
* **Exames**: Documentos pré-definidos para solicitação de exames. Exames podem ser cadastrados em `Admin` > `Cadastrar exame`.
* **Fichas**: Formulários e relatórios pré-definidos com uma grande variação dos campos. Por padrão, são disponibilizados as seguintes fichas:
   * Ficha Clínica Mulher
   * Ficha Clínica de Climaterio
   * Ficha Clínica de Anticoncepção
   * Ficha Clínica de Mastologia
   * Ficha Clínica de parto e Puerperio
   * Ficha Clínica de Pré Natal
   * Ficha Clínica de Uroginecologia
   * Ficha de Anticoncepção
   * Retorno

    Cada uma das fichas citadas acima conta com cerca de 100 campos cobrindo todos os aspectos necessários para um determinado tipo de consulta. Os campos são posicionados de uma maneira lógica e prática para o usuário.

    É possível a adição de novas fichas e relatórios. Para isso, é necessário a adição de dois arquivos html: Um deles com a composição dos campos do formulário e outro com a exibição das informações deste relatório. Também é necessário a criação de um novo `Modelo` para armazenar essas informações na base de dados. Após isso, todas essas informações devem ser inseridas em um arquivo de configuração. A partir deste ponto, a nova ficha já está disponível.

*  **Prescrição**: Documento pré-definido para gerar receitas. Os medicamentos podem ser cadastrados através do menu `Admin` > `Cadastrar medicamento`. Após o cadastro, podem ser selecionados pelo usuário e o sistema disponibilizará a prescrição pronta para ser impressa.

No menu `Consultas` > `Todas consultas` é possível ver uma lista de todas as consultas já realizadas. Assim como adicionar informações em uma consulta antiga. É disponibilizado também, um campo para busca, que pode ser utilizado para buscar consultas de um paciente em específico.


### Dashboard, ou, página inicial

Na página inicial do sistema são exibidos gráficos de várias informações relacionadas ao sistema. Como:
* Total de agendamentos em relação a consultas
* Total de pacientes cadastrados
* Total de agendamentos
* Total de consultas
* Total de consultas por tipo


_______________________

### Instalação

O sistema é desenvolvido em Python 2.7 e [web2py](http://www.web2py.com/), então para o funcionamento do sistema, é necessário fazer o download do framework em: http://www.web2py.com/init/default/download

Após fazer o download do framework, siga as instruções de execução do framework, que caso esteja no Linux será algo como:

```sh
$ unzip web2py_src.zip
$ cd web2py/
$ python web2py.py -a uma_senha_qualquer
```

Após isso, o sistema estará sendo executado em `localhost` na porta `:8000`.

Acesse o painel do administrador no endereço http://127.0.0.1:8000/admin e digite a senha definida na execução do web2py.

Neste painel, você pode fazer a importação do web2clinic. Para isso, acesse o repositório oficial do web2clinic em https://github.com/Marcelo-Theodoro/web2commerce e faça o download do arquivo `web2py.app.web2clinic.w2p`. Agora é só fazer o upload deste arquivo através do painel do administrador, que o sistema já estará disponível em http://127.0.0.1:8000/web2clinic.




Para mais informações, entre em contato com os desenvolvedores:

- Lucas Morais - lucasm310@gmail.com
- Marcelo Theodoro - marcelotheodoro@outlook.com
