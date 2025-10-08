# Data Mesh Implementation Framework

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Mermaid](https://img.shields.io/badge/Diagrams-Mermaid-orange?style=for-the-badge&logo=mermaid&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

---

## 🇧🇷 Framework de Implementação Data Mesh

Este repositório apresenta um **framework abrangente e prático para a implementação de uma arquitetura Data Mesh**, focando em princípios de **domínio de dados**, **dados como produto**, **plataforma de dados self-service** e **governança federada**. O objetivo é capacitar organizações a construir ecossistemas de dados descentralizados, escaláveis e orientados a negócios, promovendo a agilidade e a inovação através de exemplos de código funcional e bem documentado.

### 🎯 Objetivo

O principal objetivo deste projeto é **fornecer um guia detalhado e exemplos de código funcional** para profissionais de dados (engenheiros de dados, cientistas de dados, arquitetos de dados) que buscam implementar ou aprimorar uma arquitetura Data Mesh. Serão abordados desde os conceitos fundamentais até as melhores práticas de engenharia, governança e operação, com foco na criação de **Data Products** robustos e acessíveis.

### ✨ Destaques

- **Data Products Orientados a Domínio**: Implementação de classes `DomainDataProduct`, `SalesDataProduct` e `CustomerDataProduct` que encapsulam dados, metadados, lógica de acesso e métricas, demonstrando a propriedade de domínio e o tratamento de dados como produto.
- **Operações CRUD e Métricas**: Exemplos práticos de ingestão, consulta, atualização e remoção de dados, além da coleta de métricas de uso e acesso para cada Data Product, garantindo observabilidade e governança.
- **Estrutura Modular e Escalável**: O framework é projetado para ser modular, permitindo a fácil extensão e adaptação a diferentes domínios de negócio e requisitos de dados.
- **Testes Abrangentes**: Inclui testes unitários e de integração para todas as funcionalidades, assegurando a confiabilidade e a correção das implementações dos Data Products.
- **Documentação Detalhada**: Cada componente é acompanhado de explicações claras, diagramas e exemplos de uso, facilitando a compreensão e a aplicação dos conceitos de Data Mesh.

### 🏛️ Princípios do Data Mesh em Ação

O Data Mesh se baseia em quatro princípios fundamentais que orientam a descentralização e a democratização dos dados. Este framework ilustra como esses princípios podem ser aplicados na prática:

1.  **Domínio de Dados (Domain Ownership):** A responsabilidade pelos dados é descentralizada para as equipes de domínio. No nosso exemplo, `SalesDataProduct` e `CustomerDataProduct` são geridos por domínios específicos, que são responsáveis por sua ingestão, qualidade e disponibilização.

2.  **Dados como Produto (Data as a Product):** Os Data Products são tratados como produtos de primeira classe. Eles são discoverable (através de metadados), addressable (com APIs de acesso), trustworthy (com validação e métricas), self-describing (com schemas claros), interoperable e secure.

3.  **Plataforma de Dados Self-Service (Self-Serve Data Platform):** Embora não implementada como uma plataforma completa, o framework demonstra a abstração necessária para que os domínios possam criar e gerenciar seus Data Products de forma autônoma, utilizando interfaces padronizadas.

4.  **Governança Federada (Federated Computational Governance):** O framework inclui mecanismos para metadados e logs de acesso, que são a base para uma governança federada, permitindo que políticas globais sejam aplicadas enquanto os domínios mantêm autonomia operacional.

---

## 🇬🇧 Data Mesh Implementation Framework

This repository presents a **comprehensive and practical framework for implementing a Data Mesh architecture**, focusing on principles of **data domain ownership**, **data as a product**, **self-service data platform**, and **federated governance**. The goal is to empower organizations to build decentralized, scalable, and business-oriented data ecosystems, promoting agility and innovation through functional and well-documented code examples.

### 🎯 Objective

The main objective of this project is to **provide a detailed guide and functional code examples** for data professionals (data engineers, data scientists, data architects) looking to implement or improve a Data Mesh architecture. It will cover everything from fundamental concepts to best practices in engineering, governance, and operations, with a focus on creating robust and accessible **Data Products**.

### ✨ Highlights

- **Domain-Oriented Data Products**: Implementation of `DomainDataProduct`, `SalesDataProduct`, and `CustomerDataProduct` classes that encapsulate data, metadata, access logic, and metrics, demonstrating domain ownership and treating data as a product.
- **CRUD Operations and Metrics**: Practical examples of data ingestion, querying, updating, and removal, along with the collection of usage and access metrics for each Data Product, ensuring observability and governance.
- **Modular and Scalable Structure**: The framework is designed to be modular, allowing for easy extension and adaptation to different business domains and data requirements.
- **Comprehensive Testing**: Includes unit and integration tests for all functionalities, ensuring the reliability and correctness of the Data Product implementations.
- **Detailed Documentation**: Each component is accompanied by clear explanations, diagrams, and usage examples, facilitating the understanding and application of Data Mesh concepts.

### 🏛️ Data Mesh Principles in Action

Data Mesh is based on four fundamental principles that guide data decentralization and democratization. This framework illustrates how these principles can be applied in practice:

1.  **Domain Ownership:** Responsibility for data is decentralized to domain teams. In our example, `SalesDataProduct` and `CustomerDataProduct` are managed by specific domains, which are responsible for their ingestion, quality, and availability.

2.  **Data as a Product:** Data Products are treated as first-class products. They are discoverable (through metadata), addressable (with access APIs), trustworthy (with validation and metrics), self-describing (with clear schemas), interoperable, and secure.

3.  **Self-Serve Data Platform:** Although not implemented as a complete platform, the framework demonstrates the necessary abstraction for domains to create and manage their Data Products autonomously, using standardized interfaces.

4.  **Federated Computational Governance:** The framework includes mechanisms for metadata and access logs, which form the basis for federated governance, allowing global policies to be applied while domains maintain operational autonomy.

### 📊 Visualization

![Data Product Interaction](diagrams/data_product_interaction.png)

*Diagrama ilustrativo da interação entre os produtos de dados de domínio, suas fontes e consumidores, com foco na arquitetura de implementação.*


---

## 🛠️ Tecnologias Utilizadas / Technologies Used

| Categoria         | Tecnologia      | Descrição                                                                 |
| :---------------- | :-------------- | :------------------------------------------------------------------------ |
| **Linguagem**     | Python          | Linguagem principal para desenvolvimento dos Data Products.               |
| **Estrutura**     | Classes Python  | Implementação orientada a objetos para Data Products e metadados.         |
| **Serialização**  | JSON            | Formato para armazenamento de dados de exemplo e metadados.               |
| **Testes**        | `unittest`      | Framework de testes padrão do Python para validação de funcionalidades.   |
| **Diagramação**   | Mermaid         | Para criação de diagramas de arquitetura e fluxo de dados no README.      |

---

## 📁 Repository Structure

```
data-mesh-implementation-framework/
├── src/           # Código fonte e exemplos de implementação dos Data Products
├── data/          # Dados de exemplo (JSON) para simular ingestão e uso
├── images/        # Imagens e diagramas para o README e documentação
├── tests/         # Testes unitários e de integração para os Data Products
├── docs/          # Documentação adicional e guias detalhados (a ser expandido)
└── scripts/       # Scripts utilitários para automação (a ser expandido)
```

---

## 🚀 Getting Started

Para começar, clone o repositório e explore os diretórios `src/` e `data/` para exemplos detalhados e instruções de uso. Certifique-se de ter as dependências necessárias instaladas (Python 3.9+).

```bash
git clone https://github.com/GabrielDemetriosLafis/data-mesh-implementation-framework.git
cd data-mesh-implementation-framework
# Instale as dependências (se houver, neste caso, apenas Python padrão)
# pip install -r requirements.txt (se um requirements.txt for adicionado no futuro)
# Siga as instruções específicas em src/ e docs/
```

### Exemplo de Uso Avançado (Python)

O exemplo abaixo demonstra a criação, ingestão, consulta, atualização e remoção de dados para `CustomerDataProduct` e `SalesDataProduct`, além da interação com `DomainDataProduct` para gerenciamento de metadados e métricas. Este código ilustra como os princípios do Data Mesh são aplicados na prática.

```python
from src.domain_data_product import DataProductMetadata, DomainDataProduct
from src.sales_data_product import SalesDataProduct
from src.customer_data_product import CustomerDataProduct
import json

# Exemplo de uso
if __name__ == "__main__":
    print("\n==================================================")
    print("Demonstração do Framework de Implementação Data Mesh")
    print("==================================================")

    # --- 1. Inicialização e Ingestão de SalesDataProduct ---
    print("\n--- 1. Inicializando SalesDataProduct e Ingerindo Dados ---")
    sales_dp = SalesDataProduct(
        name="sales_transactions",
        description="Transações de vendas detalhadas",
        owner="sales-domain@example.com",
        version="1.0.0"
    )

    # Carregar dados de vendas de exemplo
    try:
        with open("data/sample_sales.json", "r") as f:
            sample_sales_data = json.load(f)
        for record in sample_sales_data:
            sales_dp.ingest_data(record)
        print(f"  {len(sample_sales_data)} registros de vendas ingeridos com sucesso.")
    except FileNotFoundError:
        print("  Erro: Arquivo data/sample_sales.json não encontrado. Certifique-se de que ele existe.")
    except Exception as e:
        print(f"  Erro ao ingerir dados de vendas: {e}")

    # --- 2. Inicialização e Ingestão de CustomerDataProduct ---
    print("\n--- 2. Inicializando CustomerDataProduct e Ingerindo Dados ---")
    customer_dp = CustomerDataProduct(
        name="customer_profiles",
        description="Perfis detalhados dos clientes",
        owner="customer-domain@example.com",
        version="1.0.0"
    )

    # Carregar dados de clientes de exemplo
    try:
        with open("data/sample_customers.json", "r") as f:
            sample_customers_data = json.load(f)
        for record in sample_customers_data:
            customer_dp.ingest_data(record)
        print(f"  {len(sample_customers_data)} registros de clientes ingeridos com sucesso.")
    except FileNotFoundError:
        print("  Erro: Arquivo data/sample_customers.json não encontrado. Certifique-se de que ele existe.")
    except Exception as e:
        print(f"  Erro ao ingerir dados de clientes: {e}")

    # --- 3. Consultando Dados ---
    print("\n--- 3. Consultando Dados ---")
    print("\n📊 Todas as transações de vendas:")
    all_sales = sales_dp.query()
    for sale in all_sales:
        print(f"  - Venda ID: {sale.get("transaction_id")}, Cliente: {sale.get("customer_id")}, Valor: {sale.get("amount")}")

    print("\n🔍 Consultando clientes de 'New York':")
    ny_customers = customer_dp.query({"city": "New York"})
    for customer in ny_customers:
        print(f"  - Cliente: {customer.get("name")}, Email: {customer.get("email")}")

    # --- 4. Atualizando Dados ---
    print("\n--- 4. Atualizando Dados ---")
    print("  Atualizando o email do cliente 'Alice' (CUST001)...")
    customer_dp.update_data("CUST001", {"email": "alice.new@example.com"})
    updated_alice = customer_dp.query({"customer_id": "CUST001"})
    if updated_alice: 
        print(f"  Email de Alice atualizado para: {updated_alice[0].get("email")}")

    # --- 5. Removendo Dados ---
    print("\n--- 5. Removendo Dados ---")
    print("  Removendo transação de vendas com ID 'TRN001'...")
    sales_dp.remove_data({"transaction_id": "TRN001"})
    remaining_sales = sales_dp.query({"transaction_id": "TRN001"})
    if not remaining_sales:
        print("  Transação TRN001 removida com sucesso.")
    else:
        print("  Falha ao remover transação TRN001.")

    # --- 6. Obtendo Métricas e Logs ---
    print("\n--- 6. Obtendo Métricas e Logs ---")
    print("\n📈 Métricas do SalesDataProduct:")
    sales_metrics = sales_dp.get_metrics()
    for key, value in sales_metrics.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for sub_key, sub_value in value.items():
                print(f"    - {sub_key}: {sub_value}")
        else:
            print(f"  - {key}: {value}")

    print("\n📜 Log de Acessos do CustomerDataProduct:")
    for log_entry in customer_dp.get_access_log():
        print(f"  - {log_entry}")

    print("\n==================================================")
    print("Demonstração Concluída.")
    print("==================================================")
```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, enviar pull requests ou sugerir melhorias. Por favor, siga as diretrizes de contribuição.

---

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**Autor:** Gabriel Demetrios Lafis  \n**Ano:** 2025