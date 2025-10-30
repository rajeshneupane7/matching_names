#!/usr/bin/env python3

import sys
from thefuzz import fuzz

def find_unmatched_emails(main_list, comparison_list, threshold=60):
    """
    Finds items in main_list that do not have a match in
    comparison_list with a similarity score >= threshold.
    """
    non_matching_emails = []

    # Loop through every email in your main list
    for m_email in main_list:
        max_similarity = 0
        
        # Compare it against every email in the second list
        for c_email in comparison_list:
            similarity = fuzz.ratio(m_email, c_email)
            
            # Keep track of the highest match found
            if similarity > max_similarity:
                max_similarity = similarity
        
        # If the BEST match found is STILL less than the threshold,
        # then this email is a "non-match"
        if max_similarity < threshold:
            non_matching_emails.append(m_email)
            
    return non_matching_emails

def read_emails_from_file(filepath):
    """Reads a file, returning a list of lines stripped of whitespace."""
    try:
        with open(filepath, 'r') as f:
            # Read lines, strip whitespace (like \n), and filter out empty lines
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: ./match_email.py <main_email_file> <comparison_email_file>", file=sys.stderr)
        print("Example: ./match_email.py main.txt compare.txt", file=sys.stderr)
        sys.exit(1)
        
    # Get file paths from arguments
    main_file = sys.argv[1]
    comparison_file = sys.argv[2]
    
    # Read email lists from files
    main_list = read_emails_from_file(main_file)
    comparison_list = read_emails_from_file(comparison_file)
    
    # Find the unmatched emails (using the default 60% threshold)
    unmatched = find_unmatched_emails(main_list, comparison_list)
    
    # Print the result to standard output
    if unmatched:
        print("Emails with no match above 60% similarity:")
        for email in unmatched:
            print(email)
    else:
        print("All emails found a match above 60% similarity.")



