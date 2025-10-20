# Exemplos / Examples

Esta pasta contém exemplos práticos de uso do Data Mesh Implementation Framework.

## 📝 Exemplos Disponíveis

### 1. basic_example.py

Demonstra o uso básico do framework:
- Criação de Data Products (Sales e Customer)
- Publicação de Data Products
- Adição de dados com validação
- Consultas e filtragem de dados
- Obtenção de métricas
- Criação de segmentos de clientes
- Integração entre Data Products
- Análise de linhagem de dados

**Como executar:**

```bash
# A partir do diretório raiz do projeto
python examples/basic_example.py
```

**Saída esperada:**

O exemplo irá:
1. ✅ Criar e publicar um SalesDataProduct
2. ✅ Adicionar 3 transações de vendas
3. ✅ Consultar dados de vendas
4. ✅ Exibir métricas de vendas (receita total, média, etc.)
5. ✅ Demonstrar todas as funcionalidades principais do framework

## 🚀 Criando Seus Próprios Exemplos

Use os exemplos acima como referência para criar seus próprios casos de uso:

1. Importe os módulos necessários do pacote `src`
2. Crie instâncias de Data Products
3. Configure metadados, schemas e SLAs apropriados
4. Adicione e valide dados
5. Execute operações CRUD
6. Obtenha métricas e relatórios de qualidade

## 📚 Estrutura Básica de um Exemplo

```python
import sys
import os

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import SalesDataProduct, CustomerDataProduct

def main():
    # Seu código aqui
    pass

if __name__ == "__main__":
    main()
```

## 🔗 Recursos Adicionais

- [README Principal](../README.md)
- [Documentação de API](../README.md#-api-documentation)
- [Princípios do Data Mesh](../docs/data_mesh_principles.md)
- [Guia de Contribuição](../CONTRIBUTING.md)
