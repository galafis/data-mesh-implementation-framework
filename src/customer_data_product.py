"""
Customer Data Product - Data Mesh Implementation Framework
Author: Gabriel Demetrios Lafis
Year: 2025

Este módulo demonstra um produto de dados de clientes em uma arquitetura Data Mesh.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class CustomerDataProduct:
    """
    Representa um produto de dados de clientes em um Data Mesh.
    
    Este produto de dados é de propriedade do domínio de clientes e fornece
    dados sobre perfis de clientes, segmentação e histórico de interações.
    """
    
    def __init__(self, name: str, owner: str, domain: str = "Customer"):
        """
        Inicializa um produto de dados de clientes.
        
        Args:
            name: Nome do produto de dados
            owner: Proprietário do produto de dados (equipe ou indivíduo)
            domain: Domínio ao qual o produto pertence (padrão: Customer)
        """
        self.name = name
        self.owner = owner
        self.domain = domain
        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "schema_version": "1.0",
            "data_quality_sla": "99.5%",
            "update_frequency": "real-time",
            "compliance": ["GDPR", "LGPD"]
        }
        self.customers: Dict[str, Dict[str, Any]] = {}
        self.segments: Dict[str, List[str]] = {}
    
    def add_customer(self, customer_data: Dict[str, Any]) -> None:
        """
        Adiciona um cliente ao produto de dados.
        
        Args:
            customer_data: Dicionário contendo informações do cliente
        """
        required_fields = ["customer_id", "name", "email", "registration_date"]
        if not all(field in customer_data for field in required_fields):
            raise ValueError(f"Customer data must contain all required fields: {required_fields}")
        
        customer_id = customer_data["customer_id"]
        self.customers[customer_id] = customer_data
    
    def update_customer(self, customer_id: str, updates: Dict[str, Any]) -> None:
        """
        Atualiza informações de um cliente.
        
        Args:
            customer_id: ID do cliente
            updates: Dicionário com campos a serem atualizados
        """
        if customer_id not in self.customers:
            raise ValueError(f"Customer {customer_id} not found")
        
        self.customers[customer_id].update(updates)
        self.customers[customer_id]["last_updated"] = datetime.now().isoformat()
    
    def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """
        Retorna informações de um cliente específico.
        
        Args:
            customer_id: ID do cliente
            
        Returns:
            Dicionário com dados do cliente ou None se não encontrado
        """
        return self.customers.get(customer_id)
    
    def create_segment(self, segment_name: str, criteria: callable) -> None:
        """
        Cria um segmento de clientes baseado em critérios.
        
        Args:
            segment_name: Nome do segmento
            criteria: Função que recebe dados do cliente e retorna True/False
        """
        self.segments[segment_name] = [
            customer_id for customer_id, customer_data in self.customers.items()
            if criteria(customer_data)
        ]
    
    def get_segment(self, segment_name: str) -> List[str]:
        """
        Retorna os IDs dos clientes em um segmento.
        
        Args:
            segment_name: Nome do segmento
            
        Returns:
            Lista de IDs de clientes no segmento
        """
        return self.segments.get(segment_name, [])
    
    def get_customer_count(self) -> int:
        """
        Retorna o número total de clientes.
        
        Returns:
            Número de clientes
        """
        return len(self.customers)
    
    def get_segment_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas sobre os segmentos de clientes.
        
        Returns:
            Dicionário com estatísticas de segmentação
        """
        total_customers = len(self.customers)
        return {
            "total_customers": total_customers,
            "total_segments": len(self.segments),
            "segments": {
                segment_name: {
                    "customer_count": len(customer_ids),
                    "percentage": f"{(len(customer_ids) / total_customers * 100):.2f}%" if total_customers > 0 else "0%"
                }
                for segment_name, customer_ids in self.segments.items()
            }
        }
    
    def export_data(self, anonymize: bool = False) -> str:
        """
        Exporta os dados do produto em formato JSON.
        
        Args:
            anonymize: Se True, remove informações pessoalmente identificáveis
            
        Returns:
            String JSON com os dados
        """
        customers_data = self.customers.copy()
        
        if anonymize:
            for customer_id, customer_data in customers_data.items():
                customer_data["name"] = "***"
                customer_data["email"] = "***@***.com"
        
        export = {
            "name": self.name,
            "owner": self.owner,
            "domain": self.domain,
            "metadata": self.metadata,
            "customers": customers_data,
            "segments": self.segments
        }
        return json.dumps(export, indent=2)
    
    def get_data_quality_report(self) -> Dict[str, Any]:
        """
        Gera um relatório de qualidade de dados.
        
        Returns:
            Dicionário com informações de qualidade
        """
        total_records = len(self.customers)
        complete_records = sum(
            1 for customer in self.customers.values()
            if all(customer.get(field) for field in ["customer_id", "name", "email", "registration_date"])
        )
        completeness_rate = (complete_records / total_records * 100) if total_records > 0 else 0
        
        return {
            "total_records": total_records,
            "complete_records": complete_records,
            "completeness_rate": f"{completeness_rate:.2f}%",
            "sla_target": self.metadata["data_quality_sla"],
            "meets_sla": completeness_rate >= 99.5
        }


if __name__ == "__main__":
    # Exemplo de uso
    customer_product = CustomerDataProduct(
        name="Customer 360 View",
        owner="Customer Experience Team"
    )
    
    # Adicionar alguns clientes de exemplo
    customer_product.add_customer({
        "customer_id": "CUST001",
        "name": "João Silva",
        "email": "joao.silva@example.com",
        "registration_date": "2024-01-15",
        "lifetime_value": 5000.00,
        "tier": "gold"
    })
    
    customer_product.add_customer({
        "customer_id": "CUST002",
        "name": "Maria Santos",
        "email": "maria.santos@example.com",
        "registration_date": "2024-03-20",
        "lifetime_value": 1500.00,
        "tier": "silver"
    })
    
    customer_product.add_customer({
        "customer_id": "CUST003",
        "name": "Pedro Oliveira",
        "email": "pedro.oliveira@example.com",
        "registration_date": "2025-05-10",
        "lifetime_value": 500.00,
        "tier": "bronze"
    })
    
    # Criar segmentos
    customer_product.create_segment(
        "high_value",
        lambda c: c.get("lifetime_value", 0) > 3000
    )
    
    customer_product.create_segment(
        "premium",
        lambda c: c.get("tier") in ["gold", "platinum"]
    )
    
    print("Customer Segment Statistics:")
    print(json.dumps(customer_product.get_segment_statistics(), indent=2))
    
    print("\nData Quality Report:")
    print(json.dumps(customer_product.get_data_quality_report(), indent=2))
    
    print("\nHigh Value Customers:")
    print(customer_product.get_segment("high_value"))
