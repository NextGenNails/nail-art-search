# 🏪 Vendor Data Management Guide

## 📋 **Information Currently Displayed on Frontend**

Your Nail'd app displays the following vendor information:

### **Primary Display Fields:**
1. **`name`** - Vendor/salon name (e.g., "Luxe Nail Studio")
2. **`distance`** - Distance from user (e.g., "2.1 mi away") 
3. **`location`** - City/area (e.g., "Richardson, TX")
4. **`rating`** - Star rating (e.g., "4.9")
5. **`image`** - Vendor profile/salon image URL
6. **`address`** - Full street address (shown in dropdown)
7. **`website`** - Vendor website URL (shown in dropdown)
8. **`booking_link`** - Direct booking URL (for "Book" button)

### **Additional Backend Fields:**
9. **`vendor_phone`** - Contact phone number
10. **`instagram_handle`** - Social media handle
11. **`specialties`** - Services offered (french, acrylic, gel, etc.)
12. **`price_range`** - Cost level ($, $$, $$$)
13. **`hours`** - Operating hours
14. **`description`** - Business description

## 🛠️ **How to Add Your Vendor Data**

### **Option 1: Provide Data, I'll Add It**
Send me vendor information in this format:

```json
{
  "vendor_name": "Your Nail Studio Name",
  "vendor_location": "123 Main St, Suite 100, Dallas, TX 75201", 
  "city": "Dallas",
  "state": "TX",
  "zip_code": "75201",
  "vendor_website": "https://yournailstudio.com",
  "booking_link": "https://yournailstudio.com/book",
  "vendor_rating": "4.8",
  "vendor_phone": "(214) 555-0123",
  "instagram_handle": "@yournailstudio",
  "specialties": ["french", "acrylic", "gel", "nail_art"],
  "price_range": "$$",
  "description": "Professional nail studio specializing in custom designs"
}
```

### **Option 2: Use the Management Scripts**
I've created tools for you to manage vendors:

1. **Add vendors**: `python assign_real_vendors.py add`
2. **Bulk assign**: `python assign_real_vendors.py`
3. **Manage database**: `python vendor_manager.py`

## 📊 **What I Can Do With Your Data**

### **✅ Automatic Assignment:**
- **Style-based matching**: Assign vendors based on nail art styles
- **Geographic distribution**: Spread vendors across Dallas area
- **Specialty alignment**: Match vendor expertise to image types

### **✅ Database Integration:**
- **Pinecone updates**: Add vendor metadata to existing images
- **Search optimization**: Improve search results with real data
- **Frontend integration**: Replace mock data with real vendors

### **✅ Data Management:**
- **Validation**: Ensure all required fields are present
- **Deduplication**: Prevent duplicate vendor entries
- **Bulk operations**: Handle multiple vendors efficiently

## 🎯 **Required Information (Minimum)**

For each vendor, I need at minimum:

1. **`vendor_name`** - Business name
2. **`vendor_location`** - Full address
3. **`city`** - City name
4. **`state`** - State abbreviation
5. **`vendor_website`** - Website URL
6. **`booking_link`** - How customers book
7. **`vendor_rating`** - Star rating
8. **`vendor_phone`** - Contact number

## 🌟 **Optional Information (Recommended)**

These fields enhance the user experience:

- **`instagram_handle`** - Social media presence
- **`specialties`** - What they're good at
- **`price_range`** - Budget expectations
- **`description`** - What makes them special
- **`hours`** - When they're open
- **`profile_image`** - Salon/artist photo

## 🔄 **Assignment Strategy**

I can assign vendors to your 723 images using:

### **Smart Matching:**
- **Style-based**: French nails → French specialists
- **Geographic**: Distribute across Dallas metro
- **Balanced**: Equal distribution among vendors
- **Quality-focused**: Higher rated vendors for better matches

### **Metadata Enhancement:**
Each image gets:
- Complete vendor information
- Booking capabilities
- Contact details
- Specialty tags
- Location data

## 📱 **Frontend Impact**

Once assigned, users will see:
- **Real nail salons** instead of mock data
- **Actual booking links** that work
- **Genuine ratings** and reviews
- **Accurate locations** and distances
- **Professional contact info**

## 🚀 **Next Steps**

1. **Provide vendor data** in the format above
2. **I'll validate and format** the information
3. **Assign to images** in Pinecone database
4. **Test the integration** with your app
5. **Deploy the updates** to production

## 📝 **Example Vendor Entry**

```json
{
  "vendor_name": "Artisan Nail Studio",
  "vendor_location": "4321 Preston Rd, Suite 150, Plano, TX 75024",
  "city": "Plano",
  "state": "TX", 
  "zip_code": "75024",
  "vendor_website": "https://artisannailstudio.com",
  "booking_link": "https://artisannailstudio.com/appointments",
  "vendor_rating": "4.9",
  "vendor_phone": "(972) 555-0123",
  "instagram_handle": "@artisannails",
  "specialties": ["nail_art", "french", "gel", "acrylic"],
  "price_range": "$$$",
  "description": "Award-winning nail artists specializing in custom designs and luxury treatments",
  "hours": {
    "monday": "9:00 AM - 7:00 PM",
    "tuesday": "9:00 AM - 7:00 PM",
    "wednesday": "9:00 AM - 7:00 PM", 
    "thursday": "9:00 AM - 7:00 PM",
    "friday": "9:00 AM - 8:00 PM",
    "saturday": "8:00 AM - 6:00 PM",
    "sunday": "10:00 AM - 5:00 PM"
  }
}
```

## 💡 **Pro Tips**

- **Real booking links**: Use actual booking systems (Square, Booksy, etc.)
- **Accurate ratings**: Use real Google/Yelp ratings
- **Current info**: Verify phone numbers and websites work
- **Local focus**: Dallas metro area performs best
- **Specialty tags**: Use consistent terms (french, acrylic, gel, nail_art)

---

**Ready to add your vendor data? Just provide the information and I'll handle the technical integration! 🚀**
