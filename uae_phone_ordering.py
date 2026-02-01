"""
UAE Telephone Number Ordering Function

This module provides functionality to order UAE telephone numbers
according to local people's preferences.

UAE telephone number preferences typically include:
1. Mobile carrier preferences (Etisalat and Du are major carriers)
2. Numbers with repeating digits (considered lucky)
3. Numbers with sequential patterns
4. Avoiding numbers with 4 (sometimes considered unlucky in some cultures)
"""

import re
from typing import List, Dict, Any


def parse_uae_phone(phone: str) -> Dict[str, Any]:
    """
    Parse a UAE telephone number and extract relevant information.
    
    Args:
        phone: UAE phone number (can include +971 or 00971 prefix, or just the local number)
    
    Returns:
        Dictionary containing parsed phone information
    """
    # Remove common separators and spaces
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Remove country code if present
    if cleaned.startswith('+971'):
        cleaned = cleaned[4:]
    elif cleaned.startswith('00971'):
        cleaned = cleaned[5:]
    elif cleaned.startswith('971'):
        cleaned = cleaned[3:]
    
    # Extract prefix (first 2 digits for mobile, or area code)
    prefix = cleaned[:2] if len(cleaned) >= 2 else cleaned
    
    return {
        'original': phone,
        'cleaned': cleaned,
        'prefix': prefix,
        'full_number': cleaned
    }


def count_repeating_digits(number: str) -> int:
    """Count sequences of repeating digits in a number."""
    count = 0
    i = 0
    while i < len(number):
        j = i
        while j < len(number) and number[j] == number[i]:
            j += 1
        length = j - i
        if length >= 2:
            count += length - 1
        i = j
    return count


def count_sequential_patterns(number: str) -> int:
    """Count sequential digit patterns (ascending or descending)."""
    count = 0
    for i in range(len(number) - 2):
        # Check for ascending sequence
        if len(number) > i + 2:
            try:
                d1, d2, d3 = int(number[i]), int(number[i+1]), int(number[i+2])
                if d2 == d1 + 1 and d3 == d2 + 1:
                    count += 1
                elif d2 == d1 - 1 and d3 == d2 - 1:
                    count += 1
            except ValueError:
                pass
    return count


def calculate_preference_score(phone_info: Dict[str, Any]) -> float:
    """
    Calculate a preference score for a UAE phone number based on local preferences.
    
    Higher scores indicate more preferred numbers.
    
    Scoring criteria:
    - Mobile numbers (50, 52, 54, 55, 56, 58) get bonus points
    - Repeating digits add to score
    - Sequential patterns add to score
    - Numbers containing 7 or 8 (considered lucky) get bonus
    - Premium prefixes (50, 55, 56) get higher scores
    """
    score = 0.0
    number = phone_info['cleaned']
    prefix = phone_info['prefix']
    
    # Premium mobile prefixes (most preferred carriers/series)
    premium_prefixes = ['50', '55', '56']
    good_prefixes = ['52', '54', '58']
    
    if prefix in premium_prefixes:
        score += 10.0
    elif prefix in good_prefixes:
        score += 7.0
    elif prefix in ['04', '02', '03', '06', '07', '09']:  # Landline prefixes
        score += 3.0
    
    # Repeating digits are highly valued
    repeating_count = count_repeating_digits(number)
    score += repeating_count * 3.0
    
    # Sequential patterns
    sequential_count = count_sequential_patterns(number)
    score += sequential_count * 2.0
    
    # Lucky numbers (7 and 8 are considered lucky)
    score += number.count('7') * 0.5
    score += number.count('8') * 0.5
    
    # Avoid numbers with many 4s (sometimes considered unlucky)
    score -= number.count('4') * 0.3
    
    # Round numbers (ending in 00, 000, etc.) are preferred
    if number.endswith('000'):
        score += 5.0
    elif number.endswith('00'):
        score += 3.0
    elif number.endswith('0'):
        score += 1.0
    
    return score


def order_uae_phones(phone_numbers: List[str]) -> List[str]:
    """
    Order UAE telephone numbers according to local people's preferences.
    
    Args:
        phone_numbers: List of UAE phone numbers to order
    
    Returns:
        List of phone numbers ordered by preference (most preferred first)
    
    Example:
        >>> phones = ['+971 50 123 4567', '+971 55 777 7777', '+971 4 123 4567']
        >>> ordered = order_uae_phones(phones)
    """
    # Parse all phone numbers
    parsed_phones = [parse_uae_phone(phone) for phone in phone_numbers]
    
    # Calculate scores
    for phone_info in parsed_phones:
        phone_info['score'] = calculate_preference_score(phone_info)
    
    # Sort by score (descending - highest preference first)
    sorted_phones = sorted(parsed_phones, key=lambda x: x['score'], reverse=True)
    
    # Return original phone numbers in sorted order
    return [phone['original'] for phone in sorted_phones]


def main():
    """Example usage of the UAE phone ordering function."""
    # Example: 50 UAE telephone numbers
    sample_phones = [
        '+971 50 123 4567',
        '+971 55 777 7777',  # Many repeating 7s - high preference
        '+971 52 234 5678',  # Sequential pattern
        '+971 56 888 8888',  # Many repeating 8s - high preference
        '+971 54 111 1111',  # Many repeating 1s
        '+971 50 999 9999',  # Many repeating 9s
        '+971 4 123 4567',   # Dubai landline
        '+971 2 234 5678',   # Abu Dhabi landline
        '+971 58 345 6789',
        '+971 50 100 0000',  # Round number
        '+971 55 200 0000',  # Round number
        '+971 52 321 4321',  # Pattern
        '+971 56 456 7890',  # Sequential
        '+971 54 555 5555',  # All 5s
        '+971 50 678 9012',
        '+971 55 123 3210',
        '+971 52 444 4444',  # Many 4s - lower preference
        '+971 56 567 8901',
        '+971 58 789 0123',
        '+971 50 890 1234',
        '+971 55 901 2345',
        '+971 52 012 3456',
        '+971 54 234 5670',
        '+971 56 345 6700',
        '+971 58 456 7000',
        '+971 50 567 8000',
        '+971 55 678 9000',
        '+971 52 789 0100',
        '+971 54 890 1200',
        '+971 56 901 2300',
        '+971 58 123 4500',
        '+971 50 234 5600',
        '+971 55 345 6700',
        '+971 52 456 7800',
        '+971 54 567 8900',
        '+971 56 678 9100',
        '+971 58 789 1200',
        '+971 50 890 2300',
        '+971 55 901 3400',
        '+971 52 112 2334',
        '+971 54 223 3445',
        '+971 56 334 4556',
        '+971 58 445 5667',
        '+971 50 556 6778',
        '+971 55 667 7889',
        '+971 52 778 8990',
        '+971 54 889 9001',
        '+971 56 990 0112',
        '+971 58 101 1223',
        '+971 50 212 2334',
    ]
    
    print(f"Ordering {len(sample_phones)} UAE telephone numbers by local preference...\n")
    
    ordered_phones = order_uae_phones(sample_phones)
    
    print("Top 10 Most Preferred Numbers:")
    print("-" * 50)
    for i, phone in enumerate(ordered_phones[:10], 1):
        phone_info = parse_uae_phone(phone)
        score = calculate_preference_score(phone_info)
        print(f"{i:2d}. {phone:20s} (Score: {score:.1f})")
    
    print("\n" + "=" * 50)
    print("\nAll Ordered Numbers:")
    print("-" * 50)
    for i, phone in enumerate(ordered_phones, 1):
        phone_info = parse_uae_phone(phone)
        score = calculate_preference_score(phone_info)
        print(f"{i:2d}. {phone:20s} (Score: {score:.1f})")


if __name__ == '__main__':
    main()
