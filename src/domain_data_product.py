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


class DataProductStatus(Enum):
    """Status do Data Product"""
    DRAFT = "draft"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class DataQualityLevel(Enum):
    """Níveis de qualidade de dados"""
    BRONZE = "bronze"  # Dados brutos
    SILVER = "silver"  # Dados limpos e validados
    GOLD = "gold"      # Dados agregados e prontos para consumo


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
    fields: Dict[str, str]  # nome_campo: tipo
    primary_key: Optional[str] = None
    indexes: List[str] = field(default_factory=list)


@dataclass
class DataProductSLA:
    """Service Level Agreement do Data Product"""
    availability: float  # Porcentagem (ex: 99.9)
    freshness: int  # Minutos de latência máxima
    completeness: float  # Porcentagem de completude dos dados
    accuracy: float  # Porcentagem de precisão dos dados


class DomainDataProduct:
    """
    Implementação de um Domain Data Product seguindo os princípios do Data Mesh.
    
    Princípios implementados:
    1. Domain Ownership: Cada domínio é responsável por seus próprios dados
    2. Data as a Product: Dados são tratados como produtos com qualidade e SLA
    3. Self-serve Data Platform: Interface padronizada para descoberta e consumo
    4. Federated Computational Governance: Políticas de governança aplicadas
    """
    
    def __init__(self, metadata: DataProductMetadata, schema: DataSchema, sla: DataProductSLA):
        self.metadata = metadata
        self.schema = schema
        self.sla = sla
        self._data_store: List[Dict[str, Any]] = []
        self._access_log: List[Dict[str, Any]] = []
    
    def publish(self) -> bool:
        """
        Publica o Data Product, tornando-o disponível para consumo.
        Valida se todos os requisitos foram atendidos antes da publicação.
        """
        if not self._validate_for_publication():
            return False
        
        self.metadata.status = DataProductStatus.PUBLISHED
        self.metadata.updated_at = datetime.now()
        print(f"✓ Data Product '{self.metadata.name}' v{self.metadata.version} publicado com sucesso!")
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
        
        return True
    
    def add_data(self, data: Dict[str, Any]) -> bool:
        """Adiciona dados ao Data Product"""
        if not self._validate_data_schema(data):
            return False
        
        self._data_store.append(data)
        return True
    
    def _validate_data_schema(self, data: Dict[str, Any]) -> bool:
        """Valida se os dados seguem o schema definido"""
        for field_name in self.schema.fields.keys():
            if field_name not in data:
                print(f"✗ Campo obrigatório '{field_name}' não encontrado nos dados")
                return False
        return True
    
    def query(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Consulta dados do Data Product.
        Registra o acesso para auditoria e monitoramento.
        """
        self._log_access("query", filters)
        
        if not filters:
            return self._data_store
        
        # Filtro simples para demonstração
        results = []
        for record in self._data_store:
            match = all(record.get(k) == v for k, v in filters.items())
            if match:
                results.append(record)
        
        return results
    
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
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas do Data Product"""
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
        """Retorna informações de linhagem do Data Product"""
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
    """Exemplo de uso do Domain Data Product"""
    
    # Criar metadados do Data Product
    metadata = DataProductMetadata(
        name="customer-analytics",
        version="1.0.0",
        domain="sales",
        owner="sales-team@company.com",
        description="Dados analíticos de clientes para o domínio de vendas",
        tags=["customers", "analytics", "sales"],
        quality_level=DataQualityLevel.GOLD
    )
    
    # Definir schema dos dados
    schema = DataSchema(
        fields={
            "customer_id": "string",
            "name": "string",
            "email": "string",
            "total_purchases": "integer",
            "lifetime_value": "float"
        },
        primary_key="customer_id",
        indexes=["email"]
    )
    
    # Definir SLA
    sla = DataProductSLA(
        availability=99.9,
        freshness=15,
        completeness=98.0,
        accuracy=99.5
    )
    
    # Criar o Data Product
    data_product = DomainDataProduct(metadata, schema, sla)
    
    # Adicionar dados de exemplo
    sample_data = [
        {
            "customer_id": "CUST001",
            "name": "João Silva",
            "email": "joao@example.com",
            "total_purchases": 15,
            "lifetime_value": 1500.00
        },
        {
            "customer_id": "CUST002",
            "name": "Maria Santos",
            "email": "maria@example.com",
            "total_purchases": 23,
            "lifetime_value": 3200.00
        }
    ]
    
    for data in sample_data:
        data_product.add_data(data)
    
    # Publicar o Data Product
    data_product.publish()
    
    # Consultar dados
    print("\n📊 Consultando todos os clientes:")
    customers = data_product.query()
    for customer in customers:
        print(f"  - {customer['name']}: R$ {customer['lifetime_value']:.2f}")
    
    # Consultar com filtro
    print("\n🔍 Consultando cliente específico:")
    result = data_product.query({"customer_id": "CUST001"})
    if result:
        print(f"  - Encontrado: {result[0]['name']}")
    
    # Obter métricas
    print("\n📈 Métricas do Data Product:")
    metrics = data_product.get_metrics()
    for key, value in metrics.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    - {k}: {v}")
        else:
            print(f"  {key}: {value}")
    
    # Obter linhagem
    print("\n🔗 Linhagem do Data Product:")
    lineage = data_product.get_lineage()
    for key, value in lineage.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    print("=" * 80)
    print("Data Mesh Implementation Framework - Domain Data Product Example")
    print("=" * 80)
    example_usage()
