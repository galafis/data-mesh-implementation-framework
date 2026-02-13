"""
Testes para o módulo de integração com APIs externas
Author: Gabriel Demetrios Lafis
Year: 2025
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.api_integration import WorldBankAPIIntegration, ExternalDataEnricher


class TestWorldBankAPIIntegration(unittest.TestCase):
    """Testes para a classe WorldBankAPIIntegration"""
    
    def setUp(self):
        """Configuração executada antes de cada teste"""
        self.wb_api = WorldBankAPIIntegration()
    
    def test_initialization(self):
        """Testa se a API é inicializada corretamente"""
        self.assertIsNotNone(self.wb_api.session)
        self.assertEqual(self.wb_api.BASE_URL, "https://api.worldbank.org/v2")
    
    @patch('src.api_integration.requests.Session.get')
    def test_get_countries_success(self, mock_get):
        """Testa obtenção de países com sucesso"""
        # Mock da resposta da API
        mock_response = Mock()
        mock_response.json.return_value = [
            {"page": 1, "pages": 1, "per_page": 50, "total": 2},
            [
                {"id": "BRA", "name": "Brazil", "region": {"value": "Latin America"}},
                {"id": "USA", "name": "United States", "region": {"value": "North America"}}
            ]
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        countries = self.wb_api.get_countries(per_page=50)
        
        self.assertEqual(len(countries), 2)
        self.assertEqual(countries[0]["id"], "BRA")
        self.assertEqual(countries[1]["name"], "United States")
    
    @patch('src.api_integration.requests.Session.get')
    def test_get_countries_api_error(self, mock_get):
        """Testa tratamento de erro ao obter países"""
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("API Error")
        
        countries = self.wb_api.get_countries()
        
        self.assertEqual(countries, [])
    
    @patch('src.api_integration.requests.Session.get')
    def test_get_indicators_success(self, mock_get):
        """Testa obtenção de indicadores com sucesso"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"page": 1, "pages": 1, "per_page": 20, "total": 2},
            [
                {"id": "NY.GDP.MKTP.CD", "name": "GDP (current US$)"},
                {"id": "SP.POP.TOTL", "name": "Population, total"}
            ]
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        indicators = self.wb_api.get_indicators(per_page=20)
        
        self.assertEqual(len(indicators), 2)
        self.assertEqual(indicators[0]["id"], "NY.GDP.MKTP.CD")
    
    @patch('src.api_integration.requests.Session.get')
    def test_get_indicators_with_search(self, mock_get):
        """Testa obtenção de indicadores com filtro de busca"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"page": 1, "pages": 1, "per_page": 20, "total": 2},
            [
                {"id": "NY.GDP.MKTP.CD", "name": "GDP (current US$)"},
                {"id": "SP.POP.TOTL", "name": "Population, total"}
            ]
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        indicators = self.wb_api.get_indicators(search_term="GDP", per_page=20)
        
        self.assertEqual(len(indicators), 1)
        self.assertEqual(indicators[0]["id"], "NY.GDP.MKTP.CD")
    
    @patch('src.api_integration.requests.Session.get')
    def test_get_country_data_success(self, mock_get):
        """Testa obtenção de dados de país com sucesso"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"page": 1, "pages": 1, "per_page": 100, "total": 2},
            [
                {
                    "indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP"},
                    "country": {"id": "BRA", "value": "Brazil"},
                    "value": 1000000000,
                    "date": "2022"
                },
                {
                    "indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP"},
                    "country": {"id": "BRA", "value": "Brazil"},
                    "value": 950000000,
                    "date": "2021"
                }
            ]
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        data = self.wb_api.get_country_data("BRA", "NY.GDP.MKTP.CD")
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["value"], 1000000000)
    
    @patch('src.api_integration.requests.Session.get')
    def test_get_country_data_with_year_range(self, mock_get):
        """Testa obtenção de dados com range de anos"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"page": 1, "pages": 1, "per_page": 100, "total": 1},
            [
                {
                    "indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP"},
                    "country": {"id": "BRA", "value": "Brazil"},
                    "value": 1000000000,
                    "date": "2022"
                }
            ]
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        data = self.wb_api.get_country_data("BRA", "NY.GDP.MKTP.CD", start_year=2020, end_year=2022)
        
        self.assertIsNotNone(data)
        mock_get.assert_called_once()
    
    @patch('src.api_integration.requests.Session.get')
    def test_get_multiple_countries_data(self, mock_get):
        """Testa obtenção de dados para múltiplos países"""
        def mock_response_func(*args, **kwargs):
            mock_response = Mock()
            if 'BRA' in args[0]:
                mock_response.json.return_value = [
                    {},
                    [{"value": 1000, "date": "2022", "country": {"value": "Brazil"}}]
                ]
            elif 'USA' in args[0]:
                mock_response.json.return_value = [
                    {},
                    [{"value": 2000, "date": "2022", "country": {"value": "United States"}}]
                ]
            mock_response.raise_for_status = Mock()
            return mock_response
        
        mock_get.side_effect = mock_response_func
        
        results = self.wb_api.get_multiple_countries_data(
            ["BRA", "USA"],
            "NY.GDP.MKTP.CD",
            year=2022
        )
        
        self.assertEqual(len(results), 2)
        self.assertIn("BRA", results)
        self.assertIn("USA", results)


class TestExternalDataEnricher(unittest.TestCase):
    """Testes para a classe ExternalDataEnricher"""
    
    def setUp(self):
        """Configuração executada antes de cada teste"""
        self.enricher = ExternalDataEnricher()
    
    def test_initialization(self):
        """Testa se o enricher é inicializado corretamente"""
        self.assertIsNotNone(self.enricher.wb_api)
    
    @patch.object(WorldBankAPIIntegration, 'get_country_data')
    def test_enrich_with_country_indicators(self, mock_get_data):
        """Testa enriquecimento com indicadores de país"""
        mock_get_data.return_value = [
            {
                "indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP"},
                "value": 1000000,
                "date": "2022"
            }
        ]
        
        result = self.enricher.enrich_with_country_indicators(
            "BRA",
            ["NY.GDP.MKTP.CD"]
        )
        
        self.assertEqual(result["country_code"], "BRA")
        self.assertIn("indicators", result)
        self.assertIn("NY.GDP.MKTP.CD", result["indicators"])
    
    @patch.object(WorldBankAPIIntegration, 'get_multiple_countries_data')
    def test_create_comparative_dataset(self, mock_get_multiple):
        """Testa criação de dataset comparativo"""
        mock_get_multiple.return_value = {
            "BRA": {
                "value": 1000,
                "date": "2022",
                "country": {"value": "Brazil"},
                "indicator": {"value": "GDP"}
            },
            "USA": {
                "value": 2000,
                "date": "2022",
                "country": {"value": "United States"},
                "indicator": {"value": "GDP"}
            }
        }
        
        result = self.enricher.create_comparative_dataset(
            ["BRA", "USA"],
            "NY.GDP.MKTP.CD",
            year=2022
        )
        
        self.assertEqual(len(result), 2)
        # Verifica se está ordenado por valor (decrescente)
        self.assertGreaterEqual(result[0]["value"], result[1]["value"])


if __name__ == "__main__":
    print("=" * 80)
    print("Executando testes do módulo de integração com APIs")
    print("=" * 80)
    
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestWorldBankAPIIntegration))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestExternalDataEnricher))
    
    result = runner.run(suite)
    
    sys.exit(0 if result.wasSuccessful() else 1)
