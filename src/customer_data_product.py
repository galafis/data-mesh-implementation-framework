
"""
Customer Data Product - Data Mesh Implementation Framework
Author: Gabriel Demetrios Lafis
Year: 2025

Este módulo demonstra um produto de dados de clientes em uma arquitetura Data Mesh,
utilizando o DomainDataProduct como base para gerenciamento de dados e metadados.
"""

from typing import Dict, List, Any
from datetime import datetime
import json
import re
from collections import defaultdict

try:
    from .domain_data_product import DomainDataProduct, DataProductMetadata, DataSchema, DataProductSLA, DataProductStatus, DataQualityLevel
except ImportError:
    from domain_data_product import DomainDataProduct, DataProductMetadata, DataSchema, DataProductSLA, DataProductStatus, DataQualityLevel


class CustomerDataProduct(DomainDataProduct):
    """
    Representa um produto de dados de clientes em um Data Mesh, estendendo DomainDataProduct.
    
    Este produto de dados é de propriedade do domínio de clientes e fornece
    dados sobre perfis de clientes, segmentação e histórico de interações.
    """
    
    def __init__(self, name: str, owner: str, domain: str = "Customer",
                 version: str = "1.0.0", description: str = "Customer profiles and segmentation data product"):
        
        # Definir metadados específicos para clientes
        metadata = DataProductMetadata(
            name=name,
            version=version,
            domain=domain,
            owner=owner,
            description=description,
            tags=["customers", "profiles", "segmentation", "CRM"],
            quality_level=DataQualityLevel.SILVER # Começa como SILVER, pode ser GOLD após validação
        )
        
        # Definir schema específico para clientes
        schema = DataSchema(
            fields={
                "customer_id": "string",
                "name": "string",
                "email": "string",
                "registration_date": "string", # Formato YYYY-MM-DD
                "lifetime_value": "float",
                "tier": "string",
                "last_interaction": "string" # Formato YYYY-MM-DD HH:MM:SS
            },
            primary_key="customer_id",
            indexes=["email", "tier"]
        )
        
        # Definir SLA para clientes
        sla = DataProductSLA(
            availability=99.9,
            freshness=5, # 5 minutos de latência máxima para atualizações de perfil
            completeness=99.5,
            accuracy=99.5
        )
        
        super().__init__(metadata, schema, sla)
        self._segments: Dict[str, List[str]] = {}

    def add_data(self, customer_data: Dict[str, Any]) -> bool:
        """
        Adiciona dados de cliente ao Data Product, com validações adicionais.
        """
        if not self._validate_customer_data(customer_data):
            print(f"✗ Falha ao adicionar dados: Validação de dados de cliente falhou para {customer_data.get('customer_id', 'N/A')}")
            return False
        
        if not super().add_data(customer_data):
            return False
        
        # Atualizar segmentos após adicionar novo cliente
        self._update_all_segments()
        return True

    def update_data(self, filters: Dict[str, Any], new_data: Dict[str, Any]) -> int:
        """
        Atualiza dados de cliente existentes no Data Product com base em filtros.
        """
        updated_count = super().update_data(filters, new_data)
        if updated_count > 0:
            self._update_all_segments()
        return updated_count

    def remove_data(self, filters: Dict[str, Any]) -> int:
        """
        Remove dados de cliente do Data Product com base em filtros.
        """
        removed_count = super().remove_data(filters)
        if removed_count > 0:
            self._update_all_segments()
        return removed_count

    def _validate_customer_data(self, customer_data: Dict[str, Any]) -> bool:
        """
        Valida dados de cliente específicos, além do schema básico.
        """
        required_fields = ["customer_id", "name", "email", "registration_date", "lifetime_value", "tier"]
        if not all(field in customer_data for field in required_fields):
            print(f"✗ Dados de cliente incompletos. Campos obrigatórios: {required_fields}")
            return False
        
        # Validação de formato de e-mail
        if not re.match(r"[^@]+@[^@]+\.[^@]+", customer_data["email"]):
            print(f"✗ Formato de e-mail inválido para {customer_data['email']}")
            return False

        # Validação de formato de data de registro
        try:
            datetime.strptime(customer_data["registration_date"], "%Y-%m-%d")
        except ValueError:
            print(f"✗ Formato de registration_date inválido para {customer_data['registration_date']}. Esperado YYYY-MM-DD.")
            return False
        
        # Validação de formato de última interação (se presente)
        if "last_interaction" in customer_data and customer_data["last_interaction"]:
            try:
                datetime.strptime(customer_data["last_interaction"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print(f"✗ Formato de last_interaction inválido para {customer_data['last_interaction']}. Esperado YYYY-MM-DD HH:MM:SS.")
                return False

        # Validação de valor de lifetime_value
        if not isinstance(customer_data["lifetime_value"], (int, float)) or customer_data["lifetime_value"] < 0:
            print(f"✗ Valor de lifetime_value inválido para {customer_data['lifetime_value']}. Deve ser um número não negativo.")
            return False
        
        # Validação de unicidade de customer_id
        if any(record.get("customer_id") == customer_data["customer_id"] for record in self._data_store):
            print(f"✗ customer_id {customer_data['customer_id']} já existe. Clientes devem ser únicos.")
            return False

        return True

    def create_segment(self, segment_name: str, criteria_func: callable) -> None:
        """
        Cria um segmento de clientes baseado em critérios dinâmicos.
        
        Args:
            segment_name: Nome do segmento
            criteria_func: Função que recebe um dicionário de dados do cliente e retorna True/False
        """
        self._segments[segment_name] = [
            customer["customer_id"] for customer in self._data_store
            if criteria_func(customer)
        ]
        print(f"✓ Segmento \'{segment_name}\' criado/atualizado com {len(self._segments[segment_name])} clientes.")
    
    def _update_all_segments(self) -> None:
        """
        Re-avalia e atualiza todos os segmentos existentes. Chamado após operações de dados.
        (Em um cenário real, isso poderia ser otimizado ou acionado por eventos).
        """
        # Para simplificar, vamos apenas recriar os segmentos existentes. 
        # Em um sistema real, seria necessário armazenar as `criteria_func` ou uma representação delas.
        # Por enquanto, este método é um placeholder para indicar que os segmentos precisam ser atualizados.
        print("ℹ️ Segmentos precisam ser re-avaliados após alterações nos dados.")
        # Exemplo: se tivéssemos armazenado as funções lambda, poderíamos reexecutá-las aqui.
        # for segment_name, criteria_func in self._stored_criteria.items():
        #     self.create_segment(segment_name, criteria_func)

    def get_segment(self, segment_name: str) -> List[str]:
        """
        Retorna os IDs dos clientes em um segmento.
        """
        return self._segments.get(segment_name, [])
    
    def get_segment_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas sobre os segmentos de clientes.
        """
        total_customers = len(self._data_store)
        if total_customers == 0:
            return {"message": "No customer data to generate segment statistics."}

        stats = {
            "total_customers": total_customers,
            "total_segments": len(self._segments),
            "segments": {}
        }
        for segment_name, customer_ids in self._segments.items():
            count = len(customer_ids)
            stats["segments"][segment_name] = {
                "customer_count": count,
                "percentage": f"{(count / total_customers * 100):.2f}%"
            }
        return stats
    
    def get_customer_demographics(self) -> Dict[str, Any]:
        """
        Gera um relatório demográfico básico dos clientes.
        """
        if not self._data_store:
            return {"message": "No customer data to generate demographics."}

        tiers = defaultdict(int)
        for customer in self._data_store:
            tiers[customer.get("tier", "Unknown")] += 1
        
        return {
            "total_customers": len(self._data_store),
            "customers_by_tier": dict(tiers)
        }

    def get_data_quality_report(self) -> Dict[str, Any]:
        """
        Gera um relatório de qualidade de dados mais detalhado para clientes.
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

        # Validação de unicidade para customer_id
        customer_ids = [record["customer_id"] for record in self._data_store if "customer_id" in record]
        unique_customer_ids = len(set(customer_ids))
        duplicate_customers = total_records - unique_customer_ids
        uniqueness_rate = round((unique_customer_ids / total_records) * 100, 2)

        # Validação de formato de e-mail
        invalid_emails = sum(1 for record in self._data_store if not re.match(r"[^@]+@[^@]+\.[^@]+", record.get("email", "")))
        email_validity_rate = round((1 - invalid_emails / total_records) * 100, 2)

        # Validação de range para 'lifetime_value'
        invalid_ltv = sum(1 for record in self._data_store if not (isinstance(record.get("lifetime_value"), (int, float)) and record["lifetime_value"] >= 0))
        ltv_validity_rate = round((1 - invalid_ltv / total_records) * 100, 2)

        # Comparar com SLA
        meets_completeness_sla = completeness_by_field.get("customer_id", 0) >= self.sla.completeness
        meets_uniqueness_sla = uniqueness_rate >= 100 # Idealmente 100% para IDs
        meets_email_sla = email_validity_rate >= self.sla.accuracy
        meets_ltv_sla = ltv_validity_rate >= self.sla.accuracy

        return {
            "total_records": total_records,
            "completeness_by_field": completeness_by_field,
            "uniqueness_customer_id": {
                "rate": f"{uniqueness_rate:.2f}%",
                "duplicates_found": duplicate_customers,
                "meets_sla": meets_uniqueness_sla
            },
            "email_format_validity": {
                "rate": f"{email_validity_rate:.2f}%",
                "invalid_records": invalid_emails,
                "meets_sla": meets_email_sla
            },
            "lifetime_value_validity": {
                "rate": f"{ltv_validity_rate:.2f}%",
                "invalid_records": invalid_ltv,
                "meets_sla": meets_ltv_sla
            },
            "overall_completeness_sla_target": f"{self.sla.completeness}%",
            "overall_completeness_meets_sla": meets_completeness_sla and meets_uniqueness_sla and meets_email_sla and meets_ltv_sla
        }


if __name__ == "__main__":
    print("=" * 80)
    print("Customer Data Product - Advanced Example")
    print("=" * 80)

    customer_product = CustomerDataProduct(
        name="Enterprise Customer 360",
        owner="Customer Experience Team",
        version="2.0.0",
        description="Data product containing comprehensive customer profiles with advanced segmentation."
    )
    
    # Publicar o Data Product (inicialmente)
    customer_product.publish()

    # Adicionar alguns clientes de exemplo
    sample_customer_data = [
        {
            "customer_id": "CUST001", "name": "João Silva", "email": "joao.silva@example.com",
            "registration_date": "2024-01-15", "lifetime_value": 5000.00, "tier": "gold",
            "last_interaction": "2025-10-07 10:30:00"
        },
        {
            "customer_id": "CUST002", "name": "Maria Santos", "email": "maria.santos@example.com",
            "registration_date": "2024-03-20", "lifetime_value": 1500.00, "tier": "silver",
            "last_interaction": "2025-10-06 14:00:00"
        },
        {
            "customer_id": "CUST003", "name": "Pedro Oliveira", "email": "pedro.oliveira@example.com",
            "registration_date": "2025-05-10", "lifetime_value": 500.00, "tier": "bronze",
            "last_interaction": "2025-10-05 09:15:00"
        },
        {
            "customer_id": "CUST004", "name": "Ana Souza", "email": "ana.souza@example.com",
            "registration_date": "2024-02-01", "lifetime_value": 7500.00, "tier": "gold",
            "last_interaction": "2025-10-07 11:00:00"
        },
        # Dados com problemas para testar validações
        {
            "customer_id": "CUST005", "name": "Carlos Lima", "email": "carlos.lima@invalid",
            "registration_date": "2024-06-01", "lifetime_value": 200.00, "tier": "bronze",
            "last_interaction": "2025-10-01 12:00:00"
        }, # Email inválido
        {
            "customer_id": "CUST006", "name": "Laura Costa", "email": "laura.costa@example.com",
            "registration_date": "invalid-date", "lifetime_value": 1000.00, "tier": "silver",
            "last_interaction": "2025-10-02 13:00:00"
        }, # Data de registro inválida
        {
            "customer_id": "CUST001", "name": "João Duplicado", "email": "joao.duplicado@example.com",
            "registration_date": "2025-01-01", "lifetime_value": 10.00, "tier": "bronze",
            "last_interaction": "2025-10-03 14:00:00"
        } # customer_id duplicado
    ]
    
    for data in sample_customer_data:
        customer_product.add_data(data)
    
    # Criar segmentos dinamicamente
    customer_product.create_segment(
        "high_value_customers",
        lambda c: c.get("lifetime_value", 0) > 3000 and c.get("tier") == "gold"
    )
    
    customer_product.create_segment(
        "recent_interactions",
        lambda c: datetime.strptime(c.get("last_interaction", "2000-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S") > datetime(2025, 10, 6)
    )

    customer_product.create_segment(
        "new_customers_2025",
        lambda c: datetime.strptime(c.get("registration_date", "2000-01-01"), "%Y-%m-%d").year == 2025
    )
    
    print("\n" + "=" * 30 + " Customer Demographics " + "=" * 26)
    print(json.dumps(customer_product.get_customer_demographics(), indent=2))

    print("\n" + "=" * 30 + " Segment Statistics " + "=" * 29)
    print(json.dumps(customer_product.get_segment_statistics(), indent=2))
    
    print("\n" + "=" * 30 + " Data Quality Report " + "=" * 24)
    print(json.dumps(customer_product.get_data_quality_report(), indent=2))

    print("\n" + "=" * 30 + " Query Examples " + "=" * 30)
    # Consultar clientes de um segmento
    high_value_ids = customer_product.get_segment("high_value_customers")
    print(f"\nClientes de Alto Valor (IDs): {high_value_ids}")
    print("Detalhes dos Clientes de Alto Valor:")
    for cust_id in high_value_ids:
        customer_details = customer_product.query({"customer_id": cust_id})
        if customer_details:
            print(f"  - {customer_details[0]['name']} ({customer_details[0]['email']}) - LTV: R$ {customer_details[0]['lifetime_value']:.2f}")

    # Atualizar um cliente
    print("\nAtualizando tier do cliente CUST003...")
    customer_product.update_data({"customer_id": "CUST003"}, {"tier": "silver", "lifetime_value": 1200.00})
    updated_customer = customer_product.query({"customer_id": "CUST003"})
    if updated_customer:
        print(f"Cliente CUST003 atualizado: Tier {updated_customer[0]['tier']}, LTV R$ {updated_customer[0]['lifetime_value']:.2f}")
    
    # Remover um cliente
    print("\nRemovendo cliente CUST002...")
    customer_product.remove_data({"customer_id": "CUST002"})
    remaining_customer = customer_product.query({"customer_id": "CUST002"})
    if not remaining_customer:
        print("Cliente CUST002 removido com sucesso.")

    print("\n" + "=" * 80)
    print("Exemplo Concluído")
    print("=" * 80)


