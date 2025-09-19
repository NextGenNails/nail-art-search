#!/usr/bin/env python3
"""
General Metadata Search System for Nail'd
Search vendors and images by any metadata field
"""

import os
import json
import re
from typing import Dict, List, Any, Optional, Union
from dataclasses import asdict
from vendor_manager import VendorManager

class MetadataSearchEngine:
    """Advanced metadata search for vendors and images"""
    
    def __init__(self, vendors_file: str = "real_vendors_database.json"):
        self.vendor_manager = VendorManager(vendors_file)
        self.vendors = self.vendor_manager.list_vendors()
        
    def search_vendors(self, 
                      query: str = None,
                      filters: Dict[str, Any] = None,
                      exact_match: bool = False) -> List[Dict[str, Any]]:
        """
        Search vendors by any metadata field
        
        Args:
            query: General text search across all fields
            filters: Specific field filters (e.g., {"city": "Dallas", "price_range": "$$"})
            exact_match: Whether to use exact matching or fuzzy search
            
        Returns:
            List of matching vendors with metadata
        """
        
        results = []
        
        for vendor in self.vendors:
            vendor_dict = asdict(vendor)
            
            # Apply filters first
            if filters and not self._matches_filters(vendor_dict, filters):
                continue
                
            # Apply general query search
            if query and not self._matches_query(vendor_dict, query, exact_match):
                continue
                
            # Add search relevance score
            score = self._calculate_relevance_score(vendor_dict, query, filters)
            
            result = {
                **vendor_dict,
                "search_score": score,
                "match_reasons": self._get_match_reasons(vendor_dict, query, filters)
            }
            
            results.append(result)
        
        # Sort by relevance score
        results.sort(key=lambda x: x["search_score"], reverse=True)
        return results
    
    def search_by_availability(self, day: str = None, time: str = None) -> List[Dict[str, Any]]:
        """Search vendors by availability"""
        
        results = []
        
        for vendor in self.vendors:
            vendor_dict = asdict(vendor)
            
            if self._is_available(vendor_dict, day, time):
                score = 1.0
                if day and vendor_dict.get("hours", {}).get(day.lower()):
                    score = 1.5  # Boost if specific day matches
                    
                result = {
                    **vendor_dict,
                    "search_score": score,
                    "availability_match": True
                }
                results.append(result)
        
        return sorted(results, key=lambda x: x["search_score"], reverse=True)
    
    def search_by_price_range(self, 
                             min_price: int = None, 
                             max_price: int = None,
                             price_category: str = None) -> List[Dict[str, Any]]:
        """Search vendors by price range"""
        
        results = []
        
        for vendor in self.vendors:
            vendor_dict = asdict(vendor)
            
            if self._matches_price_criteria(vendor_dict, min_price, max_price, price_category):
                result = {
                    **vendor_dict,
                    "search_score": 1.0,
                    "price_match": True
                }
                results.append(result)
        
        return results
    
    def search_by_services(self, services: List[str], match_all: bool = False) -> List[Dict[str, Any]]:
        """Search vendors by services/specialties"""
        
        results = []
        
        for vendor in self.vendors:
            vendor_dict = asdict(vendor)
            vendor_specialties = vendor_dict.get("specialties", [])
            
            if match_all:
                # Must have ALL services
                if all(self._service_matches(service, vendor_specialties) for service in services):
                    score = len(services)  # Higher score for more matches
                    result = {
                        **vendor_dict,
                        "search_score": score,
                        "service_matches": services
                    }
                    results.append(result)
            else:
                # Must have ANY service
                matching_services = []
                for service in services:
                    if self._service_matches(service, vendor_specialties):
                        matching_services.append(service)
                
                if matching_services:
                    score = len(matching_services) / len(services)  # Percentage match
                    result = {
                        **vendor_dict,
                        "search_score": score,
                        "service_matches": matching_services
                    }
                    results.append(result)
        
        return sorted(results, key=lambda x: x["search_score"], reverse=True)
    
    def advanced_search(self, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Advanced search with multiple criteria"""
        
        results = self.vendors.copy()
        search_results = []
        
        for vendor in results:
            vendor_dict = asdict(vendor)
            score = 0
            match_reasons = []
            
            # Check each search parameter
            for param, value in search_params.items():
                if param == "name" and value:
                    if self._fuzzy_match(vendor_dict.get("vendor_name", ""), value):
                        score += 2
                        match_reasons.append(f"Name matches '{value}'")
                
                elif param == "instagram" and value:
                    if self._fuzzy_match(vendor_dict.get("instagram_handle", ""), value):
                        score += 2
                        match_reasons.append(f"Instagram matches '{value}'")
                
                elif param == "city" and value:
                    if self._fuzzy_match(vendor_dict.get("city", ""), value):
                        score += 1.5
                        match_reasons.append(f"City matches '{value}'")
                
                elif param == "services" and value:
                    services = value if isinstance(value, list) else [value]
                    matching_services = []
                    vendor_specialties = vendor_dict.get("specialties", [])
                    
                    for service in services:
                        if self._service_matches(service, vendor_specialties):
                            matching_services.append(service)
                    
                    if matching_services:
                        score += len(matching_services)
                        match_reasons.append(f"Services: {', '.join(matching_services)}")
                
                elif param == "price_range" and value:
                    if self._price_range_matches(vendor_dict.get("price_range", ""), value):
                        score += 1
                        match_reasons.append(f"Price range matches '{value}'")
                
                elif param == "availability" and value:
                    if self._availability_matches(vendor_dict, value):
                        score += 1
                        match_reasons.append(f"Available on '{value}'")
            
            # Only include vendors with matches
            if score > 0:
                result = {
                    **vendor_dict,
                    "search_score": score,
                    "match_reasons": match_reasons
                }
                search_results.append(result)
        
        return sorted(search_results, key=lambda x: x["search_score"], reverse=True)
    
    def _matches_filters(self, vendor_dict: Dict, filters: Dict) -> bool:
        """Check if vendor matches all filters"""
        for key, value in filters.items():
            vendor_value = vendor_dict.get(key)
            if not vendor_value or not self._fuzzy_match(str(vendor_value), str(value)):
                return False
        return True
    
    def _matches_query(self, vendor_dict: Dict, query: str, exact_match: bool) -> bool:
        """Check if vendor matches general query"""
        if not query:
            return True
            
        # Search across all text fields
        searchable_fields = [
            "vendor_name", "vendor_location", "city", "state", 
            "instagram_handle", "description", "specialties"
        ]
        
        search_text = ""
        for field in searchable_fields:
            value = vendor_dict.get(field, "")
            if isinstance(value, list):
                search_text += " " + " ".join(value)
            else:
                search_text += " " + str(value)
        
        if exact_match:
            return query.lower() in search_text.lower()
        else:
            return self._fuzzy_match(search_text, query)
    
    def _fuzzy_match(self, text: str, query: str) -> bool:
        """Fuzzy text matching"""
        if not text or not query:
            return False
            
        text = text.lower()
        query = query.lower()
        
        # Exact match
        if query in text:
            return True
        
        # Word-by-word match
        query_words = query.split()
        return any(word in text for word in query_words)
    
    def _service_matches(self, service: str, vendor_specialties: List[str]) -> bool:
        """Check if service matches vendor specialties"""
        service = service.lower().replace("-", "_").replace(" ", "_")
        
        for specialty in vendor_specialties:
            specialty = specialty.lower().replace("-", "_").replace(" ", "_")
            if service in specialty or specialty in service:
                return True
        return False
    
    def _price_range_matches(self, vendor_price: str, query_price: str) -> bool:
        """Check if price ranges match"""
        return vendor_price.lower() == query_price.lower()
    
    def _availability_matches(self, vendor_dict: Dict, day: str) -> bool:
        """Check if vendor is available on specific day"""
        hours = vendor_dict.get("hours", {})
        if not hours:
            return True  # Assume available if no hours specified
            
        day_schedule = hours.get(day.lower())
        return day_schedule and day_schedule.lower() != "closed"
    
    def _is_available(self, vendor_dict: Dict, day: str = None, time: str = None) -> bool:
        """Check vendor availability"""
        if not day:
            return True
            
        return self._availability_matches(vendor_dict, day)
    
    def _matches_price_criteria(self, vendor_dict: Dict, min_price: int, max_price: int, price_category: str) -> bool:
        """Check if vendor matches price criteria"""
        if price_category:
            return vendor_dict.get("price_range") == price_category
        
        # For now, return True - you could parse actual price ranges
        return True
    
    def _calculate_relevance_score(self, vendor_dict: Dict, query: str, filters: Dict) -> float:
        """Calculate search relevance score"""
        score = 0.0
        
        if query:
            # Boost score for name matches
            if query.lower() in vendor_dict.get("vendor_name", "").lower():
                score += 3.0
            
            # Boost for Instagram matches
            if query.lower() in vendor_dict.get("instagram_handle", "").lower():
                score += 2.0
            
            # Boost for specialty matches
            specialties = vendor_dict.get("specialties", [])
            if any(query.lower() in specialty.lower() for specialty in specialties):
                score += 1.5
        
        if filters:
            score += len(filters) * 0.5  # Boost for filter matches
        
        return score
    
    def _get_match_reasons(self, vendor_dict: Dict, query: str, filters: Dict) -> List[str]:
        """Get reasons why this vendor matched"""
        reasons = []
        
        if query:
            if query.lower() in vendor_dict.get("vendor_name", "").lower():
                reasons.append(f"Name contains '{query}'")
            if query.lower() in vendor_dict.get("instagram_handle", "").lower():
                reasons.append(f"Instagram contains '{query}'")
        
        if filters:
            for key, value in filters.items():
                reasons.append(f"{key} = {value}")
        
        return reasons

# Example usage and testing
if __name__ == "__main__":
    # Initialize search engine
    search_engine = MetadataSearchEngine()
    
    print("🔍 Metadata Search Engine Test")
    print("=" * 40)
    
    # Test 1: Search by name
    print("\n1. Search by name 'Ariadna':")
    results = search_engine.search_vendors(query="Ariadna")
    for result in results:
        print(f"  ✅ {result['vendor_name']} (Score: {result['search_score']})")
    
    # Test 2: Search by service
    print("\n2. Search by service 'gel_x':")
    results = search_engine.search_by_services(["gel_x"])
    for result in results:
        print(f"  ✅ {result['vendor_name']} - Services: {result['service_matches']}")
    
    # Test 3: Search by city
    print("\n3. Search by city 'Dallas':")
    results = search_engine.search_vendors(filters={"city": "Dallas"})
    for result in results:
        print(f"  ✅ {result['vendor_name']} in {result['city']}")
    
    # Test 4: Advanced search
    print("\n4. Advanced search (multiple criteria):")
    results = search_engine.advanced_search({
        "services": ["acrylic"],
        "city": "Dallas",
        "availability": "monday"
    })
    for result in results:
        print(f"  ✅ {result['vendor_name']} - Reasons: {', '.join(result['match_reasons'])}")
    
    print(f"\n📊 Total vendors in database: {len(search_engine.vendors)}")
