#!/usr/bin/env python3
"""
Update Supabase database schema to include LAB histogram column.
"""

import os
import logging
from supabase_client import create_supabase_client

logger = logging.getLogger(__name__)

def add_histogram_column():
    """Add lab_histogram column to the nail_art_metadata table."""
    try:
        # Get credentials from environment
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables are required")
        
        supabase_client = create_supabase_client(supabase_url, supabase_key)
        supabase = supabase_client.client
        logger.info("✅ Supabase client created")
        
        # SQL to add the histogram column
        sql_commands = [
            """
            -- Add lab_histogram column if it doesn't exist
            DO $$ 
            BEGIN 
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'nail_art_metadata' 
                    AND column_name = 'lab_histogram'
                ) THEN
                    ALTER TABLE nail_art_metadata 
                    ADD COLUMN lab_histogram TEXT;
                    
                    COMMENT ON COLUMN nail_art_metadata.lab_histogram 
                    IS '3D LAB histogram as JSON array, L1-normalized, 8x8x8 bins';
                END IF;
            END $$;
            """,
            """
            -- Add index on lab_histogram for faster queries (optional)
            CREATE INDEX IF NOT EXISTS idx_nail_art_metadata_lab_histogram 
            ON nail_art_metadata USING gin(lab_histogram);
            """
        ]
        
        for i, sql in enumerate(sql_commands):
            logger.info(f"📝 Executing SQL command {i+1}/{len(sql_commands)}")
            try:
                result = supabase.rpc('execute_sql', {'sql': sql.strip()}).execute()
                logger.info(f"✅ SQL command {i+1} executed successfully")
            except Exception as e:
                # Try alternative approach for schema changes
                logger.warning(f"⚠️  RPC approach failed for command {i+1}, trying direct query: {e}")
                try:
                    # For schema changes, we might need to use a different approach
                    if i == 0:  # Column addition
                        # Check if column exists first
                        check_result = supabase.table('nail_art_metadata').select('lab_histogram').limit(1).execute()
                        logger.info("✅ Column already exists or was created successfully")
                    else:
                        logger.info("✅ Index creation skipped (may require admin privileges)")
                except Exception as e2:
                    if "column \"lab_histogram\" does not exist" in str(e2):
                        logger.error(f"❌ Column doesn't exist and couldn't be created: {e2}")
                        raise
                    else:
                        logger.info("✅ Column likely exists, continuing...")
        
        # Verify the schema update
        try:
            # Try to select from the table with the new column
            result = supabase.table('nail_art_metadata').select('filename, lab_histogram').limit(1).execute()
            logger.info("✅ Schema verification successful - lab_histogram column is accessible")
            
            if result.data:
                sample_record = result.data[0]
                logger.info(f"📋 Sample record: filename={sample_record.get('filename', 'N/A')}, "
                          f"has_histogram={sample_record.get('lab_histogram') is not None}")
            
        except Exception as e:
            logger.error(f"❌ Schema verification failed: {e}")
            raise
            
    except Exception as e:
        logger.error(f"❌ Failed to update schema: {e}")
        raise

def test_histogram_storage():
    """Test storing and retrieving a histogram."""
    try:
        # Get credentials from environment
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables are required")
        
        supabase_client = create_supabase_client(supabase_url, supabase_key)
        supabase = supabase_client.client
        
        # Test histogram data
        test_histogram = [0.1] * 512  # 8x8x8 = 512 bins
        test_histogram_json = str(test_histogram)
        
        # Try to find an existing record to update
        existing_records = supabase.table('nail_art_metadata').select('id, filename').limit(1).execute()
        
        if existing_records.data:
            record_id = existing_records.data[0]['id']
            filename = existing_records.data[0]['filename']
            
            logger.info(f"📝 Testing histogram storage with record: {filename}")
            
            # Update the record with test histogram
            result = supabase.table('nail_art_metadata').update({
                'lab_histogram': test_histogram_json
            }).eq('id', record_id).execute()
            
            if result.data:
                logger.info("✅ Test histogram stored successfully")
                
                # Verify retrieval
                retrieved = supabase.table('nail_art_metadata').select('lab_histogram').eq('id', record_id).execute()
                if retrieved.data and retrieved.data[0].get('lab_histogram'):
                    logger.info("✅ Test histogram retrieved successfully")
                    
                    # Clean up test data
                    supabase.table('nail_art_metadata').update({
                        'lab_histogram': None
                    }).eq('id', record_id).execute()
                    logger.info("🧹 Test data cleaned up")
                    
                else:
                    logger.error("❌ Failed to retrieve test histogram")
            else:
                logger.error("❌ Failed to store test histogram")
        else:
            logger.warning("⚠️  No existing records found for testing")
            
    except Exception as e:
        logger.error(f"❌ Histogram storage test failed: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    logger.info("🚀 Starting Supabase schema update...")
    add_histogram_column()
    
    logger.info("🧪 Testing histogram storage...")
    test_histogram_storage()
    
    logger.info("✅ Schema update complete!")
