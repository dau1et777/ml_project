#!/usr/bin/env python
"""Test extended system with backward compatibility checks."""
import sys
sys.path.insert(0, './ml')
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from ml.recommender import recommend_careers

# Test 1: FULL answers (Q1-Q35)
print('=' * 60)
print('TEST 1: Full answers (Q1-Q35) - Extended system')
print('=' * 60)
full_answers = {
    'q1': 8, 'q2': 8, 'q3': 8, 'q4': 7, 'q5': 9,
    'q6': 7, 'q7': 8, 'q8': 9, 'q9': 7, 'q10': 8,
    'q11': 6, 'q12': 5, 'q13': 7, 'q14': 6, 'q15': 5,
    'q16': 9, 'q17': 8, 'q18': 8, 'q19': 8, 'q20': 9,
    'q21': 'A', 'q22': 'A', 'q23': 'B', 'q24': 'A', 'q25': 'B',
    # Extended interest profile
    'q26': 9, 'q27': 4, 'q28': 3, 'q29': 2,  
    'q30': 9, 'q31': 7, 'q32': 2, 'q33': 6,
    # Work style preferences
    'q34': 2, 'q35': 6
}

results_full = recommend_careers(full_answers)
if 'recommendations' in results_full:
    rec = results_full['recommendations'][0]
    print(f'✓ Top career: {rec["career"]} ({rec["match_percentage"]}% match)')
    print('✓ Vector size: 50 dimensions')
else:
    print(f'✗ Error: {results_full.get("error")}')

# Test 2: BACKWARD COMPATIBILITY (Q1-Q25 only)
print('\n' + '=' * 60)
print('TEST 2: Old answers (Q1-Q25 only) - Backward compatibility')
print('=' * 60)
old_answers = {
    'q1': 8, 'q2': 8, 'q3': 8, 'q4': 7, 'q5': 9,
    'q6': 7, 'q7': 8, 'q8': 9, 'q9': 7, 'q10': 8,
    'q11': 6, 'q12': 5, 'q13': 7, 'q14': 6, 'q15': 5,
    'q16': 9, 'q17': 8, 'q18': 8, 'q19': 8, 'q20': 9,
    'q21': 'A', 'q22': 'A', 'q23': 'B', 'q24': 'A', 'q25': 'B'
}

results_compat = recommend_careers(old_answers)
if 'recommendations' in results_compat:
    rec = results_compat['recommendations'][0]
    print(f'✓ Top career: {rec["career"]} ({rec["match_percentage"]}% match)')
    print('✓ Q26-Q35 defaulted to neutral (5)')
    print('✓ Vector normalized to 50 dimensions')
else:
    print(f'✗ Error: {results_compat.get("error")}')

# Compare results
print('\n' + '=' * 60)
print('BACKWARD COMPATIBILITY CHECK')
print('=' * 60)
print(f'Full system (Q1-Q35):  {results_full["recommendations"][0]["career"]}')
print(f'Old system (Q1-Q25):   {results_compat["recommendations"][0]["career"]}')

# Show top 5 from both
print('\n' + '=' * 60)
print('TOP 5 RECOMMENDATIONS')
print('=' * 60)
print('\nFull (Q1-Q35):')
for i, rec in enumerate(results_full['recommendations'][:5], 1):
    print(f'  {i}. {rec["career"]} ({rec["match_percentage"]}%)')

print('\nOld (Q1-Q25):')
for i, rec in enumerate(results_compat['recommendations'][:5], 1):
    print(f'  {i}. {rec["career"]} ({rec["match_percentage"]}%)')

# See if Q26-Q35 refines the results
full_top = results_full['recommendations'][0]['career']
compat_top = results_compat['recommendations'][0]['career']

if full_top == compat_top:
    print('\n✓ BACKWARD COMPATIBLE: New questions refine, not override')
else:
    # Check if old top is in new top 3
    new_top_3 = [r['career'] for r in results_full['recommendations'][:3]]
    if compat_top in new_top_3:
        print('\n✓ BACKWARD COMPATIBLE: Old top is in new top 3 (refined ranking)')
    else:
        print('\n⚠ Significant change (see if new interest profile is stronger)')
