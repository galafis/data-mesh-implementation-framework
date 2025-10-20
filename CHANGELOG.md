# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2025-10-20

### Adicionado
- Implementação completa do `DomainDataProduct` com suporte a metadados, schema e SLA
- `SalesDataProduct` com métricas específicas de vendas e validações
- `CustomerDataProduct` com segmentação dinâmica de clientes
- Integração com World Bank API através do módulo `api_integration.py`
- Suite completa de testes unitários e de integração (38 testes)
- Configuração de CI/CD com GitHub Actions
- Suporte para operações CRUD (Create, Read, Update, Delete)
- Sistema de logging de acessos para auditoria
- Validação de qualidade de dados com relatórios detalhados
- Métodos para gerenciamento de dependências entre Data Products
- Carregamento de dados de arquivos JSON
- Documentação completa em português e inglês
- Exemplos práticos de uso
- Diagramas de arquitetura Data Mesh

### Arquivos de Configuração
- `.gitignore` para Python
- `setup.py` para instalação do pacote
- `requirements.txt` com dependências
- `LICENSE` MIT
- `CONTRIBUTING.md` com guia de contribuição
- `CHANGELOG.md` (este arquivo)
- `.github/workflows/tests.yml` para CI/CD

### Documentação
- README.md bilíngue (PT-BR/EN) com exemplos detalhados
- `docs/data_mesh_principles.md` explicando os 4 princípios fundamentais
- Diagramas de interação entre Data Products
- Exemplos de código executáveis

### Testes
- 38 testes unitários e de integração
- Cobertura de código > 80%
- Testes para validação de dados
- Testes para operações CRUD
- Testes de integração entre Data Products

## [Unreleased]

### Planejado
- Dashboard de monitoramento de Data Products
- Catálogo de dados interativo
- Suporte para mais fontes de dados (SQL, NoSQL, APIs)
- Automação de deployment
- Documentação em formato de site estático
- Exemplos com dados reais de diferentes domínios
- Suporte para governança federada automatizada
- Templates para novos Data Products
