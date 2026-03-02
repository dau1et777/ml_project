"""
Django signals for Career Guidance Platform.
Handles post-migration data initialization.
"""
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import QuizQuestion, Career, Skill, CareerSkill


@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    """
    Create default quiz questions, careers, and skills after migration.
    This runs once after migrations are applied.
    """
    # Create quiz questions if they don't exist
    if QuizQuestion.objects.count() == 0:
        _create_quiz_questions()
    
    # Create careers if they don't exist
    if Career.objects.count() == 0:
        _create_careers()
    
    # Create skills if they don't exist
    if Skill.objects.count() == 0:
        _create_skills()
    
    # Create career-skill relationships
    if CareerSkill.objects.count() == 0:
        _create_career_skills()


def _create_quiz_questions():
    """Create the 35 quiz questions."""
    questions = [
        # Q1-Q20: Cognitive and personality dimensions (scales 1-10)
        {'order': 1, 'text': 'How comfortable are you with complex analytical problems?', 'type': 'scale', 'category': 'cognitive'},
        {'order': 2, 'text': 'How much do you enjoy working with people?', 'type': 'scale', 'category': 'cognitive'},
        {'order': 3, 'text': 'How creative do you consider yourself?', 'type': 'scale', 'category': 'cognitive'},
        {'order': 4, 'text': 'How organized and detail-oriented are you?', 'type': 'scale', 'category': 'cognitive'},
        {'order': 5, 'text': 'How comfortable are you with public speaking?', 'type': 'scale', 'category': 'cognitive'},
        {'order': 6, 'text': 'How much do you enjoy learning new technologies?', 'type': 'scale', 'category': 'cognitive'},
        {'order': 7, 'text': 'How comfortable are you with uncertainty and change?', 'type': 'scale', 'category': 'cognitive'},
        {'order': 8, 'text': 'How much do you prefer working independently?', 'type': 'scale', 'category': 'cognitive'},
        {'order': 9, 'text': 'How driven are you by financial rewards?', 'type': 'scale', 'category': 'motivation'},
        {'order': 10, 'text': 'How important is work-life balance to you?', 'type': 'scale', 'category': 'motivation'},
        {'order': 11, 'text': 'How much do you value helping others?', 'type': 'scale', 'category': 'motivation'},
        {'order': 12, 'text': 'How important is job security to you?', 'type': 'scale', 'category': 'motivation'},
        {'order': 13, 'text': 'How much do you enjoy leadership roles?', 'type': 'scale', 'category': 'motivation'},
        {'order': 14, 'text': 'How important is environmental impact in your career choice?', 'type': 'scale', 'category': 'motivation'},
        {'order': 15, 'text': 'How much do you prefer structured environments?', 'type': 'scale', 'category': 'cognitive'},
        {'order': 16, 'text': 'How important is continuous learning and development?', 'type': 'scale', 'category': 'motivation'},
        {'order': 17, 'text': 'How comfortable are you with ethical dilemmas?', 'type': 'scale', 'category': 'cognitive'},
        {'order': 18, 'text': 'How much do you enjoy competitive environments?', 'type': 'scale', 'category': 'cognitive'},
        {'order': 19, 'text': 'How important is flexibility in work location to you?', 'type': 'scale', 'category': 'motivation'},
        {'order': 20, 'text': 'How much do you enjoy problem-solving?', 'type': 'scale', 'category': 'cognitive'},
        
        # Q21-Q25: Motivation style (choices)
        {'order': 21, 'text': 'What primarily motivates you?', 'type': 'choice', 'options': {'A': 'Money and compensation', 'B': 'Impact and meaning', 'C': 'Growth and learning', 'D': 'Stability and security'}, 'category': 'motivation'},
        {'order': 22, 'text': 'What work environment appeals to you most?', 'type': 'choice', 'options': {'A': 'Large corporations', 'B': 'Startups', 'C': 'Non-profits', 'D': 'Freelance/Self-employed'}, 'category': 'work_style'},
        {'order': 23, 'text': 'How do you prefer to work?', 'type': 'choice', 'options': {'A': 'Team-based projects', 'B': 'Individual tasks', 'C': 'Mixed', 'D': 'Leadership roles'}, 'category': 'work_style'},
        {'order': 24, 'text': 'What type of problems do you prefer solving?', 'type': 'choice', 'options': {'A': 'Technical', 'B': 'Business', 'C': 'Creative', 'D': 'Social'}, 'category': 'cognitive'},
        {'order': 25, 'text': 'What is your ideal career timeline?', 'type': 'choice', 'options': {'A': 'Quick entry and impact', 'B': 'Steady long-term growth', 'C': 'Flexible and exploratory', 'D': 'Specialized expertise'}, 'category': 'motivation'},
        
        # Q26-Q33: Interest areas (8 dimensions - scales 1-10)
        {'order': 26, 'text': 'Interest in Technology and Programming', 'type': 'scale', 'category': 'interests'},
        {'order': 27, 'text': 'Interest in Business and Entrepreneurship', 'type': 'scale', 'category': 'interests'},
        {'order': 28, 'text': 'Interest in Creative fields (Design, Art, Media)', 'type': 'scale', 'category': 'interests'},
        {'order': 29, 'text': 'Interest in Social and People-focused work', 'type': 'scale', 'category': 'interests'},
        {'order': 30, 'text': 'Interest in Data and Analytics', 'type': 'scale', 'category': 'interests'},
        {'order': 31, 'text': 'Interest in Product Development', 'type': 'scale', 'category': 'interests'},
        {'order': 32, 'text': 'Interest in Education and Training', 'type': 'scale', 'category': 'interests'},
        {'order': 33, 'text': 'Interest in Operations and Management', 'type': 'scale', 'category': 'interests'},
        
        # Q34-Q35: Work style refinement (scales 1-10)
        {'order': 34, 'text': 'Preference for Independent vs Collaborative work', 'type': 'scale', 'category': 'work_style'},
        {'order': 35, 'text': 'Preference for Remote vs Office work', 'type': 'scale', 'category': 'work_style'},
    ]
    
    for q in questions:
        QuizQuestion.objects.create(
            text=q['text'],
            question_type='scale' if q['type'] == 'scale' else 'choice',
            options=q.get('options', None),
            category=q['category'],
            order=q['order'],
            weight=1.0
        )


def _create_careers():
    """Create 85 career profiles."""
    careers = [
        # Technology Careers
        ('Software Engineer', 'Develop applications and systems using programming languages', 80000, 200000, 'high'),
        ('Data Scientist', 'Analyze complex datasets to drive business decisions', 90000, 180000, 'high'),
        ('Machine Learning Engineer', 'Build and deploy machine learning models and systems', 100000, 220000, 'high'),
        ('Full Stack Developer', 'Develop both frontend and backend web applications', 85000, 180000, 'high'),
        ('DevOps Engineer', 'Manage infrastructure, deployment, and system operations', 95000, 200000, 'high'),
        ('Cloud Architect', 'Design and implement cloud solutions', 110000, 250000, 'medium'),
        ('Security Engineer', 'Protect systems and networks from cyber threats', 100000, 210000, 'high'),
        ('Database Administrator', 'Manage and optimize database systems', 85000, 160000, 'medium'),
        ('Systems Administrator', 'Maintain and support IT infrastructure', 70000, 140000, 'medium'),
        ('QA Engineer', 'Test software quality and automation', 75000, 150000, 'high'),
        
        # Business & Finance
        ('Management Consultant', 'Advise organizations on strategy and operations', 95000, 250000, 'medium'),
        ('Business Analyst', 'Analyze business processes and requirements', 80000, 160000, 'high'),
        ('Financial Analyst', 'Analyze financial data and prepare reports', 85000, 180000, 'high'),
        ('Investment Manager', 'Manage investment portfolios and strategies', 100000, 500000, 'low'),
        ('Accountant', 'Prepare and examine financial records', 70000, 150000, 'medium'),
        ('Marketing Manager', 'Develop and execute marketing strategies', 85000, 180000, 'high'),
        ('Product Manager', 'Oversee product development and strategy', 95000, 200000, 'high'),
        ('Sales Manager', 'Lead and manage sales teams', 80000, 200000, 'medium'),
        ('Channel Manager', 'Manage partner channels and relationships', 85000, 180000, 'medium'),
        ('Procurement Manager', 'Manage vendor relationships and purchasing', 80000, 170000, 'medium'),
        ('Operations Manager', 'Manage business operations and efficiency', 80000, 160000, 'medium'),
        ('HR Manager', 'Manage human resources and employee relations', 75000, 150000, 'medium'),
        
        # Creative & Design
        ('UX/UI Designer', 'Design user interfaces and user experiences', 80000, 160000, 'high'),
        ('Graphic Designer', 'Create visual content for various media', 60000, 130000, 'medium'),
        ('Product Designer', 'Design products for market', 85000, 180000, 'high'),
        ('Motion Designer', 'Create animated graphics and motion content', 70000, 150000, 'medium'),
        ('Brand Designer', 'Develop and maintain brand visual identity', 75000, 160000, 'medium'),
        ('Game Developer', 'Develop video games', 80000, 180000, 'high'),
        ('AR/VR Developer', 'Create augmented and virtual reality experiences', 90000, 200000, 'high'),
        ('Animation Director', 'Direct animation projects and teams', 85000, 180000, 'low'),
        ('Creative Director', 'Lead creative vision for projects', 90000, 220000, 'low'),
        ('Content Creator', 'Create content for digital platforms', 50000, 150000, 'medium'),
        
        # Education & Training
        ('Teacher', 'Educate students in academic subjects', 50000, 90000, 'medium'),
        ('Corporate Trainer', 'Develop and deliver training programs', 65000, 140000, 'medium'),
        ('Instructional Designer', 'Design learning experiences and courses', 70000, 150000, 'medium'),
        ('Curriculum Developer', 'Develop educational curriculum', 65000, 130000, 'low'),
        ('Education Consultant', 'Advise on educational programs and strategy', 75000, 160000, 'low'),
        ('Online Learning Specialist', 'Develop online educational content', 70000, 140000, 'medium'),
        ('EdTech Developer', 'Develop educational technology solutions', 80000, 180000, 'high'),
        ('University Professor', 'Teach and conduct research at university', 70000, 150000, 'low'),
        
        # Healthcare & Social
        ('User Experience Researcher', 'Research user needs and behaviors', 80000, 160000, 'medium'),
        ('Data Analyst', 'Analyze data to inform business decisions', 75000, 160000, 'high'),
        ('Clinical Data Manager', 'Manage clinical research data', 70000, 140000, 'medium'),
        ('Healthcare Manager', 'Manage healthcare operations and staff', 80000, 160000, 'medium'),
        ('Therapist/Counselor', 'Provide mental health support', 60000, 120000, 'medium'),
        ('Social Worker', 'Assist vulnerable populations', 55000, 100000, 'medium'),
        ('Public Health Specialist', 'Work on public health initiatives', 65000, 130000, 'medium'),
        ('Non-profit Manager', 'Manage non-profit organizations', 70000, 140000, 'medium'),
        
        # Engineering (Specialized)
        ('Mechanical Engineer', 'Design mechanical systems and products', 80000, 160000, 'medium'),
        ('Civil Engineer', 'Design infrastructure and buildings', 75000, 150000, 'medium'),
        ('Electrical Engineer', 'Design electrical systems', 85000, 170000, 'medium'),
        ('Chemical Engineer', 'Design chemical manufacturing processes', 85000, 170000, 'medium'),
        ('Software Architect', 'Design large-scale software systems', 120000, 250000, 'low'),
        ('Release Manager', 'Manage software release processes', 90000, 180000, 'medium'),
        ('Technical Lead', 'Lead technical teams and projects', 100000, 200000, 'medium'),
        ('Engineering Manager', 'Manage engineering teams', 110000, 230000, 'low'),
        
        # Sales & Business Development
        ('Business Development Manager', 'Identify and develop new business opportunities', 80000, 200000, 'medium'),
        ('Account Manager', 'Manage client relationships', 75000, 180000, 'medium'),
        ('Sales Representative', 'Sell products and services', 60000, 150000, 'high'),
        ('Entrepreneur', 'Start and manage own business', 40000, 1000000, 'low'),
        ('Startup Founder', 'Found and lead startup companies', 0, 500000, 'low'),
        
        # Research & Science
        ('Research Scientist', 'Conduct scientific research', 75000, 150000, 'low'),
        ('Lab Technician', 'Support laboratory research', 50000, 100000, 'medium'),
        ('Statistician', 'Analyze statistical data', 80000, 160000, 'low'),
        ('Researcher (Academia)', 'Conduct academic research', 70000, 140000, 'low'),
        
        # Arts & Media
        ('Journalist', 'Report news and information', 55000, 120000, 'medium'),
        ('Content Writer', 'Write content for various platforms', 50000, 120000, 'medium'),
        ('Video Producer', 'Produce video content', 65000, 150000, 'medium'),
        ('Photographer', 'Take photographs for clients', 50000, 120000, 'medium'),
        ('Music Producer', 'Produce music and audio', 60000, 180000, 'low'),
        ('Filmmaker', 'Create films and videos', 60000, 180000, 'low'),
        ('Actor/Performer', 'Perform in theater, film, TV', 30000, 200000, 'low'),
        
        # Legal & Government
        ('Lawyer', 'Provide legal services', 80000, 250000, 'low'),
        ('Legal Consultant', 'Consult on legal matters', 85000, 200000, 'low'),
        ('Compliance Officer', 'Ensure regulatory compliance', 85000, 170000, 'medium'),
        ('Government Official', 'Work in government agencies', 70000, 140000, 'low'),
        ('Policy Analyst', 'Analyze and develop policies', 75000, 150000, 'low'),
        
        # Miscellaneous
        ('Venture Capitalist', 'Invest in and support startups', 100000, 1000000, 'low'),
        ('Consultant', 'Provide expert advice to organizations', 85000, 250000, 'medium'),
        ('Project Manager', 'Manage project execution', 80000, 160000, 'high'),
        ('Scrum Master', 'Facilitate agile development teams', 80000, 160000, 'high'),
        ('Technical Writer', 'Write technical documentation', 70000, 140000, 'medium'),
        ('Solutions Architect', 'Design solutions for clients', 100000, 200000, 'medium'),
        
        # Executive Leadership
        ('Chief Executive Officer', 'Lead organization, set vision and strategy, report to Board', 200000, 1000000, 'low'),
        ('Chief Financial Officer', 'Oversee financial operations and strategy', 180000, 800000, 'low'),
        ('Chief Product Officer', 'Lead product strategy and development', 180000, 700000, 'low'),
        ('Director of Engineering', 'Direct engineering teams and technical strategy', 150000, 400000, 'low'),
    ]
    
    for name, desc, salary_min, salary_max, demand in careers:
        Career.objects.create(
            name=name,
            description=desc,
            salary_min=salary_min,
            salary_max=salary_max,
            demand_level=demand
        )


def _create_skills():
    """Create common skills."""
    skills = [
        # Technical Skills
        ('Python', 'technical'),
        ('JavaScript', 'technical'),
        ('Java', 'technical'),
        ('C++', 'technical'),
        ('React', 'technical'),
        ('Django', 'technical'),
        ('SQL', 'technical'),
        ('Machine Learning', 'technical'),
        ('Data Analysis', 'technical'),
        ('Cloud Computing (AWS/Azure/GCP)', 'technical'),
        ('Docker/Kubernetes', 'technical'),
        ('DevOps', 'technical'),
        ('API Design', 'technical'),
        ('Cybersecurity', 'technical'),
        ('Mobile Development', 'technical'),
        
        # Soft Skills
        ('Communication', 'soft'),
        ('Leadership', 'soft'),
        ('Project Management', 'soft'),
        ('Problem Solving', 'soft'),
        ('Critical Thinking', 'soft'),
        ('Teamwork', 'soft'),
        ('Creativity', 'soft'),
        ('Emotional Intelligence', 'soft'),
        ('Time Management', 'soft'),
        ('Negotiation', 'soft'),
        ('Presentation Skills', 'soft'),
        ('Conflict Resolution', 'soft'),
        
        # Domain Knowledge
        ('Finance', 'domain'),
        ('Healthcare', 'domain'),
        ('Marketing', 'domain'),
        ('Sales', 'domain'),
        ('Human Resources', 'domain'),
        ('Operations', 'domain'),
        ('Supply Chain', 'domain'),
        ('Product Development', 'domain'),
        ('User Experience', 'domain'),
        ('Business Strategy', 'domain'),
    ]
    
    for name, category in skills:
        Skill.objects.create(name=name, category=category)


def _create_career_skills():
    """Create relationships between careers and required skills."""
    career_skills = {
        'Software Engineer': [
            ('Python', 'intermediate'),
            ('API Design', 'intermediate'),
            ('Problem Solving', 'expert'),
            ('Teamwork', 'intermediate'),
        ],
        'Data Scientist': [
            ('Python', 'expert'),
            ('Data Analysis', 'expert'),
            ('Machine Learning', 'expert'),
            ('SQL', 'intermediate'),
            ('Communication', 'intermediate'),
        ],
        'Product Manager': [
            ('Business Strategy', 'expert'),
            ('Communication', 'expert'),
            ('Leadership', 'intermediate'),
            ('User Experience', 'intermediate'),
            ('Project Management', 'intermediate'),
        ],
        'UX/UI Designer': [
            ('User Experience', 'expert'),
            ('Creativity', 'expert'),
            ('Communication', 'intermediate'),
            ('Problem Solving', 'intermediate'),
        ],
        'Management Consultant': [
            ('Business Strategy', 'expert'),
            ('Communication', 'expert'),
            ('Leadership', 'expert'),
            ('Problem Solving', 'expert'),
            ('Critical Thinking', 'expert'),
        ],
        'Machine Learning Engineer': [
            ('Python', 'expert'),
            ('Machine Learning', 'expert'),
            ('Data Analysis', 'expert'),
            ('Problem Solving', 'expert'),
        ],
        'Marketing Manager': [
            ('Marketing', 'expert'),
            ('Communication', 'expert'),
            ('Leadership', 'intermediate'),
            ('Creativity', 'intermediate'),
            ('Data Analysis', 'intermediate'),
        ],
        'DevOps Engineer': [
            ('Docker/Kubernetes', 'expert'),
            ('Cloud Computing (AWS/Azure/GCP)', 'expert'),
            ('DevOps', 'expert'),
            ('Problem Solving', 'intermediate'),
        ],
        'Teacher': [
            ('Communication', 'expert'),
            ('Emotional Intelligence', 'expert'),
            ('Patience', 'expert'),
            ('Creativity', 'intermediate'),
        ],
        'Lawyer': [
            ('Communication', 'expert'),
            ('Critical Thinking', 'expert'),
            ('Problem Solving', 'intermediate'),
            ('Negotiation', 'expert'),
        ],
    }
    
    for career_name, skills in career_skills.items():
        try:
            career = Career.objects.get(name=career_name)
            for skill_name, proficiency in skills:
                try:
                    skill = Skill.objects.get(name=skill_name)
                    CareerSkill.objects.get_or_create(
                        career=career,
                        skill=skill,
                        defaults={'proficiency_level': proficiency}
                    )
                except Skill.DoesNotExist:
                    pass
        except Career.DoesNotExist:
            pass
