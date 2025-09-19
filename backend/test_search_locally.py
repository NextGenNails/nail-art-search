#!/usr/bin/env python3
"""
Local Testing for Metadata Search System
Test all search functionality without Pinecone dependency
"""

import sys
import os
from metadata_search import MetadataSearchEngine

def test_all_search_functions():
    """Test all search functionality locally"""
    
    print("🚀 Testing Metadata Search System Locally")
    print("=" * 50)
    
    # Initialize search engine
    try:
        search_engine = MetadataSearchEngine()
        vendors = search_engine.vendors
        print(f"✅ Loaded {len(vendors)} vendors successfully")
    except Exception as e:
        print(f"❌ Failed to initialize search engine: {e}")
        return False
    
    print(f"\n📋 Available Vendors:")
    for i, vendor in enumerate(vendors, 1):
        print(f"  {i}. {vendor.vendor_name}")
        print(f"     📍 {vendor.city}, {vendor.state}")
        print(f"     📱 {vendor.instagram_handle}")
        print(f"     💰 {vendor.price_range}")
        print(f"     🎨 {', '.join(vendor.specialties[:3])}...")
        print()
    
    # Test different search scenarios
    test_scenarios = [
        {
            "name": "Search by name 'Ariadna'",
            "method": "search_vendors",
            "params": {"query": "Ariadna"}
        },
        {
            "name": "Search by name 'Mia'", 
            "method": "search_vendors",
            "params": {"query": "Mia"}
        },
        {
            "name": "Search by city 'Dallas'",
            "method": "search_vendors",
            "params": {"filters": {"city": "Dallas"}}
        },
        {
            "name": "Search by city 'Plano'",
            "method": "search_vendors", 
            "params": {"filters": {"city": "Plano"}}
        },
        {
            "name": "Search by service 'acrylic'",
            "method": "search_by_services",
            "params": {"services": ["acrylic"]}
        },
        {
            "name": "Search by service 'gel_x'",
            "method": "search_by_services",
            "params": {"services": ["gel_x"]}
        },
        {
            "name": "Search by service '3d_art'",
            "method": "search_by_services", 
            "params": {"services": ["3d_art"]}
        },
        {
            "name": "Search by price range '$$$'",
            "method": "search_vendors",
            "params": {"filters": {"price_range": "$$$"}}
        },
        {
            "name": "Search by price range '$$'",
            "method": "search_vendors",
            "params": {"filters": {"price_range": "$$"}}
        },
        {
            "name": "Search by availability 'monday'",
            "method": "search_by_availability",
            "params": {"day": "monday"}
        },
        {
            "name": "Advanced search: Dallas + acrylic",
            "method": "advanced_search",
            "params": {"search_params": {"city": "Dallas", "services": ["acrylic"]}}
        },
        {
            "name": "Advanced search: gel_x + 3d_art",
            "method": "advanced_search",
            "params": {"search_params": {"services": ["gel_x", "3d_art"]}}
        }
    ]
    
    # Run all test scenarios
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🔍 Test {i}: {scenario['name']}")
        print("-" * 40)
        
        try:
            method = getattr(search_engine, scenario['method'])
            results = method(**scenario['params'])
            
            if results:
                print(f"✅ Found {len(results)} results:")
                for result in results[:2]:  # Show first 2 results
                    score = result.get('search_score', 0)
                    reasons = result.get('match_reasons', [])
                    print(f"  • {result['vendor_name']} (Score: {score:.1f})")
                    if reasons:
                        print(f"    Reasons: {', '.join(reasons)}")
                
                if len(results) > 2:
                    print(f"  ... and {len(results) - 2} more")
            else:
                print("❌ No results found")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print(f"\n🎉 Search System Testing Complete!")
    print(f"📊 Total tests run: {len(test_scenarios)}")
    
    return True

def test_api_endpoints():
    """Test the API endpoints with curl commands"""
    
    print(f"\n🌐 API Endpoint Test Commands:")
    print("=" * 40)
    
    endpoints = [
        "curl 'http://localhost:8000/vendors'",
        "curl 'http://localhost:8000/search/vendors?q=Ariadna'",
        "curl 'http://localhost:8000/search/vendors?city=Dallas'",
        "curl 'http://localhost:8000/search/vendors?services=acrylic'",
        "curl 'http://localhost:8000/search/vendors?price_range=$$$'",
        "curl 'http://localhost:8000/search/services?services=gel_x,3d_art'",
        "curl 'http://localhost:8000/search/availability?day=monday'"
    ]
    
    for i, endpoint in enumerate(endpoints, 1):
        print(f"{i}. {endpoint}")
    
    print(f"\n💻 Frontend Test URL:")
    print("http://localhost:3000/search-test")

if __name__ == "__main__":
    # Run comprehensive tests
    success = test_all_search_functions()
    
    if success:
        test_api_endpoints()
        
        print(f"\n🚀 Ready for Local Testing!")
        print("=" * 30)
        print("1. Backend: python3 backend/main_pinecone.py")
        print("2. Frontend: cd frontend && npm run dev")
        print("3. Test page: http://localhost:3000/search-test")
    else:
        print("❌ Setup failed. Please check the errors above.")
