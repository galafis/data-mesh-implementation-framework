
"""
Testes unitários para Domain Data Product e seus derivados
Author: Gabriel Demetrios Lafis
Year: 2025
"""

import unittest
import sys
import os
from datetime import datetime
import json

# Adicionar o diretório src ao path para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.domain_data_product import (
    DomainDataProduct,
    DataProductMetadata,
    DataSchema,
    DataProductSLA,
    DataProductStatus,
    DataQualityLevel
)
from src.sales_data_product import SalesDataProduct
from src.customer_data_product import CustomerDataProduct


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
                "value": "integer",
                "name": "string"
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

        # Adicionar alguns dados iniciais para testes de update/remove
        self.data_product.add_data({"id": "001", "value": 100, "name": "Item A"})
        self.data_product.add_data({"id": "002", "value": 200, "name": "Item B"})
        self.data_product.add_data({"id": "003", "value": 150, "name": "Item C"})
    
    def test_initialization(self):
        """Testa se o Data Product é inicializado corretamente"""
        self.assertEqual(self.data_product.metadata.name, "test-product")
        self.assertEqual(self.data_product.metadata.status, DataProductStatus.DRAFT)
        self.assertEqual(len(self.data_product._data_store), 3)
    
    def test_add_valid_data(self):
        """Testa a adição de dados válidos"""
        data = {"id": "004", "value": 250, "name": "Item D"}
        result = self.data_product.add_data(data)
        self.assertTrue(result)
        self.assertEqual(len(self.data_product._data_store), 4)
    
    def test_add_invalid_data_missing_field(self):
        """Testa a adição de dados inválidos (sem campo obrigatório)"""
        data = {"id": "004", "value": 250}  # Falta o campo 'name'
        result = self.data_product.add_data(data)
        self.assertFalse(result)
        self.assertEqual(len(self.data_product._data_store), 3)

    def test_add_invalid_data_wrong_type(self):
        """Testa a adição de dados inválidos (tipo incorreto)"""
        data = {"id": "004", "value": "250", "name": "Item D"}  # 'value' deveria ser integer
        result = self.data_product.add_data(data)
        self.assertFalse(result)
        self.assertEqual(len(self.data_product._data_store), 3)
    
    def test_publish_valid_product(self):
        """Testa a publicação de um Data Product válido"""
        result = self.data_product.publish()
        self.assertTrue(result)
        self.assertEqual(self.data_product.metadata.status, DataProductStatus.PUBLISHED)
    
    def test_publish_invalid_product_metadata(self):
        """Testa a publicação de um Data Product com metadados inválidos"""
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

    def test_publish_invalid_product_schema(self):
        """Testa a publicação de um Data Product com schema inválido"""
        invalid_schema = DataSchema(fields={})
        invalid_product = DomainDataProduct(self.metadata, invalid_schema, self.sla)
        result = invalid_product.publish()
        self.assertFalse(result)
        self.assertEqual(invalid_product.metadata.status, DataProductStatus.DRAFT)
    
    def test_query_all_data(self):
        """Testa a consulta de todos os dados"""
        results = self.data_product.query()
        self.assertEqual(len(results), 3)
    
    def test_query_with_filter(self):
        """Testa a consulta com filtro"""
        results = self.data_product.query({"id": "001"})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["value"], 100)

        results_no_match = self.data_product.query({"id": "999"})
        self.assertEqual(len(results_no_match), 0)
    
    def test_update_existing_data(self):
        """Testa a atualização de dados existentes"""
        updated_count = self.data_product.update_data({"id": "001"}, {"value": 120, "name": "Updated Item A"})
        self.assertEqual(updated_count, 1)
        updated_record = self.data_product.query({"id": "001"})[0]
        self.assertEqual(updated_record["value"], 120)
        self.assertEqual(updated_record["name"], "Updated Item A")

    def test_update_non_existing_data(self):
        """Testa a atualização de dados que não existem"""
        updated_count = self.data_product.update_data({"id": "999"}, {"value": 500})
        self.assertEqual(updated_count, 0)

    def test_update_with_invalid_type(self):
        """Testa a atualização com tipo de dado inválido"""
        updated_count = self.data_product.update_data({"id": "001"}, {"value": "invalid_int"})
        self.assertEqual(updated_count, 0)
        # Verifica se o dado original não foi alterado
        original_record = self.data_product.query({"id": "001"})[0]
        self.assertEqual(original_record["value"], 100)

    def test_remove_existing_data(self):
        """Testa a remoção de dados existentes"""
        removed_count = self.data_product.remove_data({"id": "002"})
        self.assertEqual(removed_count, 1)
        self.assertEqual(len(self.data_product._data_store), 2)
        self.assertEqual(self.data_product.query({"id": "002"}), [])

    def test_remove_non_existing_data(self):
        """Testa a remoção de dados que não existem"""
        removed_count = self.data_product.remove_data({"id": "999"})
        self.assertEqual(removed_count, 0)
        self.assertEqual(len(self.data_product._data_store), 3)

    def test_get_metrics(self):
        """Testa a obtenção de métricas"""
        self.data_product.query()
        metrics = self.data_product.get_metrics()
        self.assertEqual(metrics["total_records"], 3)
        self.assertGreaterEqual(metrics["total_accesses"], 1) # Pode ter sido chamado pelo setUp ou outros testes
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
        initial_log_count = len(self.data_product._access_log)
        self.data_product.query()
        self.data_product.query({"id": "001"})
        
        self.assertEqual(len(self.data_product._access_log), initial_log_count + 2)
        self.assertEqual(self.data_product._access_log[-2]["operation"], "query")


class TestSalesDataProduct(unittest.TestCase):
    """Testes para a classe SalesDataProduct"""

    def setUp(self):
        self.sales_product = SalesDataProduct(
            name="Test Sales",
            owner="Sales Team"
        )

    def test_initialization(self):
        self.assertEqual(self.sales_product.metadata.name, "Test Sales")
        self.assertEqual(self.sales_product.metadata.domain, "Sales")
        self.assertEqual(self.sales_product.metadata.quality_level, DataQualityLevel.SILVER)

    def test_add_valid_sale(self):
        sale_data = {
            "transaction_id": "TXN001", "product_id": "P1", "customer_id": "C1",
            "amount": 100.00, "date": "2025-01-01", "product_category": "Electronics", "region": "NA"
        }
        self.assertTrue(self.sales_product.add_data(sale_data))
        self.assertEqual(len(self.sales_product._data_store), 1)
        self.assertAlmostEqual(self.sales_product.get_sales_metrics()["total_revenue"], 100.00)

    def test_add_invalid_sale_missing_field(self):
        sale_data = {
            "transaction_id": "TXN001", "product_id": "P1", "customer_id": "C1",
            "amount": 100.00, "date": "2025-01-01", "region": "NA" # Missing product_category
        }
        self.assertFalse(self.sales_product.add_data(sale_data))
        self.assertEqual(len(self.sales_product._data_store), 0)

    def test_add_invalid_sale_wrong_amount_type(self):
        sale_data = {
            "transaction_id": "TXN001", "product_id": "P1", "customer_id": "C1",
            "amount": "invalid", "date": "2025-01-01", "product_category": "Electronics", "region": "NA"
        }
        self.assertFalse(self.sales_product.add_data(sale_data))
        self.assertEqual(len(self.sales_product._data_store), 0)

    def test_add_invalid_sale_negative_amount(self):
        sale_data = {
            "transaction_id": "TXN001", "product_id": "P1", "customer_id": "C1",
            "amount": -10.00, "date": "2025-01-01", "product_category": "Electronics", "region": "NA"
        }
        self.assertFalse(self.sales_product.add_data(sale_data))
        self.assertEqual(len(self.sales_product._data_store), 0)

    def test_add_invalid_sale_duplicate_transaction_id(self):
        sale_data1 = {
            "transaction_id": "TXN001", "product_id": "P1", "customer_id": "C1",
            "amount": 100.00, "date": "2025-01-01", "product_category": "Electronics", "region": "NA"
        }
        sale_data2 = {
            "transaction_id": "TXN001", "product_id": "P2", "customer_id": "C2",
            "amount": 200.00, "date": "2025-01-02", "product_category": "Books", "region": "EU"
        }
        self.assertTrue(self.sales_product.add_data(sale_data1))
        self.assertFalse(self.sales_product.add_data(sale_data2)) # Should fail due to duplicate ID
        self.assertEqual(len(self.sales_product._data_store), 1)

    def test_get_sales_metrics(self):
        sales_data = [
            {"transaction_id": "TXN001", "product_id": "P1", "customer_id": "C1", "amount": 100.00, "date": "2025-01-01", "product_category": "Electronics", "region": "NA"},
            {"transaction_id": "TXN002", "product_id": "P2", "customer_id": "C2", "amount": 200.00, "date": "2025-01-02", "product_category": "Books", "region": "EU"},
            {"transaction_id": "TXN003", "product_id": "P1", "customer_id": "C1", "amount": 150.00, "date": "2025-01-03", "product_category": "Electronics", "region": "NA"}
        ]
        for sale in sales_data:
            self.sales_product.add_data(sale)
        
        metrics = self.sales_product.get_sales_metrics()
        self.assertAlmostEqual(metrics["total_revenue"], 450.00)
        self.assertEqual(metrics["total_transactions"], 3)
        self.assertAlmostEqual(metrics["average_transaction_value"], 150.00)
        self.assertEqual(metrics["sales_by_category"]["Electronics"], 250.00)
        self.assertEqual(metrics["sales_by_region"]["NA"], 250.00)

    def test_get_data_quality_report(self):
        sales_data = [
            {"transaction_id": "TXN001", "product_id": "P1", "customer_id": "C1", "amount": 100.00, "date": "2025-01-01", "product_category": "Electronics", "region": "NA"},
            {"transaction_id": "TXN002", "product_id": "P2", "customer_id": "C2", "amount": 200.00, "date": "2025-01-02", "product_category": "Books", "region": "EU"}
        ]
        for sale in sales_data:
            self.sales_product.add_data(sale)
        
        report = self.sales_product.get_data_quality_report()
        self.assertEqual(report["total_records"], 2)  # Only valid records added
        # Since both records are valid, all metrics should be 100%
        self.assertEqual(float(report["date_format_validity"]["rate"].replace("%", "")), 100.00)
        self.assertTrue(report["overall_completeness_meets_sla"])


class TestCustomerDataProduct(unittest.TestCase):
    """Testes para a classe CustomerDataProduct"""

    def setUp(self):
        self.customer_product = CustomerDataProduct(
            name="Test Customer 360",
            owner="CX Team"
        )

    def test_initialization(self):
        self.assertEqual(self.customer_product.metadata.name, "Test Customer 360")
        self.assertEqual(self.customer_product.metadata.domain, "Customer")
        self.assertEqual(self.customer_product.metadata.quality_level, DataQualityLevel.SILVER)

    def test_add_valid_customer(self):
        customer_data = {
            "customer_id": "CUST001", "name": "John Doe", "email": "john.doe@example.com",
            "registration_date": "2024-01-01", "lifetime_value": 1000.00, "tier": "silver",
            "last_interaction": "2025-10-01 10:00:00"
        }
        self.assertTrue(self.customer_product.add_data(customer_data))
        self.assertEqual(len(self.customer_product._data_store), 1)

    def test_add_invalid_customer_missing_field(self):
        customer_data = {
            "customer_id": "CUST001", "name": "John Doe", "email": "john.doe@example.com",
            "registration_date": "2024-01-01", "lifetime_value": 1000.00, "last_interaction": "2025-10-01 10:00:00"
        } # Missing tier
        self.assertFalse(self.customer_product.add_data(customer_data))
        self.assertEqual(len(self.customer_product._data_store), 0)

    def test_add_invalid_customer_email_format(self):
        customer_data = {
            "customer_id": "CUST001", "name": "John Doe", "email": "invalid-email",
            "registration_date": "2024-01-01", "lifetime_value": 1000.00, "tier": "silver",
            "last_interaction": "2025-10-01 10:00:00"
        }
        self.assertFalse(self.customer_product.add_data(customer_data))
        self.assertEqual(len(self.customer_product._data_store), 0)

    def test_add_invalid_customer_duplicate_id(self):
        customer_data1 = {
            "customer_id": "CUST001", "name": "John Doe", "email": "john.doe@example.com",
            "registration_date": "2024-01-01", "lifetime_value": 1000.00, "tier": "silver",
            "last_interaction": "2025-10-01 10:00:00"
        }
        customer_data2 = {
            "customer_id": "CUST001", "name": "Jane Doe", "email": "jane.doe@example.com",
            "registration_date": "2024-01-02", "lifetime_value": 2000.00, "tier": "gold",
            "last_interaction": "2025-10-02 11:00:00"
        }
        self.assertTrue(self.customer_product.add_data(customer_data1))
        self.assertFalse(self.customer_product.add_data(customer_data2)) # Should fail due to duplicate ID
        self.assertEqual(len(self.customer_product._data_store), 1)

    def test_create_and_get_segment(self):
        customer_data1 = {
            "customer_id": "CUST001", "name": "John Doe", "email": "john.doe@example.com",
            "registration_date": "2024-01-01", "lifetime_value": 1000.00, "tier": "silver",
            "last_interaction": "2025-10-01 10:00:00"
        }
        customer_data2 = {
            "customer_id": "CUST002", "name": "Jane Doe", "email": "jane.doe@example.com",
            "registration_date": "2024-01-02", "lifetime_value": 2000.00, "tier": "gold",
            "last_interaction": "2025-10-02 11:00:00"
        }
        self.customer_product.add_data(customer_data1)
        self.customer_product.add_data(customer_data2)

        self.customer_product.create_segment("gold_tier", lambda c: c.get("tier") == "gold")
        gold_customers = self.customer_product.get_segment("gold_tier")
        self.assertEqual(len(gold_customers), 1)
        self.assertIn("CUST002", gold_customers)

    def test_get_segment_statistics(self):
        customer_data1 = {
            "customer_id": "CUST001", "name": "John Doe", "email": "john.doe@example.com",
            "registration_date": "2024-01-01", "lifetime_value": 1000.00, "tier": "silver",
            "last_interaction": "2025-10-01 10:00:00"
        }
        customer_data2 = {
            "customer_id": "CUST002", "name": "Jane Doe", "email": "jane.doe@example.com",
            "registration_date": "2024-01-02", "lifetime_value": 2000.00, "tier": "gold",
            "last_interaction": "2025-10-02 11:00:00"
        }
        self.customer_product.add_data(customer_data1)
        self.customer_product.add_data(customer_data2)
        self.customer_product.create_segment("gold_tier", lambda c: c.get("tier") == "gold")

        stats = self.customer_product.get_segment_statistics()
        self.assertEqual(stats["total_customers"], 2)
        self.assertEqual(stats["total_segments"], 1)
        self.assertEqual(stats["segments"]["gold_tier"]["customer_count"], 1)

    def test_get_data_quality_report(self):
        customer_data = [
            {"customer_id": "CUST001", "name": "John Doe", "email": "john.doe@example.com", "registration_date": "2024-01-01", "lifetime_value": 1000.00, "tier": "silver", "last_interaction": "2025-10-01 10:00:00"}
        ]
        for cust in customer_data:
            self.customer_product.add_data(cust)
        
        report = self.customer_product.get_data_quality_report()
        self.assertEqual(report["total_records"], 1)  # Only valid record added
        # Since the record is valid, all metrics should be 100%
        self.assertEqual(float(report["email_format_validity"]["rate"].replace("%", "")), 100.00)
        self.assertTrue(report["overall_completeness_meets_sla"])


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


if __name__ == "__main__":
    print("=" * 80)
    print("Executando testes do Data Mesh Implementation Framework")
    print("=" * 80)
    # Criar um TextTestRunner com verbosity=2 para ver detalhes dos testes
    runner = unittest.TextTestRunner(verbosity=2)
    # Criar uma suíte de testes e adicionar todos os testes de cada classe
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDomainDataProduct))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSalesDataProduct))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCustomerDataProduct))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDataProductMetadata))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDataSchema))
    
    # Executar a suíte de testes
    result = runner.run(suite)
    
    # Sair com código de erro se algum teste falhar
    sys.exit(0 if result.wasSuccessful() else 1)

