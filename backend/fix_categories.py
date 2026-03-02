"""
Fix Career Categories
Updates careers with 'other' category to specific categories
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from career_app.models import Career

def fix_categories():
    """Fix career categories that are set to 'other'"""
    
    careers = Career.objects.all()
    updated_count = 0
    
    print("Fixing career categories...\n")
    
    for career in careers:
        career_lower = career.name.lower()
        new_category = None
        
        # Finance (check first for CFO, venture capitalist, etc.)
        if 'cfo' in career_lower or 'chief financial' in career_lower or 'venture' in career_lower or 'compliance' in career_lower:
            new_category = 'finance'
        elif any(word in career_lower for word in ['banker', 'investment', 'treasurer', 'auditor']):
            new_category = 'finance'
        # Science & Research
        elif any(word in career_lower for word in ['scientist', 'chemist', 'physicist', 'biologist', 'biotechnologist', 'researcher', 'research', 'statistician', 'statistic']):
            new_category = 'science'
        # Marketing
        elif any(word in career_lower for word in ['marketing', 'seo', 'brand']):
            new_category = 'marketing'
        # Technology
        elif 'scrum' in career_lower or 'administrator' in career_lower:
            new_category = 'technology'
        elif any(word in career_lower for word in ['engineer', 'developer', 'programmer', 'architect', 'data', 'mobile', 'backend', 'frontend', 'web', 'software', 'tech', 'ai', 'ml']):
            new_category = 'technology'
        # Creative & Design
        elif 'music' in career_lower or 'video' in career_lower or 'film' in career_lower or 'actor' in career_lower or 'photograph' in career_lower or 'journalist' in career_lower or 'producer' in career_lower:
            new_category = 'creative'
        elif any(word in career_lower for word in ['designer', 'ux', 'ui', 'artist', 'creative', 'writer', 'copywriter', 'content', 'illustration', 'animation', 'design', 'performer']):
            new_category = 'creative'
        # Healthcare
        elif 'health' in career_lower or 'social worker' in career_lower:
            new_category = 'healthcare'
        elif any(word in career_lower for word in ['doctor', 'nurse', 'physician', 'therapist', 'healthcare', 'medical']):
            new_category = 'healthcare'
        # Education
        elif 'learning' in career_lower:
            new_category = 'education'
        elif any(word in career_lower for word in ['teacher', 'professor', 'educator', 'instructor']):
            new_category = 'education'
        # Business & Management
        elif any(word in career_lower for word in ['manager', 'director', 'consultant', 'owner', 'planner', 'strategist', 'analyst', 'accountant', 'business', 'tax', 'operations', 'sales', 'programme', 'ceo', 'cpo', 'chief', 'officer', 'entrepreneur', 'founder', 'lawyer', 'government', 'official']):
            new_category = 'business'
        
        # Update if category changed
        if new_category and new_category != career.category:
            old_category = career.category
            career.category = new_category
            career.save()
            updated_count += 1
            print(f"  ✓ Updated: {career.name}")
            print(f"    {old_category} → {new_category}")
    
    if updated_count == 0:
        print("✓ All careers already have correct categories!")
    else:
        print(f"\n✓ Successfully updated {updated_count} careers")
    
    # Show category breakdown
    print("\nCategory breakdown:")
    categories = Career.objects.values_list('category', flat=True)
    from collections import Counter
    category_counts = Counter(categories)
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count}")

if __name__ == '__main__':
    fix_categories()
