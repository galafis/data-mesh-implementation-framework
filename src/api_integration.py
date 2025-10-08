"""
Data Mesh Implementation Framework - API Integration Module
Author: Gabriel Demetrios Lafis
Year: 2025

Este módulo demonstra a integração de Data Products com APIs externas,
especificamente a API do World Bank para dados de desenvolvimento mundial.
"""

import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class WorldBankAPIIntegration:
    """
    Integração com a API do World Bank para enriquecer Data Products com dados reais.
    """
    
    BASE_URL = "https://api.worldbank.org/v2"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DataMeshFramework/1.0'
        })
    
    def get_countries(self, per_page: int = 50) -> List[Dict[str, Any]]:
        """
        Obtém lista de países do World Bank.
        
        Args:
            per_page: Número de resultados por página
            
        Returns:
            Lista de países com seus metadados
        """
        try:
            url = f"{self.BASE_URL}/country"
            params = {
                'format': 'json',
                'per_page': per_page
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if len(data) > 1:
                countries = data[1]
                print(f"✓ {len(countries)} países recuperados da API do World Bank")
                return countries
            
            return []
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro ao buscar países: {e}")
            return []
    
    def get_indicators(self, search_term: Optional[str] = None, per_page: int = 20) -> List[Dict[str, Any]]:
        """
        Obtém lista de indicadores do World Bank.
        
        Args:
            search_term: Termo de busca para filtrar indicadores
            per_page: Número de resultados por página
            
        Returns:
            Lista de indicadores disponíveis
        """
        try:
            url = f"{self.BASE_URL}/indicator"
            params = {
                'format': 'json',
                'per_page': per_page
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if len(data) > 1:
                indicators = data[1]
                
                # Filtrar por termo de busca se fornecido
                if search_term:
                    indicators = [
                        ind for ind in indicators 
                        if search_term.lower() in ind.get('name', '').lower()
                    ]
                
                print(f"✓ {len(indicators)} indicadores recuperados da API do World Bank")
                return indicators
            
            return []
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro ao buscar indicadores: {e}")
            return []
    
    def get_country_data(
        self, 
        country_code: str, 
        indicator_code: str, 
        start_year: Optional[int] = None,
        end_year: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtém dados de um indicador específico para um país.
        
        Args:
            country_code: Código do país (ex: 'BRA' para Brasil)
            indicator_code: Código do indicador (ex: 'NY.GDP.MKTP.CD' para GDP)
            start_year: Ano inicial (opcional)
            end_year: Ano final (opcional)
            
        Returns:
            Lista de dados do indicador ao longo do tempo
        """
        try:
            url = f"{self.BASE_URL}/country/{country_code}/indicator/{indicator_code}"
            params = {
                'format': 'json',
                'per_page': 100
            }
            
            if start_year:
                params['date'] = f"{start_year}:{end_year or datetime.now().year}"
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if len(data) > 1:
                indicator_data = data[1]
                if indicator_data:
                    print(f"✓ {len(indicator_data)} registros recuperados para {country_code} - {indicator_code}")
                    return indicator_data
            
            print(f"ℹ️ Nenhum dado encontrado para {country_code} - {indicator_code}")
            return []
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro ao buscar dados do país: {e}")
            return []
    
    def get_multiple_countries_data(
        self,
        country_codes: List[str],
        indicator_code: str,
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Obtém dados de um indicador para múltiplos países.
        
        Args:
            country_codes: Lista de códigos de países
            indicator_code: Código do indicador
            year: Ano específico (opcional, usa o mais recente se não fornecido)
            
        Returns:
            Dicionário com dados por país
        """
        results = {}
        
        for country_code in country_codes:
            data = self.get_country_data(
                country_code, 
                indicator_code,
                start_year=year,
                end_year=year
            )
            
            if data:
                # Pegar o valor mais recente se não especificou ano
                if not year and data:
                    # Ordenar por data e pegar o mais recente com valor
                    sorted_data = sorted(
                        [d for d in data if d.get('value') is not None],
                        key=lambda x: x.get('date', ''),
                        reverse=True
                    )
                    if sorted_data:
                        results[country_code] = sorted_data[0]
                else:
                    results[country_code] = data[0] if data else None
        
        print(f"✓ Dados recuperados para {len(results)} países")
        return results


class ExternalDataEnricher:
    """
    Classe para enriquecer Data Products com dados de APIs externas.
    """
    
    def __init__(self):
        self.wb_api = WorldBankAPIIntegration()
    
    def enrich_with_country_indicators(
        self,
        country_code: str,
        indicators: List[str]
    ) -> Dict[str, Any]:
        """
        Enriquece dados com múltiplos indicadores de um país.
        
        Args:
            country_code: Código do país
            indicators: Lista de códigos de indicadores
            
        Returns:
            Dicionário com todos os indicadores
        """
        enriched_data = {
            'country_code': country_code,
            'indicators': {},
            'retrieved_at': datetime.now().isoformat()
        }
        
        for indicator_code in indicators:
            data = self.wb_api.get_country_data(country_code, indicator_code)
            if data:
                # Pegar o valor mais recente
                recent_data = [d for d in data if d.get('value') is not None]
                if recent_data:
                    sorted_data = sorted(
                        recent_data,
                        key=lambda x: x.get('date', ''),
                        reverse=True
                    )
                    enriched_data['indicators'][indicator_code] = {
                        'value': sorted_data[0].get('value'),
                        'date': sorted_data[0].get('date'),
                        'indicator_name': sorted_data[0].get('indicator', {}).get('value', '')
                    }
        
        return enriched_data
    
    def create_comparative_dataset(
        self,
        country_codes: List[str],
        indicator_code: str,
        year: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Cria um dataset comparativo entre países para um indicador.
        
        Args:
            country_codes: Lista de códigos de países
            indicator_code: Código do indicador
            year: Ano específico (opcional)
            
        Returns:
            Lista de dados comparativos
        """
        data = self.wb_api.get_multiple_countries_data(
            country_codes,
            indicator_code,
            year
        )
        
        comparative_data = []
        for country_code, country_data in data.items():
            if country_data and country_data.get('value') is not None:
                comparative_data.append({
                    'country_code': country_code,
                    'country_name': country_data.get('country', {}).get('value', ''),
                    'indicator_code': indicator_code,
                    'indicator_name': country_data.get('indicator', {}).get('value', ''),
                    'value': country_data.get('value'),
                    'year': country_data.get('date'),
                    'unit': country_data.get('unit', '')
                })
        
        # Ordenar por valor
        comparative_data.sort(key=lambda x: x['value'], reverse=True)
        
        return comparative_data


def example_usage():
    """
    Exemplo de uso da integração com APIs externas.
    """
    print("\n" + "=" * 80)
    print("Data Mesh Implementation Framework - API Integration Example")
    print("Demonstrando integração com World Bank API")
    print("=" * 80)
    
    # Inicializar integração
    wb_api = WorldBankAPIIntegration()
    enricher = ExternalDataEnricher()
    
    # Exemplo 1: Buscar países
    print("\n" + "-" * 40)
    print("Exemplo 1: Buscando países")
    print("-" * 40)
    countries = wb_api.get_countries(per_page=10)
    if countries:
        print("\nPrimeiros 5 países:")
        for country in countries[:5]:
            print(f"  - {country.get('name')} ({country.get('id')})")
    
    # Exemplo 2: Buscar indicadores
    print("\n" + "-" * 40)
    print("Exemplo 2: Buscando indicadores de GDP")
    print("-" * 40)
    indicators = wb_api.get_indicators(search_term="GDP", per_page=5)
    if indicators:
        print("\nIndicadores encontrados:")
        for indicator in indicators:
            print(f"  - {indicator.get('id')}: {indicator.get('name')}")
    
    # Exemplo 3: Dados de um país específico
    print("\n" + "-" * 40)
    print("Exemplo 3: GDP do Brasil (últimos 5 anos)")
    print("-" * 40)
    brazil_gdp = wb_api.get_country_data(
        'BRA',
        'NY.GDP.MKTP.CD',
        start_year=2019,
        end_year=2023
    )
    if brazil_gdp:
        print("\nDados do GDP do Brasil:")
        for data_point in brazil_gdp[:5]:
            if data_point.get('value'):
                print(f"  - {data_point.get('date')}: ${data_point.get('value'):,.0f}")
    
    # Exemplo 4: Enriquecimento com múltiplos indicadores
    print("\n" + "-" * 40)
    print("Exemplo 4: Enriquecendo dados do Brasil com múltiplos indicadores")
    print("-" * 40)
    enriched = enricher.enrich_with_country_indicators(
        'BRA',
        [
            'NY.GDP.MKTP.CD',  # GDP
            'SP.POP.TOTL',     # População
            'NY.GDP.PCAP.CD'   # GDP per capita
        ]
    )
    print("\nDados enriquecidos:")
    print(json.dumps(enriched, indent=2))
    
    # Exemplo 5: Dataset comparativo
    print("\n" + "-" * 40)
    print("Exemplo 5: Comparando GDP per capita entre países")
    print("-" * 40)
    comparative = enricher.create_comparative_dataset(
        ['BRA', 'USA', 'CHN', 'IND', 'DEU'],
        'NY.GDP.PCAP.CD',
        year=2022
    )
    if comparative:
        print("\nComparação de GDP per capita (2022):")
        for i, data in enumerate(comparative, 1):
            print(f"  {i}. {data['country_name']}: ${data['value']:,.2f}")


if __name__ == "__main__":
    example_usage()
