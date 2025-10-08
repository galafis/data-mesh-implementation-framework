
"""
Data Mesh Implementation Framework - Domain Data Product
Author: Gabriel Demetrios Lafis
Year: 2025

Este módulo demonstra a implementação de um Data Product em uma arquitetura Data Mesh.
Um Data Product é uma unidade autônoma que encapsula dados, metadados, código e infraestrutura.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import json
import os


class DataProductStatus(Enum):
    """Status do Data Product"""
    DRAFT = "draft"  # Rascunho, em desenvolvimento
    PUBLISHED = "published"  # Publicado, disponível para consumo
    DEPRECATED = "deprecated"  # Descontinuado, mas ainda disponível
    ARCHIVED = "archived"  # Arquivado, não mais disponível


class DataQualityLevel(Enum):
    """Níveis de qualidade de dados"""
    BRONZE = "bronze"  # Dados brutos, sem processamento
    SILVER = "silver"  # Dados limpos, validados e enriquecidos
    GOLD = "gold"      # Dados agregados, prontos para consumo e análise


@dataclass
class DataProductMetadata:
    """Metadados do Data Product"""
    name: str
    version: str
    domain: str
    owner: str
    description: str
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status: DataProductStatus = DataProductStatus.DRAFT
    quality_level: DataQualityLevel = DataQualityLevel.BRONZE


@dataclass
class DataSchema:
    """Schema dos dados do Data Product"""
    fields: Dict[str, str]  # nome_campo: tipo (ex: "id": "string", "age": "integer")
    primary_key: Optional[str] = None
    indexes: List[str] = field(default_factory=list)


@dataclass
class DataProductSLA:
    """Service Level Agreement (SLA) do Data Product"""
    availability: float  # Porcentagem (ex: 99.9%)
    freshness: int  # Minutos de latência máxima para atualização
    completeness: float  # Porcentagem de completude dos dados
    accuracy: float  # Porcentagem de precisão dos dados


class DomainDataProduct:
    """
    Implementação de um Domain Data Product seguindo os princípios do Data Mesh.
    
    Princípios implementados:
    1. Domain Ownership: Cada domínio é responsável por seus próprios dados.
    2. Data as a Product: Dados são tratados como produtos com qualidade e SLA.
    3. Self-serve Data Platform: Interface padronizada para descoberta e consumo.
    4. Federated Computational Governance: Políticas de governança aplicadas.
    """
    
    def __init__(self, metadata: DataProductMetadata, schema: DataSchema, sla: DataProductSLA):
        self.metadata = metadata
        self.schema = schema
        self.sla = sla
        self._data_store: List[Dict[str, Any]] = []  # Armazenamento interno de dados
        self._access_log: List[Dict[str, Any]] = []  # Log de acessos para auditoria
    
    def publish(self) -> bool:
        """
        Publica o Data Product, tornando-o disponível para consumo.
        Valida se todos os requisitos foram atendidos antes da publicação.
        """
        if not self._validate_for_publication():
            print(f"✗ Falha na publicação: Validações pendentes para o Data Product \'{self.metadata.name}\'")
            return False
        
        self.metadata.status = DataProductStatus.PUBLISHED
        self.metadata.updated_at = datetime.now()
        print(f"✓ Data Product \'{self.metadata.name}\' v{self.metadata.version} publicado com sucesso!")
        return True

    def _validate_for_publication(self) -> bool:
        """Valida se o Data Product está pronto para publicação"""
        validations = [
            (self.metadata.name, "Nome do Data Product é obrigatório"),
            (self.metadata.version, "Versão é obrigatória"),
            (self.metadata.domain, "Domínio é obrigatório"),
            (self.metadata.owner, "Owner é obrigatório"),
            (self.schema.fields, "Schema deve ter pelo menos um campo"),
        ]
        
        for value, error_msg in validations:
            if not value:
                print(f"✗ Validação falhou: {error_msg}")
                return False
        
        # Adicionar validações de qualidade e conformidade aqui
        if self.metadata.quality_level == DataQualityLevel.BRONZE and self.metadata.status == DataProductStatus.PUBLISHED:
            print(f"⚠️ Aviso: Data Product \'{self.metadata.name}\' está sendo publicado com nível de qualidade BRONZE. Considere elevar o nível de qualidade.")

        return True
    
    def add_data(self, data: Dict[str, Any]) -> bool:
        """
        Adiciona dados ao Data Product, validando-os contra o schema definido.
        """
        if not self._validate_data_schema(data):
            print(f"✗ Falha ao adicionar dados: Dados não conformes com o schema do Data Product \'{self.metadata.name}\'")
            return False
        
        self._data_store.append(data)
        print(f"✓ Dados adicionados ao Data Product \'{self.metadata.name}\'")
        return True
    
    def _validate_data_schema(self, data: Dict[str, Any]) -> bool:
        """
        Valida se os dados seguem o schema definido.
        Retorna True se válido, False caso contrário.
        """
        for field_name, field_type in self.schema.fields.items():
            if field_name not in data:
                print(f"✗ Campo obrigatório \'{field_name}\' não encontrado nos dados")
                return False
            # Validação de tipo básica (pode ser expandida)
            if field_type == "integer" and not isinstance(data[field_name], int):
                print(f"✗ Tipo inválido para o campo \'{field_name}\' (esperado inteiro, recebido {type(data[field_name]).__name__})")
                return False
            if field_type == "float" and not isinstance(data[field_name], float):
                print(f"✗ Tipo inválido para o campo \'{field_name}\' (esperado float, recebido {type(data[field_name]).__name__})")
                return False
            if field_type == "string" and not isinstance(data[field_name], str):
                print(f"✗ Tipo inválido para o campo \'{field_name}\' (esperado string, recebido {type(data[field_name]).__name__})")
                return False
        return True
    
    def query(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Consulta dados do Data Product com base em filtros.
        Registra o acesso para auditoria e monitoramento.
        """
        self._log_access("query", filters)
        
        if not filters:
            print(f"ℹ️ Consultando todos os {len(self._data_store)} registros do Data Product \'{self.metadata.name}\'")
            return self._data_store
        
        results = []
        for record in self._data_store:
            match = all(record.get(k) == v for k, v in filters.items())
            if match:
                results.append(record)
        
        print(f"✓ {len(results)} registros encontrados para os filtros {filters} no Data Product \'{self.metadata.name}\'")
        return results
    
    def update_data(self, filters: Dict[str, Any], new_data: Dict[str, Any]) -> int:
        """
        Atualiza dados existentes no Data Product com base em filtros.
        Registra a operação para auditoria.
        """
        if not filters:
            print("✗ Erro: Filtros são obrigatórios para atualizar dados.")
            return 0
        
        # Validar apenas os campos que estão sendo atualizados contra o schema
        for field_name, value in new_data.items():
            if field_name in self.schema.fields:
                expected_type = self.schema.fields[field_name]
                if expected_type == "integer" and not isinstance(value, int):
                    print(f"✗ Tipo inválido para o campo \'{field_name}\' (esperado inteiro, recebido {type(value).__name__})")
                    return 0
                if expected_type == "float" and not isinstance(value, float):
                    print(f"✗ Tipo inválido para o campo \'{field_name}\' (esperado float, recebido {type(value).__name__})")
                    return 0
                if expected_type == "string" and not isinstance(value, str):
                    print(f"✗ Tipo inválido para o campo \'{field_name}\' (esperado string, recebido {type(value).__name__})")
                    return 0

        updated_count = 0
        for record in self._data_store:
            match = all(record.get(k) == v for k, v in filters.items())
            if match:
                record.update(new_data)
                updated_count += 1
        
        if updated_count > 0:
            self._log_access("update", {"filters": filters, "new_data": new_data})
            print(f"✓ {updated_count} registros atualizados no Data Product \'{self.metadata.name}\'")
        else:
            print(f"ℹ️ Nenhum registro encontrado para atualizar com os filtros fornecidos no Data Product \'{self.metadata.name}\'")
        return updated_count

    def remove_data(self, filters: Dict[str, Any]) -> int: 
        """
        Remove dados do Data Product com base em filtros.
        Registra a operação para auditoria.
        """
        if not filters:
            print("✗ Erro: Filtros são obrigatórios para remover dados.")
            return 0
        
        initial_count = len(self._data_store)
        self._data_store = [record for record in self._data_store if not all(record.get(k) == v for k, v in filters.items())]
        removed_count = initial_count - len(self._data_store)
        
        if removed_count > 0:
            self._log_access("remove", filters)
            print(f"✓ {removed_count} registros removidos do Data Product \'{self.metadata.name}\'")
        else:
            print(f"ℹ️ Nenhum registro encontrado para remover com os filtros fornecidos no Data Product \'{self.metadata.name}\'")
        
        return removed_count

    def _log_access(self, operation: str, params: Any = None):
        """Registra acessos ao Data Product para auditoria"""
        log_entry = {
            "timestamp": datetime.now(),
            "operation": operation,
            "params": params,
            "data_product": self.metadata.name,
            "version": self.metadata.version
        }
        self._access_log.append(log_entry)
        print(f"[LOG] {log_entry['timestamp']}: Operação '{operation}' no Data Product '{self.metadata.name}' registrada.")
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Retorna métricas do Data Product.
        """
        return {
            "total_records": len(self._data_store),
            "total_accesses": len(self._access_log),
            "status": self.metadata.status.value,
            "quality_level": self.metadata.quality_level.value,
            "sla": {
                "availability": f"{self.sla.availability}%",
                "freshness": f"{self.sla.freshness} min",
                "completeness": f"{self.sla.completeness}%",
                "accuracy": f"{self.sla.accuracy}%"
            }
        }
    
    def get_lineage(self) -> Dict[str, Any]:
        """
        Retorna informações de linhagem do Data Product.
        """
        return {
            "data_product": self.metadata.name,
            "version": self.metadata.version,
            "domain": self.metadata.domain,
            "owner": self.metadata.owner,
            "created_at": self.metadata.created_at.isoformat(),
            "updated_at": self.metadata.updated_at.isoformat(),
            "upstream_dependencies": [],  # Seria populado com dependências reais
            "downstream_consumers": []     # Seria populado com consumidores reais
        }


def example_usage():
    """
    Exemplo de uso do Domain Data Product, incluindo interação com SalesDataProduct e CustomerDataProduct.
    """
    
    # Importar os Data Products específicos
    from sales_data_product import SalesDataProduct
    from customer_data_product import CustomerDataProduct

    print("\n" + "=" * 80)
    print("Data Mesh Implementation Framework - Domain Data Product Example")
    print("Demonstrando a interação entre diferentes Data Products")
    print("=" * 80)

    # --- 1. Criar e usar o SalesDataProduct ---
    print("\n" + "-" * 20 + " Sales Data Product " + "-" * 20)
    sales_product = SalesDataProduct(
        name="Enterprise Sales Transactions",
        owner="Global Sales Team",
        version="2.0.0",
        description="Data product containing all enterprise sales transactions with enhanced quality checks."
    )
    sales_product.publish()

    # Carregar dados de vendas de um arquivo JSON
    sales_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_sales.json")
    if os.path.exists(sales_file_path):
        with open(sales_file_path, "r") as f:
            sample_sales_data = json.load(f)
        print(f"Carregando {len(sample_sales_data)} registros de vendas de {sales_file_path}")
        for data in sample_sales_data:
            sales_product.add_data(data)
    else:
        print(f"✗ Arquivo de dados de vendas não encontrado: {sales_file_path}")

    print("\nSales Metrics:")
    print(json.dumps(sales_product.get_sales_metrics(), indent=2))
    print("\nSales Data Quality Report:")
    print(json.dumps(sales_product.get_data_quality_report(), indent=2))

    # --- 2. Criar e usar o CustomerDataProduct ---
    print("\n" + "-" * 20 + " Customer Data Product " + "-" * 20)
    customer_product = CustomerDataProduct(
        name="Enterprise Customer 360",
        owner="Customer Experience Team",
        version="2.0.0",
        description="Data product containing comprehensive customer profiles with advanced segmentation."
    )
    customer_product.publish()

    # Carregar dados de clientes de um arquivo JSON
    customers_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_customers.json")
    if os.path.exists(customers_file_path):
        with open(customers_file_path, "r") as f:
            sample_customer_data = json.load(f)
        print(f"Carregando {len(sample_customer_data)} registros de clientes de {customers_file_path}")
        for data in sample_customer_data:
            customer_product.add_data(data)
    else:
        print(f"✗ Arquivo de dados de clientes não encontrado: {customers_file_path}")

    # Criar segmentos dinamicamente
    customer_product.create_segment(
        "high_value_customers",
        lambda c: c.get("lifetime_value", 0) > 3000 and c.get("tier") == "gold"
    )
    customer_product.create_segment(
        "recent_interactions",
        lambda c: datetime.strptime(c.get("last_interaction", "2000-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S") > datetime(2025, 10, 6)
    )
    print("\nCustomer Segment Statistics:")
    print(json.dumps(customer_product.get_segment_statistics(), indent=2))
    print("\nCustomer Data Quality Report:")
    print(json.dumps(customer_product.get_data_quality_report(), indent=2))

    # --- 3. Exemplo de Interação entre Data Products (Simulada) ---
    print("\n" + "-" * 20 + " Inter-Data Product Interaction " + "-" * 20)
    print("Simulando a identificação de clientes de alto valor que fizeram compras recentes.")
    
    high_value_customer_ids = set(customer_product.get_segment("high_value_customers"))
    recent_interaction_customer_ids = set(customer_product.get_segment("recent_interactions"))

    # Clientes que são de alto valor E tiveram interações recentes
    intersecting_customer_ids = list(high_value_customer_ids.intersection(recent_interaction_customer_ids))
    
    print(f"\nClientes de Alto Valor com Interações Recentes (IDs): {intersecting_customer_ids}")
    if intersecting_customer_ids:
        print("Detalhes e Compras Recentes:")
        for cust_id in intersecting_customer_ids:
            customer_details = customer_product.query({"customer_id": cust_id})
            customer_sales = sales_product.query({"customer_id": cust_id})
            if customer_details:
                print(f"  - Cliente: {customer_details[0]['name']} (LTV: R$ {customer_details[0]['lifetime_value']:.2f})")
                if customer_sales:
                    print("    Compras:")
                    for sale in customer_sales:
                        print(f"      - {sale['product_category']} (R$ {sale['amount']:.2f}) em {sale['date']}")
                else:
                    print("    Nenhuma compra recente encontrada.")

    print("\n" + "=" * 80)
    print("Exemplo Concluído")
    print("=" * 80)


if __name__ == "__main__":
    example_usage()

