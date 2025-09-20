#!/bin/bash

# Script to test multiple Supabase image URLs
echo "🔍 Testing Supabase image URLs..."

# Array of potential filenames
filenames=(
    "06b608cefa19ee4cf77fcb5e16c67441.jpg"
    "10-A-Sparkle-In-Fall.jpg"
    "-denver_manic11.jpg"
    "0b1e82a15fa5e0d0b4f5b66419e22a49.jpg"
    "0ca9f10d642022c92534ad8b6e3f7c15.jpg"
    "0e1867d615af550df0a7b7596c8e4d2f.jpg"
    "08899376046268a41abc4d5e7f2b8c93.jpg"
    "09e252f2bc02f6b379567ed8a1b4c6f7.jpg"
    "0b16b6fadd074430bf60b2e9c5a7d8f4.jpg"
    "04848fa751ab01fa56044cc6e8c3e2d5.jpg"
    "050a47d479b3cb7be72589e4a8f5c2d1.jpg"
    "065634fa-f42d-406a-a8af-c5e7d1f8b9c2.jpg"
    "065717038b4e426202e481f7c3a8d9e5.jpg"
    "06a364396fc0ea25688678b4c5d7e2f3.jpg"
    "036653ed7f54487d866db6b7a8e5c4f1.jpg"
    "02f909fa35c4d443cd20f97e78e6a4c3.jpg"
    "02835226764cd49975376e8c9e2a2c0a.jpg"
    "00d62c2afd91a7c4250d64c3bb2e4d8b.jpg"
    "nail_art_1.jpg"
    "nail_art_2.jpg"
    "1--Bridal-Nail-Art-Designs-for-Your-Wedding-Day.jpg"
)

working_files=()
total_tested=0

for filename in "${filenames[@]}"; do
    total_tested=$((total_tested + 1))
    echo -n "[$total_tested/${#filenames[@]}] Testing $filename: "
    
    status=$(curl -s "https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/$filename" -I | head -1 | grep -o "HTTP/[0-9.]* [0-9]*")
    
    if [[ $status == *"200"* ]]; then
        echo "✅ WORKS"
        working_files+=("$filename")
    else
        echo "❌ Failed ($status)"
    fi
    
    sleep 0.1  # Small delay
done

echo ""
echo "🎉 Summary:"
echo "   Total tested: $total_tested"
echo "   Working images: ${#working_files[@]}"
echo ""

if [ ${#working_files[@]} -gt 0 ]; then
    echo "📋 Working image filenames:"
    for i in "${!working_files[@]}"; do
        echo "   $((i+1)). ${working_files[i]}"
    done
    
    # Save to file
    echo "Working images found:" > working_images.txt
    printf '%s\n' "${working_files[@]}" >> working_images.txt
    echo ""
    echo "💾 Saved results to working_images.txt"
else
    echo "❌ No working images found!"
fi
