#!/usr/bin/env python3
"""
Test Metadata Search System
Demonstrates all search capabilities with your real vendor data
"""

import sys
import os
sys.path.append('backend')

from backend.metadata_search import MetadataSearchEngine

def main():
    """Main testing function"""
    
    print("🔍 Nail'd Metadata Search System Demo")
    print("=" * 50)
    
    # Initialize search engine
    search_engine = MetadataSearchEngine('backend/real_vendors_database.json')
    vendors = search_engine.vendors
    
    print(f"✅ Loaded {len(vendors)} vendors")
    print()
    
    # Show available vendors
    print("📋 Your Vendors:")
    for i, vendor in enumerate(vendors, 1):
        print(f"{i}. {vendor.vendor_name}")
        print(f"   📍 {vendor.city}, {vendor.state}")
        print(f"   📱 {vendor.instagram_handle}")
        print(f"   💰 {vendor.price_range}")
        print(f"   🎨 {', '.join(vendor.specialties)}")
        print(f"   🔗 {vendor.booking_link}")
        print()
    
    # Interactive search testing
    while True:
        print("\n🔍 Search Options:")
        print("1. Search by name")
        print("2. Search by city") 
        print("3. Search by services")
        print("4. Search by price range")
        print("5. Search by availability")
        print("6. Advanced search (multiple criteria)")
        print("7. Show all vendors")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            name = input("Enter name to search: ")
            results = search_engine.search_vendors(query=name)
            show_results(results, f"Name search: '{name}'")
            
        elif choice == "2":
            city = input("Enter city (Dallas, Plano, etc.): ")
            results = search_engine.search_vendors(filters={"city": city})
            show_results(results, f"City search: '{city}'")
            
        elif choice == "3":
            services = input("Enter services (comma-separated, e.g., acrylic,gel_x): ")
            service_list = [s.strip() for s in services.split(",")]
            results = search_engine.search_by_services(service_list)
            show_results(results, f"Services search: {service_list}")
            
        elif choice == "4":
            price = input("Enter price range ($, $$, $$$): ")
            results = search_engine.search_vendors(filters={"price_range": price})
            show_results(results, f"Price range search: '{price}'")
            
        elif choice == "5":
            day = input("Enter day (monday, tuesday, etc.): ")
            results = search_engine.search_by_availability(day)
            show_results(results, f"Availability search: '{day}'")
            
        elif choice == "6":
            print("Enter multiple criteria (leave blank to skip):")
            name = input("  Name: ")
            city = input("  City: ")
            services = input("  Services (comma-separated): ")
            price = input("  Price range: ")
            
            search_params = {}
            if name: search_params["name"] = name
            if city: search_params["city"] = city
            if services: search_params["services"] = [s.strip() for s in services.split(",")]
            if price: search_params["price_range"] = price
            
            results = search_engine.advanced_search(search_params)
            show_results(results, f"Advanced search: {search_params}")
            
        elif choice == "7":
            results = [{"vendor_name": v.vendor_name, "city": v.city, "specialties": v.specialties, "price_range": v.price_range, "instagram_handle": v.instagram_handle} for v in vendors]
            show_results(results, "All vendors")
            
        elif choice == "8":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

def show_results(results, search_description):
    """Display search results"""
    
    print(f"\n📊 Results for {search_description}:")
    print("-" * 50)
    
    if not results:
        print("❌ No results found")
        return
    
    print(f"✅ Found {len(results)} vendor(s):")
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['vendor_name']}")
        print(f"   📍 Location: {result.get('city', 'N/A')}, {result.get('state', 'N/A')}")
        print(f"   📱 Instagram: {result.get('instagram_handle', 'N/A')}")
        print(f"   💰 Price: {result.get('price_range', 'N/A')}")
        
        if 'specialties' in result and result['specialties']:
            print(f"   🎨 Services: {', '.join(result['specialties'])}")
        
        if 'search_score' in result:
            print(f"   📈 Relevance: {result['search_score']:.1f}")
        
        if 'match_reasons' in result and result['match_reasons']:
            print(f"   ✅ Matches: {', '.join(result['match_reasons'])}")
        
        if 'booking_link' in result:
            print(f"   🔗 Book: {result['booking_link']}")

if __name__ == "__main__":
    main()
