"""
Sync ML Careers to Database
Automatically adds any missing careers from ML system to database
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from career_app.models import Career

# Import ML careers
sys.path.insert(0, 'ml')
from careers import get_all_careers, get_career_description

def sync_careers():
    """Sync all ML careers to database"""
    
    # Get ML careers
    ml_careers = get_all_careers()
    print(f"Found {len(ml_careers)} careers in ML system")
    
    # Get existing DB careers
    db_career_names = set(Career.objects.values_list('name', flat=True))
    print(f"Found {len(db_career_names)} careers in database")
    
    # Find missing careers
    missing_careers = [c for c in ml_careers if c not in db_career_names]
    
    if not missing_careers:
        print("\n✓ All ML careers already exist in database!")
        return
    
    print(f"\nFound {len(missing_careers)} missing careers:")
    for career in sorted(missing_careers):
        print(f"  - {career}")
    
    print("\nAdding missing careers to database...")
    
    # Add missing careers
    added_count = 0
    for career_name in missing_careers:
        description = get_career_description(career_name)
        
        # Try to infer category from name
        career_lower = career_name.lower()
        
        # Finance (check first for CFO, venture capitalist, etc.)
        if 'cfo' in career_lower or 'chief financial' in career_lower or 'venture' in career_lower or 'compliance' in career_lower:
            category = 'finance'
        elif any(word in career_lower for word in ['banker', 'investment', 'treasurer', 'auditor']):
            category = 'finance'
        # Science & Research
        elif any(word in career_lower for word in ['scientist', 'chemist', 'physicist', 'biologist', 'biotechnologist', 'researcher', 'research', 'statistician', 'statistic']):
            category = 'science'
        # Marketing
        elif any(word in career_lower for word in ['marketing', 'seo', 'brand']):
            category = 'marketing'
        # Technology
        elif 'scrum' in career_lower or 'administrator' in career_lower:
            category = 'technology'
        elif any(word in career_lower for word in ['engineer', 'developer', 'programmer', 'architect', 'data', 'mobile', 'backend', 'frontend', 'web', 'software', 'tech', 'ai', 'ml']):
            category = 'technology'
        # Creative & Design
        elif 'music' in career_lower or 'video' in career_lower or 'film' in career_lower or 'actor' in career_lower or 'photograph' in career_lower or 'journalist' in career_lower or 'producer' in career_lower:
            category = 'creative'
        elif any(word in career_lower for word in ['designer', 'ux', 'ui', 'artist', 'creative', 'writer', 'copywriter', 'content', 'illustration', 'animation', 'design', 'performer']):
            category = 'creative'
        # Healthcare
        elif 'health' in career_lower or 'social worker' in career_lower:
            category = 'healthcare'
        elif any(word in career_lower for word in ['doctor', 'nurse', 'physician', 'therapist', 'healthcare', 'medical']):
            category = 'healthcare'
        # Education
        elif 'learning' in career_lower:
            category = 'education'
        elif any(word in career_lower for word in ['teacher', 'professor', 'educator', 'instructor']):
            category = 'education'
        # Business & Management
        elif any(word in career_lower for word in ['manager', 'director', 'consultant', 'owner', 'planner', 'strategist', 'analyst', 'accountant', 'business', 'tax', 'operations', 'sales', 'programme', 'ceo', 'cpo', 'chief', 'officer', 'entrepreneur', 'founder', 'lawyer', 'government', 'official']):
            category = 'business'
        else:
            category = 'business'
        
        # Create career with default salary ranges
        Career.objects.create(
            name=career_name,
            description=description or f"Professional career in {career_name.lower()}",
            category=category,
            salary_min=60000,
            salary_max=150000,
            demand_level='medium'
        )
        added_count += 1
        print(f"  ✓ Added: {career_name} ({category})")
    
    print(f"\n✓ Successfully added {added_count} careers to database")
    print(f"Total careers now: {Career.objects.count()}")

if __name__ == '__main__':
    sync_careers()
