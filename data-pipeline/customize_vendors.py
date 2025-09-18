#!/usr/bin/env python3
"""
Script to customize Instagram vendor accounts for scraping.
"""

import json
from pathlib import Path

def load_vendor_template():
    """Load the vendor template structure"""
    return {
        "username": "example_nail_artist",
        "name": "Example Nail Artist",
        "booking_url": "https://example.com/book",
        "location": "City, State",
        "specialties": ["Nail Art", "Gel Extensions", "Custom Designs"]
    }

def add_custom_vendor():
    """Add a custom vendor to the scraper"""
    print("=== Add Custom Nail Art Vendor ===")
    
    vendor = {}
    vendor["username"] = input("Instagram username (without @): ").strip()
    vendor["name"] = input("Business/Artist name: ").strip()
    vendor["booking_url"] = input("Booking website URL: ").strip()
    vendor["location"] = input("Location (City, State): ").strip()
    
    print("Enter specialties (comma-separated): ")
    specialties_input = input().strip()
    vendor["specialties"] = [s.strip() for s in specialties_input.split(",") if s.strip()]
    
    return vendor

def save_vendors_to_file(vendors, filename="custom_vendors.json"):
    """Save vendors to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(vendors, f, indent=2, ensure_ascii=False)
    print(f"✅ Vendors saved to {filename}")

def load_vendors_from_file(filename="custom_vendors.json"):
    """Load vendors from a JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def main():
    """Main function to manage custom vendors"""
    print("Instagram Vendor Customization Tool")
    
    while True:
        print("\nOptions:")
        print("1. Add a new vendor")
        print("2. View current vendors")
        print("3. Show vendor template")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            vendor = add_custom_vendor()
            vendors = load_vendors_from_file()
            vendors.append(vendor)
            save_vendors_to_file(vendors)
            
        elif choice == "2":
            vendors = load_vendors_from_file()
            if vendors:
                print("\nCurrent vendors:")
                for i, vendor in enumerate(vendors, 1):
                    print(f"{i}. {vendor['name']} (@{vendor['username']}) - {vendor['location']}")
            else:
                print("No custom vendors found.")
                
        elif choice == "3":
            template = load_vendor_template()
            print("\nVendor template:")
            print(json.dumps(template, indent=2))
            
        elif choice == "4":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 