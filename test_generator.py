#!/usr/bin/env python3
"""
Test script for the report generator
"""

import asyncio
import os
from report_generator import ReportGenerator

async def test_report_generation():
    """Test the report generation functionality."""
    generator = ReportGenerator()
    
    # Test data
    test_data = {
        'title': 'Artificial Intelligence in Modern Education',
        'language': 'EN',
        'student': 'John Smith',
        'professor': 'Dr. Jane Doe',
        'university': 'Test University',
        'college': 'College of Computer Science',
        'department': 'Computer Science Department',
        'year': 2024,
        'pages': 10,
        'ref_style': 'APA'
    }
    
    print("Testing report generation...")
    try:
        docx_path, pdf_path = await generator.generate_report(test_data)
        
        print(f"✅ DOCX generated: {os.path.basename(docx_path)}")
        print(f"   File size: {os.path.getsize(docx_path)} bytes")
        print(f"   File exists: {os.path.exists(docx_path)}")
        
        print(f"✅ PDF generated: {os.path.basename(pdf_path)}")
        print(f"   File size: {os.path.getsize(pdf_path)} bytes")
        print(f"   File exists: {os.path.exists(pdf_path)}")
        
        # Clean up
        os.remove(docx_path)
        os.remove(pdf_path)
        print("✅ Test files cleaned up")
        
        print("🎉 Report generation test PASSED!")
        
    except Exception as e:
        print(f"❌ Test FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_report_generation())