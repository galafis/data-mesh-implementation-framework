import unittest
import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from domain_data_product import DomainDataProduct, DataProductStatus
from sales_data_product import SalesDataProduct
from customer_data_product import CustomerDataProduct

class TestIntegration(unittest.TestCase):
    """Testes de integração entre os Data Products"""

    def setUp(self):
        self.sales_product = SalesDataProduct(name="Integration Sales", owner="Integration Team")
        self.customer_product = CustomerDataProduct(name="Integration Customer", owner="Integration Team")
        
        self.sales_data = [
            {"transaction_id": "TXN100", "product_id": "P1", "customer_id": "C10", "amount": 100.0, "date": "2025-01-01", "product_category": "Electronics", "region": "NA"},
            {"transaction_id": "TXN101", "product_id": "P2", "customer_id": "C11", "amount": 200.0, "date": "2025-01-02", "product_category": "Books", "region": "EU"}
        ]
        
        self.customer_data = [
            {"customer_id": "C10", "name": "Integ John", "email": "integ.john@example.com", "registration_date": "2024-01-01", "lifetime_value": 100.0, "tier": "silver", "last_interaction": "2025-01-01 10:00:00"},
            {"customer_id": "C11", "name": "Integ Jane", "email": "integ.jane@example.com", "registration_date": "2024-01-02", "lifetime_value": 200.0, "tier": "gold", "last_interaction": "2025-01-02 11:00:00"}
        ]

        self.sales_file = "test_sales.json"
        self.customers_file = "test_customers.json"

        with open(self.sales_file, 'w') as f:
            json.dump(self.sales_data, f)
        
        with open(self.customers_file, 'w') as f:
            json.dump(self.customer_data, f)

    def tearDown(self):
        if os.path.exists(self.sales_file):
            os.remove(self.sales_file)
        if os.path.exists(self.customers_file):
            os.remove(self.customers_file)

    def test_load_data_from_json(self):
        """Testa o carregamento de dados a partir de arquivos JSON"""
        sales_loaded = self.sales_product.load_data_from_json(self.sales_file)
        customers_loaded = self.customer_product.load_data_from_json(self.customers_file)

        self.assertEqual(sales_loaded, 2)
        self.assertEqual(customers_loaded, 2)
        self.assertEqual(len(self.sales_product._data_store), 2)
        self.assertEqual(len(self.customer_product._data_store), 2)
        self.assertAlmostEqual(self.sales_product.get_sales_metrics()["total_revenue"], 300.0)

    def test_data_product_interaction_and_lineage(self):
        """Testa a interação e a linhagem entre Sales e Customer Data Products"""
        self.sales_product.load_data_from_json(self.sales_file)
        self.customer_product.load_data_from_json(self.customers_file)

        # Adicionar dependência
        self.sales_product.add_dependency(self.customer_product)
        self.customer_product.add_consumer(self.sales_product)

        # Verificar linhagem
        sales_lineage = self.sales_product.get_lineage()
        customer_lineage = self.customer_product.get_lineage()

        self.assertIn("Integration Customer", sales_lineage["upstream_dependencies"])
        self.assertIn("Integration Sales", customer_lineage["downstream_consumers"])

        # Exemplo de consulta que une informações (simulado)
        sales_records = self.sales_product.query()
        enriched_sales = []
        for sale in sales_records:
            customer = self.customer_product.query({"customer_id": sale["customer_id"]})
            if customer:
                enriched_sale = {**sale, "customer_name": customer[0]["name"], "customer_tier": customer[0]["tier"]}
                enriched_sales.append(enriched_sale)
        
        self.assertEqual(len(enriched_sales), 2)
        self.assertEqual(enriched_sales[0]["customer_name"], "Integ John")
        self.assertEqual(enriched_sales[1]["customer_tier"], "gold")

if __name__ == '__main__':
    unittest.main(verbosity=2)

