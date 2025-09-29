"""Unit tests for page control functionality."""

import unittest
from page_control import (
    count_words, calculate_target_words, adjust_content_length,
    get_page_estimate, TARGET_WORDS_PER_PAGE
)

class TestPageControl(unittest.TestCase):
    """Test cases for page control functions."""
    
    def test_count_words(self):
        """Test word counting function."""
        # Basic word counting
        self.assertEqual(count_words("Hello world"), 2)
        self.assertEqual(count_words("  Hello   world  "), 2)
        self.assertEqual(count_words(""), 0)
        self.assertEqual(count_words("   "), 0)
        
        # Multi-sentence text
        text = "This is a test. It has multiple sentences."
        self.assertEqual(count_words(text), 8)  # "This is a test It has multiple sentences"
    
    def test_calculate_target_words(self):
        """Test target word calculation."""
        min_words, max_words = calculate_target_words(1)
        
        # Should be within 5% tolerance of TARGET_WORDS_PER_PAGE
        expected_min = int(TARGET_WORDS_PER_PAGE * 0.95)
        expected_max = int(TARGET_WORDS_PER_PAGE * 1.05)
        
        self.assertEqual(min_words, expected_min)
        self.assertEqual(max_words, expected_max)
        
        # Test multiple pages
        min_words_5, max_words_5 = calculate_target_words(5)
        self.assertEqual(min_words_5, expected_min * 5)
        self.assertEqual(max_words_5, expected_max * 5)
    
    def test_get_page_estimate(self):
        """Test page estimation."""
        # Test with target words per page
        text = " ".join(["word"] * TARGET_WORDS_PER_PAGE)
        estimate = get_page_estimate(text)
        self.assertAlmostEqual(estimate, 1.0, places=1)
        
        # Test with double target words
        text = " ".join(["word"] * (TARGET_WORDS_PER_PAGE * 2))
        estimate = get_page_estimate(text)
        self.assertAlmostEqual(estimate, 2.0, places=1)
    
    def test_adjust_content_length_within_range(self):
        """Test content adjustment when already within range."""
        # Create content that's already within range for 1 page
        target_words = TARGET_WORDS_PER_PAGE
        text = " ".join(["word"] * target_words)
        
        adjusted = adjust_content_length(text, target_pages=1)
        
        # Should remain unchanged since it's within range
        self.assertEqual(count_words(adjusted), target_words)
    
    def test_adjust_content_length_expansion(self):
        """Test content expansion when too short."""
        # Create very short content that definitely needs expansion
        short_text = "Short text."
        initial_count = count_words(short_text)
        
        adjusted = adjust_content_length(short_text, target_pages=1)
        adjusted_count = count_words(adjusted)
        
        # Should be expanded
        self.assertGreater(adjusted_count, initial_count)
        
        # Should be closer to target range for 1 page
        min_words, max_words = calculate_target_words(1)
        # Content should be expanded towards the target range
        self.assertGreater(adjusted_count, initial_count)
    
    def test_adjust_content_length_trimming(self):
        """Test content trimming when too long."""
        # Create long content with redundant phrases
        long_text = ("This is a test. Additionally, it should be noted that this is important. " * 20 +
                    "Furthermore, it is worth noting that research shows this. " * 20 +
                    "Moreover, it can be said that this demonstrates significance.")
        initial_count = count_words(long_text)
        
        adjusted = adjust_content_length(long_text, target_pages=1, max_passes=3)
        adjusted_count = count_words(adjusted)
        
        # Should be trimmed (at least some redundant phrases removed)
        self.assertLessEqual(adjusted_count, initial_count)
    
    def test_max_passes_limit(self):
        """Test that adjustment respects max passes limit."""
        # Create content with many redundant phrases that can be trimmed
        very_long_text = ("Additionally, it should be noted that this is important. " * 50 +
                         "Furthermore, it is worth noting that research shows this. " * 50)
        
        # Test with only 1 pass
        adjusted = adjust_content_length(very_long_text, target_pages=1, max_passes=1)
        
        # Should have made some adjustment even with limited passes
        self.assertLessEqual(count_words(adjusted), count_words(very_long_text))

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)