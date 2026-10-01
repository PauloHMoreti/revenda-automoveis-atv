# Front-end (templates)

Templates Jinja2 do Flask. O CSS fica em `app/static/style.css`.
Todas as páginas estendem `base.html`; os componentes reutilizáveis ficam em `_macros.html`.

## Rotas e variáveis esperadas

Cada template espera receber do backend as variáveis abaixo via `render_template`.
Os formulários fazem `POST` para a própria URL da página.

| Rota | Template | Variáveis |
| --- | --- | --- |
| `GET /` | `index.html` | `msg` (opcional) |
| `GET /clientes` | `clientes/lista.html` | `clientes`: lista com `id`, `nome`, `telefone`, `email` |
| `GET/POST /clientes/novo` | `clientes/form.html` | `cliente = None` |
| `GET/POST /clientes/<id>/editar` | `clientes/form.html` | `cliente` |
| `POST /clientes/<id>/excluir` | — | — |
| `GET /veiculos` | `veiculos/lista.html` | `veiculos`: lista com `id`, `placa`, `marca`, `modelo`, `ano` |
| `GET/POST /veiculos/novo` | `veiculos/form.html` | `veiculo = None` |
| `GET/POST /veiculos/<id>/editar` | `veiculos/form.html` | `veiculo` |
| `POST /veiculos/<id>/excluir` | — | — |
| `GET /mecanicos` | `mecanicos/lista.html` | `mecanicos`: lista com `id`, `nome`, `especialidade` |
| `GET/POST /mecanicos/novo` | `mecanicos/form.html` | `mecanico = None` |
| `GET/POST /mecanicos/<id>/editar` | `mecanicos/form.html` | `mecanico` |
| `POST /mecanicos/<id>/excluir` | — | — |
| `GET /servicos` | `servicos/lista.html` | `servicos`: lista com `id`, `descricao`, `valor` |
| `GET/POST /servicos/novo` | `servicos/form.html` | `servico = None` |
| `GET/POST /servicos/<id>/editar` | `servicos/form.html` | `servico` |
| `POST /servicos/<id>/excluir` | — | — |
| `GET /ordens` | `ordens/lista.html` | `ordens`: lista com `id`, `cliente`, `veiculo`, `placa`, `mecanico`, `servico`, `data_abertura` (date), `observacoes` — resultado do INNER JOIN |
| `GET/POST /ordens/nova` | `ordens/form.html` | `clientes`, `veiculos`, `mecanicos`, `servicos`, `hoje` (`AAAA-MM-DD`) |
| `GET /relatorios/mecanicos` | `relatorios/mecanicos.html` | `ranking`: lista com `nome`, `especialidade`, `total` — resultado do GROUP BY / COUNT |

As listas podem ser dicionários (`cursor(dictionary=True)`) ou objetos com esses atributos.

## Campos enviados pelos formulários

| Formulário | Campos (`request.form`) |
| --- | --- |
| Cliente | `nome`, `telefone`, `email` |
| Veículo | `placa`, `marca`, `modelo`, `ano` |
| Mecânico | `nome`, `especialidade` |
| Serviço | `descricao`, `valor` |
| Ordem de serviço | `cliente_id`, `veiculo_id`, `mecanico_id`, `servico_id`, `data_abertura`, `observacoes` |

## Mensagens

`base.html` exibe mensagens de `flash()`. Use a categoria `"sucesso"` ou `"erro"`:

```python
flash("Ordem de serviço cadastrada!", "sucesso")
```
