"""
Sales Data Product - Data Mesh Implementation Framework
Author: Gabriel Demetrios Lafis
Year: 2025

Este módulo demonstra um produto de dados de vendas em uma arquitetura Data Mesh.
"""

from typing import Dict, List, Any
from datetime import datetime
import json


class SalesDataProduct:
    """
    Representa um produto de dados de vendas em um Data Mesh.
    
    Este produto de dados é de propriedade do domínio de vendas e fornece
    dados sobre transações de vendas, métricas de performance e análises.
    """
    
    def __init__(self, name: str, owner: str, domain: str = "Sales"):
        """
        Inicializa um produto de dados de vendas.
        
        Args:
            name: Nome do produto de dados
            owner: Proprietário do produto de dados (equipe ou indivíduo)
            domain: Domínio ao qual o produto pertence (padrão: Sales)
        """
        self.name = name
        self.owner = owner
        self.domain = domain
        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "schema_version": "1.0",
            "data_quality_sla": "99.9%",
            "update_frequency": "daily"
        }
        self.sales_data: List[Dict[str, Any]] = []
        self.metrics: Dict[str, Any] = {}
    
    def add_sale(self, sale_data: Dict[str, Any]) -> None:
        """
        Adiciona uma transação de venda ao produto de dados.
        
        Args:
            sale_data: Dicionário contendo informações da venda
        """
        required_fields = ["transaction_id", "product_id", "customer_id", "amount", "date"]
        if not all(field in sale_data for field in required_fields):
            raise ValueError(f"Sale data must contain all required fields: {required_fields}")
        
        self.sales_data.append(sale_data)
        self._update_metrics()
    
    def _update_metrics(self) -> None:
        """Atualiza as métricas do produto de dados."""
        if not self.sales_data:
            return
        
        total_revenue = sum(sale["amount"] for sale in self.sales_data)
        total_transactions = len(self.sales_data)
        average_transaction_value = total_revenue / total_transactions if total_transactions > 0 else 0
        
        self.metrics = {
            "total_revenue": total_revenue,
            "total_transactions": total_transactions,
            "average_transaction_value": average_transaction_value,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_sales_by_product(self, product_id: str) -> List[Dict[str, Any]]:
        """
        Retorna todas as vendas de um produto específico.
        
        Args:
            product_id: ID do produto
            
        Returns:
            Lista de vendas do produto
        """
        return [sale for sale in self.sales_data if sale["product_id"] == product_id]
    
    def get_sales_by_customer(self, customer_id: str) -> List[Dict[str, Any]]:
        """
        Retorna todas as vendas de um cliente específico.
        
        Args:
            customer_id: ID do cliente
            
        Returns:
            Lista de vendas do cliente
        """
        return [sale for sale in self.sales_data if sale["customer_id"] == customer_id]
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Retorna as métricas do produto de dados.
        
        Returns:
            Dicionário com métricas
        """
        return self.metrics
    
    def export_data(self) -> str:
        """
        Exporta os dados do produto em formato JSON.
        
        Returns:
            String JSON com os dados
        """
        export = {
            "name": self.name,
            "owner": self.owner,
            "domain": self.domain,
            "metadata": self.metadata,
            "sales_data": self.sales_data,
            "metrics": self.metrics
        }
        return json.dumps(export, indent=2)
    
    def get_data_quality_report(self) -> Dict[str, Any]:
        """
        Gera um relatório de qualidade de dados.
        
        Returns:
            Dicionário com informações de qualidade
        """
        total_records = len(self.sales_data)
        complete_records = sum(1 for sale in self.sales_data if all(sale.values()))
        completeness_rate = (complete_records / total_records * 100) if total_records > 0 else 0
        
        return {
            "total_records": total_records,
            "complete_records": complete_records,
            "completeness_rate": f"{completeness_rate:.2f}%",
            "sla_target": self.metadata["data_quality_sla"],
            "meets_sla": completeness_rate >= 99.9
        }


if __name__ == "__main__":
    # Exemplo de uso
    sales_product = SalesDataProduct(
        name="Monthly Sales Transactions",
        owner="Sales Analytics Team"
    )
    
    # Adicionar algumas vendas de exemplo
    sales_product.add_sale({
        "transaction_id": "TXN001",
        "product_id": "PROD123",
        "customer_id": "CUST456",
        "amount": 150.00,
        "date": "2025-10-01"
    })
    
    sales_product.add_sale({
        "transaction_id": "TXN002",
        "product_id": "PROD124",
        "customer_id": "CUST457",
        "amount": 200.00,
        "date": "2025-10-02"
    })
    
    print("Sales Data Product Metrics:")
    print(json.dumps(sales_product.get_metrics(), indent=2))
    
    print("\nData Quality Report:")
    print(json.dumps(sales_product.get_data_quality_report(), indent=2))
