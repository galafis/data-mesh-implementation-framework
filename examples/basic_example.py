"""
Exemplo Básico - Data Mesh Implementation Framework
Author: Gabriel Demetrios Lafis
Year: 2025

Este exemplo demonstra o uso básico do framework para criar e gerenciar Data Products.
"""

import sys
import os

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import (
    SalesDataProduct,
    CustomerDataProduct,
)

def main():
    print("\n" + "="*80)
    print("Data Mesh Implementation Framework - Exemplo Básico")
    print("="*80 + "\n")

    # 1. Criar Data Product de Vendas
    print("📊 1. Criando SalesDataProduct...")
    sales_product = SalesDataProduct(
        name="Vendas Q4 2025",
        description="Transações de vendas do quarto trimestre",
        owner="sales-team@company.com",
        version="1.0.0"
    )
    
    # Publicar o Data Product
    sales_product.publish()
    
    # Adicionar dados de vendas
    print("\n📝 2. Adicionando dados de vendas...")
    sales_data = [
        {
            "transaction_id": "TXN001",
            "product_id": "PROD123",
            "customer_id": "CUST456",
            "amount": 150.00,
            "date": "2025-10-15",
            "product_category": "Electronics",
            "region": "North America"
        },
        {
            "transaction_id": "TXN002",
            "product_id": "PROD124",
            "customer_id": "CUST457",
            "amount": 200.00,
            "date": "2025-10-16",
            "product_category": "Books",
            "region": "Europe"
        },
        {
            "transaction_id": "TXN003",
            "product_id": "PROD125",
            "customer_id": "CUST456",
            "amount": 75.50,
            "date": "2025-10-17",
            "product_category": "Electronics",
            "region": "North America"
        }
    ]
    
    for sale in sales_data:
        sales_product.add_data(sale)
    
    # 3. Consultar dados
    print("\n🔍 3. Consultando dados de vendas...")
    all_sales = sales_product.query()
    print(f"Total de transações: {len(all_sales)}")
    
    electronics = sales_product.get_sales_by_product_category("Electronics")
    print(f"Transações de Electronics: {len(electronics)}")
    
    # 4. Obter métricas
    print("\n📈 4. Métricas de Vendas:")
    metrics = sales_product.get_sales_metrics()
    print(f"  - Receita Total: ${metrics['total_revenue']:.2f}")
    print(f"  - Total de Transações: {metrics['total_transactions']}")
    print(f"  - Valor Médio por Transação: ${metrics['average_transaction_value']:.2f}")
    print(f"  - Vendas por Categoria: {metrics['sales_by_category']}")
    
    print("\n" + "="*80)
    print("✨ Exemplo concluído com sucesso!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
