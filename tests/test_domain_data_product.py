"""
Testes unitários para Domain Data Product
Author: Gabriel Demetrios Lafis
Year: 2025
"""

import unittest
import sys
import os

# Adicionar o diretório src ao path para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from domain_data_product import (
    DomainDataProduct,
    DataProductMetadata,
    DataSchema,
    DataProductSLA,
    DataProductStatus,
    DataQualityLevel
)


class TestDomainDataProduct(unittest.TestCase):
    """Testes para a classe DomainDataProduct"""
    
    def setUp(self):
        """Configuração executada antes de cada teste"""
        self.metadata = DataProductMetadata(
            name="test-product",
            version="1.0.0",
            domain="test-domain",
            owner="test@example.com",
            description="Test data product",
            tags=["test"],
            quality_level=DataQualityLevel.SILVER
        )
        
        self.schema = DataSchema(
            fields={
                "id": "string",
                "value": "integer"
            },
            primary_key="id"
        )
        
        self.sla = DataProductSLA(
            availability=99.5,
            freshness=10,
            completeness=95.0,
            accuracy=98.0
        )
        
        self.data_product = DomainDataProduct(self.metadata, self.schema, self.sla)
    
    def test_initialization(self):
        """Testa se o Data Product é inicializado corretamente"""
        self.assertEqual(self.data_product.metadata.name, "test-product")
        self.assertEqual(self.data_product.metadata.status, DataProductStatus.DRAFT)
        self.assertEqual(len(self.data_product._data_store), 0)
    
    def test_add_valid_data(self):
        """Testa a adição de dados válidos"""
        data = {"id": "001", "value": 100}
        result = self.data_product.add_data(data)
        self.assertTrue(result)
        self.assertEqual(len(self.data_product._data_store), 1)
    
    def test_add_invalid_data(self):
        """Testa a adição de dados inválidos (sem campo obrigatório)"""
        data = {"id": "001"}  # Falta o campo 'value'
        result = self.data_product.add_data(data)
        self.assertFalse(result)
        self.assertEqual(len(self.data_product._data_store), 0)
    
    def test_publish_valid_product(self):
        """Testa a publicação de um Data Product válido"""
        result = self.data_product.publish()
        self.assertTrue(result)
        self.assertEqual(self.data_product.metadata.status, DataProductStatus.PUBLISHED)
    
    def test_publish_invalid_product(self):
        """Testa a publicação de um Data Product inválido"""
        invalid_metadata = DataProductMetadata(
            name="",  # Nome vazio
            version="1.0.0",
            domain="test",
            owner="test@example.com",
            description="Test"
        )
        invalid_product = DomainDataProduct(invalid_metadata, self.schema, self.sla)
        result = invalid_product.publish()
        self.assertFalse(result)
        self.assertEqual(invalid_product.metadata.status, DataProductStatus.DRAFT)
    
    def test_query_all_data(self):
        """Testa a consulta de todos os dados"""
        data1 = {"id": "001", "value": 100}
        data2 = {"id": "002", "value": 200}
        self.data_product.add_data(data1)
        self.data_product.add_data(data2)
        
        results = self.data_product.query()
        self.assertEqual(len(results), 2)
    
    def test_query_with_filter(self):
        """Testa a consulta com filtro"""
        data1 = {"id": "001", "value": 100}
        data2 = {"id": "002", "value": 200}
        self.data_product.add_data(data1)
        self.data_product.add_data(data2)
        
        results = self.data_product.query({"id": "001"})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["value"], 100)
    
    def test_get_metrics(self):
        """Testa a obtenção de métricas"""
        data = {"id": "001", "value": 100}
        self.data_product.add_data(data)
        self.data_product.query()
        
        metrics = self.data_product.get_metrics()
        self.assertEqual(metrics["total_records"], 1)
        self.assertEqual(metrics["total_accesses"], 1)
        self.assertEqual(metrics["status"], "draft")
    
    def test_get_lineage(self):
        """Testa a obtenção de linhagem"""
        lineage = self.data_product.get_lineage()
        self.assertEqual(lineage["data_product"], "test-product")
        self.assertEqual(lineage["version"], "1.0.0")
        self.assertEqual(lineage["domain"], "test-domain")
        self.assertIsInstance(lineage["upstream_dependencies"], list)
        self.assertIsInstance(lineage["downstream_consumers"], list)
    
    def test_access_logging(self):
        """Testa se os acessos são registrados"""
        self.data_product.query()
        self.data_product.query({"id": "001"})
        
        self.assertEqual(len(self.data_product._access_log), 2)
        self.assertEqual(self.data_product._access_log[0]["operation"], "query")


class TestDataProductMetadata(unittest.TestCase):
    """Testes para a classe DataProductMetadata"""
    
    def test_default_status(self):
        """Testa se o status padrão é DRAFT"""
        metadata = DataProductMetadata(
            name="test",
            version="1.0.0",
            domain="test",
            owner="test@example.com",
            description="Test"
        )
        self.assertEqual(metadata.status, DataProductStatus.DRAFT)
    
    def test_default_quality_level(self):
        """Testa se o nível de qualidade padrão é BRONZE"""
        metadata = DataProductMetadata(
            name="test",
            version="1.0.0",
            domain="test",
            owner="test@example.com",
            description="Test"
        )
        self.assertEqual(metadata.quality_level, DataQualityLevel.BRONZE)


class TestDataSchema(unittest.TestCase):
    """Testes para a classe DataSchema"""
    
    def test_schema_creation(self):
        """Testa a criação de um schema"""
        schema = DataSchema(
            fields={"id": "string", "name": "string"},
            primary_key="id",
            indexes=["name"]
        )
        self.assertEqual(len(schema.fields), 2)
        self.assertEqual(schema.primary_key, "id")
        self.assertEqual(len(schema.indexes), 1)


def run_tests():
    """Executa todos os testes"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adicionar todos os testes
    suite.addTests(loader.loadTestsFromTestCase(TestDomainDataProduct))
    suite.addTests(loader.loadTestsFromTestCase(TestDataProductMetadata))
    suite.addTests(loader.loadTestsFromTestCase(TestDataSchema))
    
    # Executar os testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 80)
    print("Executando testes do Data Mesh Implementation Framework")
    print("=" * 80)
    success = run_tests()
    sys.exit(0 if success else 1)
