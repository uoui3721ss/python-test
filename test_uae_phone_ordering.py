"""
Test cases for UAE telephone number ordering function
"""

import unittest
from uae_phone_ordering import (
    parse_uae_phone,
    count_repeating_digits,
    count_sequential_patterns,
    calculate_preference_score,
    order_uae_phones
)


class TestParseUAEPhone(unittest.TestCase):
    """Test cases for phone number parsing."""
    
    def test_parse_with_plus_prefix(self):
        """Test parsing phone with +971 prefix."""
        result = parse_uae_phone('+971 50 123 4567')
        self.assertEqual(result['prefix'], '50')
        self.assertEqual(result['cleaned'], '501234567')
    
    def test_parse_with_00_prefix(self):
        """Test parsing phone with 00971 prefix."""
        result = parse_uae_phone('00971 55 777 7777')
        self.assertEqual(result['prefix'], '55')
        self.assertEqual(result['cleaned'], '557777777')
    
    def test_parse_without_country_code(self):
        """Test parsing local number without country code."""
        result = parse_uae_phone('50 123 4567')
        self.assertEqual(result['prefix'], '50')
        self.assertEqual(result['cleaned'], '501234567')
    
    def test_parse_with_separators(self):
        """Test parsing phone with various separators."""
        result = parse_uae_phone('+971-50-123-4567')
        self.assertEqual(result['cleaned'], '501234567')
        
        result = parse_uae_phone('+971 (50) 123-4567')
        self.assertEqual(result['cleaned'], '501234567')


class TestRepeatingDigits(unittest.TestCase):
    """Test cases for counting repeating digits."""
    
    def test_no_repeating_digits(self):
        """Test number with no repeating digits."""
        self.assertEqual(count_repeating_digits('123456789'), 0)
    
    def test_some_repeating_digits(self):
        """Test number with some repeating digits."""
        self.assertEqual(count_repeating_digits('1223334444'), 6)
    
    def test_all_same_digits(self):
        """Test number with all same digits."""
        self.assertEqual(count_repeating_digits('7777777'), 6)
    
    def test_multiple_groups(self):
        """Test number with multiple groups of repeating digits."""
        count = count_repeating_digits('11223344')
        self.assertGreater(count, 0)


class TestSequentialPatterns(unittest.TestCase):
    """Test cases for counting sequential patterns."""
    
    def test_ascending_sequence(self):
        """Test ascending sequential pattern."""
        count = count_sequential_patterns('12345678')
        self.assertGreater(count, 0)
    
    def test_descending_sequence(self):
        """Test descending sequential pattern."""
        count = count_sequential_patterns('87654321')
        self.assertGreater(count, 0)
    
    def test_no_sequence(self):
        """Test number with no sequential pattern."""
        self.assertEqual(count_sequential_patterns('13579'), 0)
    
    def test_mixed_pattern(self):
        """Test number with mixed sequential patterns."""
        count = count_sequential_patterns('12387654')
        self.assertGreater(count, 0)


class TestPreferenceScore(unittest.TestCase):
    """Test cases for preference score calculation."""
    
    def test_premium_prefix_score(self):
        """Test that premium prefixes get higher scores."""
        phone1 = parse_uae_phone('+971 50 123 4567')
        phone2 = parse_uae_phone('+971 55 123 4567')
        phone3 = parse_uae_phone('+971 4 123 4567')
        
        score1 = calculate_preference_score(phone1)
        score2 = calculate_preference_score(phone2)
        score3 = calculate_preference_score(phone3)
        
        # Premium mobile should score higher than landline
        self.assertGreater(score1, score3)
        self.assertGreater(score2, score3)
    
    def test_repeating_digits_bonus(self):
        """Test that repeating digits increase score."""
        phone1 = parse_uae_phone('+971 50 777 7777')
        phone2 = parse_uae_phone('+971 50 123 4567')
        
        score1 = calculate_preference_score(phone1)
        score2 = calculate_preference_score(phone2)
        
        # More repeating digits should have higher score
        self.assertGreater(score1, score2)
    
    def test_round_number_bonus(self):
        """Test that round numbers get bonus points."""
        phone1 = parse_uae_phone('+971 50 100 0000')
        phone2 = parse_uae_phone('+971 50 123 4567')
        
        score1 = calculate_preference_score(phone1)
        score2 = calculate_preference_score(phone2)
        
        # Round number should have higher score
        self.assertGreater(score1, score2)


class TestOrderUAEPhones(unittest.TestCase):
    """Test cases for ordering phone numbers."""
    
    def test_order_basic(self):
        """Test basic ordering of phone numbers."""
        phones = [
            '+971 50 123 4567',
            '+971 55 777 7777',
            '+971 4 123 4567'
        ]
        
        ordered = order_uae_phones(phones)
        
        # Should have same length
        self.assertEqual(len(ordered), len(phones))
        
        # All phones should be present
        self.assertEqual(set(ordered), set(phones))
        
        # Phone with repeating 7s should be first (highest preference)
        self.assertEqual(ordered[0], '+971 55 777 7777')
    
    def test_order_maintains_original_format(self):
        """Test that ordering maintains original phone format."""
        phones = [
            '+971-50-123-4567',
            '+971 55 777 7777',
            '00971 4 123 4567'
        ]
        
        ordered = order_uae_phones(phones)
        
        # Original formats should be preserved
        for phone in phones:
            self.assertIn(phone, ordered)
    
    def test_order_fifty_numbers(self):
        """Test ordering exactly 50 numbers as specified in requirements."""
        # Generate 50 test phone numbers
        phones = []
        for i in range(50):
            prefix = ['50', '52', '54', '55', '56', '58'][i % 6]
            number = f'+971 {prefix} {i:03d} {i:04d}'
            phones.append(number)
        
        ordered = order_uae_phones(phones)
        
        # Should have exactly 50 numbers
        self.assertEqual(len(ordered), 50)
        
        # All numbers should be present
        self.assertEqual(set(ordered), set(phones))
    
    def test_empty_list(self):
        """Test ordering empty list."""
        ordered = order_uae_phones([])
        self.assertEqual(ordered, [])
    
    def test_single_number(self):
        """Test ordering single number."""
        phones = ['+971 50 123 4567']
        ordered = order_uae_phones(phones)
        self.assertEqual(ordered, phones)
    
    def test_score_ordering_consistency(self):
        """Test that numbers are consistently ordered by score."""
        phones = [
            '+971 50 123 4567',  # Regular number
            '+971 55 888 8888',  # Many repeating 8s
            '+971 56 100 0000',  # Round number
            '+971 52 444 4444',  # Many 4s (less preferred)
        ]
        
        ordered = order_uae_phones(phones)
        
        # Calculate scores in order
        scores = []
        for phone in ordered:
            phone_info = parse_uae_phone(phone)
            score = calculate_preference_score(phone_info)
            scores.append(score)
        
        # Scores should be in descending order
        for i in range(len(scores) - 1):
            self.assertGreaterEqual(scores[i], scores[i + 1],
                                   f"Score at position {i} should be >= score at position {i+1}")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_full_workflow(self):
        """Test complete workflow with realistic data."""
        phones = [
            '+971 50 123 4567',
            '+971 55 777 7777',
            '+971 52 234 5678',
            '+971 56 888 8888',
            '+971 54 111 1111',
            '+971 50 999 9999',
            '+971 4 123 4567',
            '+971 2 234 5678',
            '+971 58 345 6789',
            '+971 50 100 0000',
        ]
        
        ordered = order_uae_phones(phones)
        
        # Verify output
        self.assertEqual(len(ordered), len(phones))
        self.assertTrue(all(phone in ordered for phone in phones))
        
        # Top phones should have high-value patterns
        top_phone = ordered[0]
        self.assertIn('777', top_phone.replace(' ', '').replace('-', '') or
                     '888' in top_phone.replace(' ', '').replace('-', '') or
                     '999' in top_phone.replace(' ', '').replace('-', '') or
                     '111' in top_phone.replace(' ', '').replace('-', '') or
                     '000' in top_phone.replace(' ', '').replace('-', ''))


if __name__ == '__main__':
    unittest.main()
