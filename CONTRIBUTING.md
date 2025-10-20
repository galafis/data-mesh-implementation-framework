# Contributing to Data Mesh Implementation Framework

🎉 Primeiro, obrigado por dedicar seu tempo para contribuir!

As seguintes diretrizes ajudarão você a contribuir para este projeto. Estas são principalmente diretrizes, não regras. Use seu bom senso e sinta-se à vontade para propor alterações a este documento em um pull request.

## Código de Conduta

Este projeto e todos que participam dele são regidos por nosso Código de Conduta. Ao participar, espera-se que você mantenha este código. Por favor, reporte comportamento inaceitável.

## Como posso contribuir?

### Reportando Bugs

Esta seção orienta você sobre como enviar um relatório de bug. Seguir essas diretrizes ajuda os mantenedores e a comunidade a entender seu relatório, reproduzir o comportamento e encontrar relatórios relacionados.

**Antes de criar relatórios de bugs**, por favor verifique a lista de issues existentes, pois você pode descobrir que não precisa criar um novo.

#### Como enviar um bom relatório de bug?

Bugs são rastreados como [GitHub issues](https://github.com/galafis/data-mesh-implementation-framework/issues). Crie uma issue e forneça as seguintes informações:

* **Use um título claro e descritivo** para identificar o problema.
* **Descreva os passos exatos para reproduzir o problema** com o máximo de detalhes possível.
* **Forneça exemplos específicos** para demonstrar os passos.
* **Descreva o comportamento observado** e explique qual comportamento você esperava ver.
* **Inclua capturas de tela** se relevante.
* **Se o problema não foi acionado por uma ação específica**, descreva o que você estava fazendo antes de o problema acontecer.

### Sugerindo Melhorias

Esta seção orienta você sobre como enviar uma sugestão de melhoria, incluindo recursos completamente novos e melhorias menores na funcionalidade existente.

#### Como enviar uma boa sugestão de melhoria?

Sugestões de melhorias são rastreadas como [GitHub issues](https://github.com/galafis/data-mesh-implementation-framework/issues). Crie uma issue e forneça as seguintes informações:

* **Use um título claro e descritivo** para identificar a sugestão.
* **Forneça uma descrição passo a passo da melhoria sugerida** com o máximo de detalhes possível.
* **Forneça exemplos específicos** para demonstrar os passos.
* **Descreva o comportamento atual** e **explique qual comportamento você esperaria ver** e por quê.
* **Explique por que essa melhoria seria útil** para a maioria dos usuários.

### Seu Primeiro Código de Contribuição

Não tem certeza por onde começar a contribuir? Você pode começar procurando por issues marcadas como `good first issue` e `help wanted`:

* **Good first issues** - issues que geralmente requerem apenas algumas linhas de código e um ou dois testes.
* **Help wanted issues** - issues que podem ser um pouco mais envolventes do que issues para iniciantes.

### Pull Requests

O processo descrito aqui tem vários objetivos:

- Manter a qualidade do projeto
- Corrigir problemas que são importantes para os usuários
- Engajar a comunidade trabalhando em direção ao melhor framework possível
- Permitir um sistema sustentável para os mantenedores revisarem as contribuições

Por favor, siga estas etapas para que sua contribuição seja considerada pelos mantenedores:

1. **Fork o repositório** e crie sua branch a partir de `main`.
2. **Se você adicionou código que deve ser testado, adicione testes**.
3. **Se você mudou APIs, atualize a documentação**.
4. **Certifique-se de que o conjunto de testes passa**.
5. **Certifique-se de que seu código segue o estilo de código existente**.
6. **Emita esse pull request**!

#### Convenções de Estilo

* Use 4 espaços para indentação (não tabs)
* Use docstrings para documentar funções e classes
* Siga PEP 8 para estilo de código Python
* Escreva mensagens de commit claras e significativas

#### Estrutura de Branch

* `main` - branch estável para releases
* `develop` - branch de desenvolvimento
* `feature/*` - branches de recursos
* `bugfix/*` - branches de correção de bugs
* `hotfix/*` - branches de correção urgente

#### Mensagens de Commit

* Use o tempo presente ("Add feature" não "Added feature")
* Use o modo imperativo ("Move cursor to..." não "Moves cursor to...")
* Limite a primeira linha a 72 caracteres ou menos
* Referencie issues e pull requests liberalmente após a primeira linha

Exemplo:
```
Add customer segmentation feature

- Implement segment creation logic
- Add tests for segment operations
- Update documentation

Closes #123
```

### Testes

* Escreva testes para todo código novo
* Mantenha alta cobertura de testes (>80%)
* Execute todos os testes antes de enviar um pull request
* Execute testes com: `python -m pytest tests/ -v`

### Documentação

* Mantenha README.md atualizado
* Adicione docstrings a todas as funções e classes públicas
* Atualize exemplos se necessário
* Adicione comentários para código complexo

## Recursos Adicionais

* [Princípios do Data Mesh](docs/data_mesh_principles.md)
* [Issues do GitHub](https://github.com/galafis/data-mesh-implementation-framework/issues)
* [Pull Requests](https://github.com/galafis/data-mesh-implementation-framework/pulls)

## Agradecimentos

Obrigado por contribuir para o Data Mesh Implementation Framework! 🙏
