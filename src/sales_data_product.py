
"""
Sales Data Product - Data Mesh Implementation Framework
Author: Gabriel Demetrios Lafis
Year: 2025

Este módulo demonstra um produto de dados de vendas em uma arquitetura Data Mesh,
utilizando o DomainDataProduct como base para gerenciamento de dados e metadados.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from collections import defaultdict

from .domain_data_product import DomainDataProduct, DataProductMetadata, DataSchema, DataProductSLA, DataProductStatus, DataQualityLevel


class SalesDataProduct(DomainDataProduct):
    """
    Representa um produto de dados de vendas em um Data Mesh, estendendo DomainDataProduct.
    
    Este produto de dados é de propriedade do domínio de vendas e fornece
    dados sobre transações de vendas, métricas de performance e análises.
    """
    
    def __init__(self, name: str, owner: str, domain: str = "Sales",
                 version: str = "1.0.0", description: str = "Sales transactions and analytics data product"):
        
        # Definir metadados específicos para vendas
        metadata = DataProductMetadata(
            name=name,
            version=version,
            domain=domain,
            owner=owner,
            description=description,
            tags=["sales", "transactions", "revenue", "customers"],
            quality_level=DataQualityLevel.SILVER # Começa como SILVER, pode ser GOLD após validação
        )
        
        # Definir schema específico para vendas
        schema = DataSchema(
            fields={
                "transaction_id": "string",
                "product_id": "string",
                "customer_id": "string",
                "amount": "float",
                "date": "string", # Formato YYYY-MM-DD
                "product_category": "string",
                "region": "string"
            },
            primary_key="transaction_id",
            indexes=["product_id", "customer_id", "date"]
        )
        
        # Definir SLA para vendas
        sla = DataProductSLA(
            availability=99.9,
            freshness=60, # 60 minutos de latência máxima
            completeness=99.0,
            accuracy=99.0
        )
        
        super().__init__(metadata, schema, sla)
        self._sales_metrics: Dict[str, Any] = {}
        self._update_sales_metrics() # Inicializa as métricas

    def add_data(self, sale_data: Dict[str, Any]) -> bool:
        """
        Adiciona dados de venda ao Data Product, com validações adicionais.
        """
        if not self._validate_sale_data(sale_data):
            print(f"✗ Falha ao adicionar dados: Validação de dados de venda falhou para {sale_data.get('transaction_id', 'N/A')}")
            return False
        
        if not super().add_data(sale_data):
            return False
        
        self._update_sales_metrics()
        return True

    def _validate_sale_data(self, sale_data: Dict[str, Any]) -> bool:
        """
        Valida dados de venda específicos, além do schema básico.
        """
        # Validação de campos obrigatórios (já coberto pelo schema, mas reforça)
        required_fields = ["transaction_id", "product_id", "customer_id", "amount", "date", "product_category", "region"]
        if not all(field in sale_data for field in required_fields):
            print(f"✗ Dados de venda incompletos. Campos obrigatórios: {required_fields}")
            return False
        
        # Validação de formato de data
        try:
            datetime.strptime(sale_data["date"], "%Y-%m-%d")
        except ValueError:
            print(f"✗ Formato de data inválido para {sale_data['date']}. Esperado YYYY-MM-DD.")
            return False

        # Validação de valor de amount
        if not isinstance(sale_data["amount"], (int, float)) or sale_data["amount"] <= 0:
            print(f"✗ Valor de 'amount' inválido para {sale_data['amount']}. Deve ser um número positivo.")
            return False
        
        # Validação de unicidade de transaction_id (exemplo simples, em produção usaria um DB)
        if any(record["transaction_id"] == sale_data["transaction_id"] for record in self._data_store):
            print(f"✗ transaction_id {sale_data['transaction_id']} já existe. Transações devem ser únicas.")
            return False

        return True

    def _update_sales_metrics(self) -> None:
        """
        Atualiza as métricas de vendas do produto de dados.
        """
        if not self._data_store:
            self._sales_metrics = {
                "total_revenue": 0.0,
                "total_transactions": 0,
                "average_transaction_value": 0.0,
                "sales_by_category": {},
                "sales_by_region": {},
                "top_customers_by_revenue": [],
                "last_metrics_update": datetime.now().isoformat()
            }
            return
        
        total_revenue = sum(sale["amount"] for sale in self._data_store)
        total_transactions = len(self._data_store)
        average_transaction_value = total_revenue / total_transactions if total_transactions > 0 else 0
        
        sales_by_category = defaultdict(float)
        sales_by_region = defaultdict(float)
        customer_revenue = defaultdict(float)

        for sale in self._data_store:
            sales_by_category[sale.get("product_category", "Unknown")] += sale["amount"]
            sales_by_region[sale.get("region", "Unknown")] += sale["amount"]
            customer_revenue[sale.get("customer_id", "Unknown")] += sale["amount"]
        
        top_customers = sorted(customer_revenue.items(), key=lambda item: item[1], reverse=True)[:5]

        self._sales_metrics = {
            "total_revenue": round(total_revenue, 2),
            "total_transactions": total_transactions,
            "average_transaction_value": round(average_transaction_value, 2),
            "sales_by_category": dict(sales_by_category),
            "sales_by_region": dict(sales_by_region),
            "top_customers_by_revenue": top_customers,
            "last_metrics_update": datetime.now().isoformat()
        }
    
    def get_sales_metrics(self) -> Dict[str, Any]:
        """
        Retorna as métricas de vendas do produto de dados.
        """
        return self._sales_metrics
    
    def get_sales_by_product_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Retorna todas as vendas de uma categoria de produto específica.
        """
        return self.query({"product_category": category})

    def get_sales_by_region(self, region: str) -> List[Dict[str, Any]]:
        """
        Retorna todas as vendas de uma região específica.
        """
        return self.query({"region": region})

    def get_data_quality_report(self) -> Dict[str, Any]:
        """
        Gera um relatório de qualidade de dados mais detalhado.
        """
        report = super().get_metrics() # Usa métricas básicas do DomainDataProduct
        
        total_records = report.get("total_records", 0)
        if total_records == 0:
            return {"message": "No data to generate quality report."}

        # Contagem de valores nulos por campo
        null_counts = defaultdict(int)
        for record in self._data_store:
            for field_name in self.schema.fields.keys():
                if record.get(field_name) is None or record.get(field_name) == "":
                    null_counts[field_name] += 1
        
        completeness_by_field = {
            field: round((1 - null_counts[field] / total_records) * 100, 2)
            for field in self.schema.fields.keys()
        }

        # Validação de unicidade para transaction_id
        transaction_ids = [record["transaction_id"] for record in self._data_store if "transaction_id" in record]
        unique_transaction_ids = len(set(transaction_ids))
        duplicate_transactions = total_records - unique_transaction_ids
        uniqueness_rate = round((unique_transaction_ids / total_records) * 100, 2)

        # Validação de range para 'amount'
        invalid_amounts = sum(1 for record in self._data_store if not (isinstance(record.get("amount"), (int, float)) and record["amount"] > 0))
        amount_validity_rate = round((1 - invalid_amounts / total_records) * 100, 2)

        # Validação de formato de data
        invalid_dates = 0
        for record in self._data_store:
            date_str = record.get("date")
            if date_str:
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    invalid_dates += 1
            else:
                invalid_dates += 1 # Considerar nulo como inválido para este check
        date_validity_rate = round((1 - invalid_dates / total_records) * 100, 2)

        # Comparar com SLA
        meets_completeness_sla = completeness_by_field.get("transaction_id", 0) >= self.sla.completeness
        meets_uniqueness_sla = uniqueness_rate >= 100 # Idealmente 100% para IDs
        meets_amount_sla = amount_validity_rate >= self.sla.accuracy # Usando accuracy para amount
        meets_date_sla = date_validity_rate >= self.sla.accuracy # Usando accuracy para data

        return {
            "total_records": total_records,
            "completeness_by_field": completeness_by_field,
            "uniqueness_transaction_id": {
                "rate": f"{uniqueness_rate:.2f}%",
                "duplicates_found": duplicate_transactions,
                "meets_sla": meets_uniqueness_sla
            },
            "amount_validity": {
                "rate": f"{amount_validity_rate:.2f}%",
                "invalid_records": invalid_amounts,
                "meets_sla": meets_amount_sla
            },
            "date_format_validity": {
                "rate": f"{date_validity_rate:.2f}%",
                "invalid_records": invalid_dates,
                "meets_sla": meets_date_sla
            },
            "overall_completeness_sla_target": f"{self.sla.completeness}%",
            "overall_completeness_meets_sla": meets_completeness_sla and meets_uniqueness_sla and meets_amount_sla and meets_date_sla
        }


if __name__ == "__main__":
    print("=" * 80)
    print("Sales Data Product - Advanced Example")
    print("=" * 80)

    sales_product = SalesDataProduct(
        name="Enterprise Sales Transactions",
        owner="Global Sales Team",
        version="2.0.0",
        description="Data product containing all enterprise sales transactions with enhanced quality checks."
    )
    
    # Publicar o Data Product (inicialmente)
    sales_product.publish()

    # Adicionar algumas vendas de exemplo
    sample_sales_data = [
        {
            "transaction_id": "TXN001", "product_id": "PROD123", "customer_id": "CUST456",
            "amount": 150.00, "date": "2025-10-01", "product_category": "Electronics", "region": "North America"
        },
        {
            "transaction_id": "TXN002", "product_id": "PROD124", "customer_id": "CUST457",
            "amount": 200.00, "date": "2025-10-02", "product_category": "Books", "region": "Europe"
        },
        {
            "transaction_id": "TXN003", "product_id": "PROD123", "customer_id": "CUST456",
            "amount": 300.50, "date": "2025-10-03", "product_category": "Electronics", "region": "North America"
        },
        {
            "transaction_id": "TXN004", "product_id": "PROD125", "customer_id": "CUST458",
            "amount": 50.25, "date": "2025-10-03", "product_category": "Apparel", "region": "Asia"
        },
        {
            "transaction_id": "TXN005", "product_id": "PROD124", "customer_id": "CUST457",
            "amount": 120.00, "date": "2025-10-04", "product_category": "Books", "region": "Europe"
        },
        {
            "transaction_id": "TXN006", "product_id": "PROD126", "customer_id": "CUST459",
            "amount": 75.00, "date": "2025-10-05", "product_category": "Home Goods", "region": "North America"
        },
        # Dados com problemas para testar validações
        {
            "transaction_id": "TXN007", "product_id": "PROD127", "customer_id": "CUST460",
            "amount": -10.00, "date": "2025-10-06", "product_category": "Electronics", "region": "North America"
        }, # Amount inválido
        {
            "transaction_id": "TXN008", "product_id": "PROD128", "customer_id": "CUST461",
            "amount": 500.00, "date": "invalid-date", "product_category": "Books", "region": "Europe"
        }, # Data inválida
        {
            "transaction_id": "TXN001", "product_id": "PROD129", "customer_id": "CUST462",
            "amount": 99.99, "date": "2025-10-07", "product_category": "Apparel", "region": "Asia"
        } # transaction_id duplicado
    ]
    
    for data in sample_sales_data:
        sales_product.add_data(data)
    
    print("\n" + "=" * 30 + " Sales Metrics " + "=" * 30)
    print(json.dumps(sales_product.get_sales_metrics(), indent=2))
    
    print("\n" + "=" * 30 + " Data Quality Report " + "=" * 24)
    print(json.dumps(sales_product.get_data_quality_report(), indent=2))

    print("\n" + "=" * 30 + " Query Examples " + "=" * 30)
    # Consultar vendas por categoria
    electronics_sales = sales_product.get_sales_by_product_category("Electronics")
    print(f"\nTotal de vendas de Electronics: {len(electronics_sales)} registros")
    # for sale in electronics_sales:
    #     print(f"  - {sale['transaction_id']}: {sale['amount']}")

    # Consultar vendas por região
    na_sales = sales_product.get_sales_by_region("North America")
    print(f"Total de vendas na América do Norte: {len(na_sales)} registros")
    # for sale in na_sales:
    #     print(f"  - {sale['transaction_id']}: {sale['amount']}")

    # Consultar vendas de um cliente específico (usando o método query do DomainDataProduct)
    customer_sales = sales_product.query({"customer_id": "CUST456"})
    print(f"\nTotal de vendas para CUST456: {len(customer_sales)} registros")
    for sale in customer_sales:
        print(f"  - {sale['transaction_id']}: R$ {sale['amount']:.2f} ({sale['product_category']})")

    # Atualizar uma venda
    print("\nAtualizando valor da transação TXN002...")
    sales_product.update_data({"transaction_id": "TXN002"}, {"amount": 220.00, "region": "South America"})
    updated_sale = sales_product.query({"transaction_id": "TXN002"})
    if updated_sale:
        print(f"Transação TXN002 atualizada: {updated_sale[0]['amount']:.2f} na região {updated_sale[0]['region']}")
    
    # Remover uma venda
    print("\nRemovendo transação TXN005...")
    sales_product.remove_data({"transaction_id": "TXN005"})
    remaining_sales = sales_product.query({"transaction_id": "TXN005"})
    if not remaining_sales:
        print("Transação TXN005 removida com sucesso.")

    print("\n" + "=" * 80)
    print("Exemplo Concluído")
    print("=" * 80)


