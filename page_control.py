"""Page control module for managing word count and page targets."""

import re
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

# Target words per page (±5% tolerance)
TARGET_WORDS_PER_PAGE = 360
TOLERANCE_PERCENT = 0.05
MIN_WORDS_PER_PAGE = int(TARGET_WORDS_PER_PAGE * (1 - TOLERANCE_PERCENT))
MAX_WORDS_PER_PAGE = int(TARGET_WORDS_PER_PAGE * (1 + TOLERANCE_PERCENT))

def count_words(text: str) -> int:
    """Count words in text, excluding common formatting elements."""
    # Remove extra whitespace and count words
    cleaned_text = re.sub(r'\s+', ' ', text.strip())
    if not cleaned_text:
        return 0
    return len(cleaned_text.split())

def calculate_target_words(target_pages: int) -> Tuple[int, int]:
    """Calculate target word count range for given number of pages."""
    min_words = target_pages * MIN_WORDS_PER_PAGE
    max_words = target_pages * MAX_WORDS_PER_PAGE
    return min_words, max_words

def adjust_content_length(content: str, target_pages: int, max_passes: int = 3) -> str:
    """
    Adjust content length to match target page count.
    
    Args:
        content: The content to adjust
        target_pages: Target number of pages
        max_passes: Maximum adjustment passes
        
    Returns:
        Adjusted content
    """
    min_words, max_words = calculate_target_words(target_pages)
    current_words = count_words(content)
    
    logger.info(f"Current words: {current_words}, Target range: {min_words}-{max_words}")
    
    # If within range, return as-is
    if min_words <= current_words <= max_words:
        return content
    
    adjusted_content = content
    
    for pass_num in range(max_passes):
        current_words = count_words(adjusted_content)
        
        if min_words <= current_words <= max_words:
            logger.info(f"Content adjusted to target range in {pass_num + 1} passes")
            break
            
        if current_words < min_words:
            # Need to expand content
            adjusted_content = _expand_content(adjusted_content, min_words - current_words)
        elif current_words > max_words:
            # Need to trim content
            adjusted_content = _trim_content(adjusted_content, current_words - max_words)
            
        logger.info(f"Pass {pass_num + 1}: Adjusted to {count_words(adjusted_content)} words")
    
    return adjusted_content

def _expand_content(content: str, words_needed: int) -> str:
    """Expand content by adding elaborative sentences and details."""
    sentences = [s.strip() for s in content.split('.') if s.strip()]
    expanded_sentences = []
    
    words_added = 0
    expansion_phrases = [
        "Furthermore, this aspect is particularly important because it demonstrates the significance of this topic",
        "Additionally, it should be noted that research in this area has shown considerable development",
        "Moreover, research indicates that these findings contribute to our understanding of the subject matter",
        "It is also worth mentioning that contemporary studies have revealed new insights",
        "In this context, it becomes clear that further investigation is warranted",
        "This observation leads us to understand that multiple perspectives must be considered",
        "Consequently, we can observe that the implications are far-reaching",
        "As a result of this analysis, several important conclusions can be drawn",
    ]
    
    phrase_idx = 0
    
    for i, sentence in enumerate(sentences):
        expanded_sentences.append(sentence)
        
        # Add expansion after each sentence if we still need words
        if words_added < words_needed:
            expansion = expansion_phrases[phrase_idx % len(expansion_phrases)]
            expanded_sentences.append(expansion)
            words_added += count_words(expansion)
            phrase_idx += 1
            
            if words_added >= words_needed:
                break
    
    # If we still need more words, add more elaboration
    while words_added < words_needed and phrase_idx < len(expansion_phrases) * 2:
        expansion = expansion_phrases[phrase_idx % len(expansion_phrases)]
        expanded_sentences.append(expansion)
        words_added += count_words(expansion)
        phrase_idx += 1
    
    return '. '.join(expanded_sentences) + '.'

def _trim_content(content: str, words_to_remove: int) -> str:
    """Trim content by removing redundant phrases and shortening sentences."""
    # Split into sentences
    sentences = [s.strip() for s in content.split('.') if s.strip()]
    
    # Remove empty sentences and excessive elaboration
    trimmed_sentences = []
    words_removed = 0
    
    redundant_phrases = [
        "it should be noted that",
        "it is important to mention that", 
        "furthermore, it is worth noting that",
        "additionally, we should consider that",
        "moreover, it can be said that",
        "as previously mentioned",
        "in other words",
        "to put it simply",
        "furthermore, this aspect is particularly important because it demonstrates the significance of this topic",
        "additionally, it should be noted that research in this area has shown considerable development",
    ]
    
    for sentence in sentences:
        if not sentence.strip():
            continue
            
        trimmed_sentence = sentence
        
        # Remove redundant phrases
        for phrase in redundant_phrases:
            if phrase in trimmed_sentence.lower() and words_removed < words_to_remove:
                old_length = count_words(trimmed_sentence)
                trimmed_sentence = trimmed_sentence.replace(phrase, "").strip()
                # Clean up double spaces
                trimmed_sentence = ' '.join(trimmed_sentence.split())
                new_length = count_words(trimmed_sentence)
                words_removed += (old_length - new_length)
        
        if trimmed_sentence:  # Only add non-empty sentences
            trimmed_sentences.append(trimmed_sentence)
        
        if words_removed >= words_to_remove:
            # Add remaining sentences as-is
            remaining_start = len(trimmed_sentences)
            for remaining_sentence in sentences[remaining_start:]:
                if remaining_sentence.strip():
                    trimmed_sentences.append(remaining_sentence)
            break
    
    return '. '.join(trimmed_sentences) + '.' if trimmed_sentences else content

def get_page_estimate(content: str) -> float:
    """Estimate number of pages for given content."""
    word_count = count_words(content)
    return word_count / TARGET_WORDS_PER_PAGE