"""
Career Vectors - 90 diverse in-demand careers with 40-dimensional vectors.

Vector Design Strategy:
- Each career vector reflects the skills/traits required
- High values in dimensions that matter for the career
- Low values in dimensions that don't matter
- All careers differ significantly to ensure variety

Examples:
- Software Engineer: HIGH cognitive, HIGH academic, MEDIUM creativity, LOW communication
- UX Designer: MEDIUM-HIGH cognitive, HIGH creativity, MEDIUM-HIGH communication, MEDIUM academic
- Sales Manager: LOW-MEDIUM cognitive, MEDIUM communication, HIGH leadership, MEDIUM academic
- Data Scientist: HIGH cognitive, HIGH academic, MEDIUM creativity, MEDIUM-LOW communication
- Product Manager: MEDIUM cognitive, MEDIUM-HIGH communication, HIGH leadership, HIGH academic
"""

import numpy as np


# Career database with descriptions
CAREER_DESCRIPTIONS = {
    # Software & Technology (1-15)
    "Software Engineer": "Design and develop applications, systems, and software solutions",
    "Machine Learning Engineer": "Build intelligent systems using AI/ML, develop algorithms, train models",
    "Data Scientist": "Analyze complex datasets, build predictive models, extract insights",
    "DevOps Engineer": "Manage infrastructure, deployment pipelines, system automation",
    "Cloud Architect": "Design scalable cloud solutions, optimize cloud infrastructure",
    "Frontend Developer": "Build user interfaces, web applications, optimize user experience",
    "Backend Developer": "Develop server logic, databases, APIs, system architecture",
    "Full Stack Developer": "Build complete web applications from frontend to backend",
    "Database Administrator": "Manage databases, ensure data security, optimize performance",
    "Systems Administrator": "Maintain IT infrastructure, network management, system support",
    "Security Engineer": "Design security solutions, identify vulnerabilities, protect systems",
    "QA Engineer": "Test software, identify bugs, ensure quality and reliability",
    "Game Developer": "Create games, develop game engines, optimize performance",
    "Mobile App Developer": "Develop iOS/Android applications, mobile solutions",
    "AI Research Scientist": "Conduct AI research, publish papers, advance ML techniques",
    
    # Data & Analytics (16-25)
    "Business Analyst": "Analyze business processes, identify solutions, improve efficiency",
    "Analytics Engineer": "Build data pipelines, analytics infrastructure, data modeling",
    "Data Engineer": "Design data systems, ETL pipelines, data warehouses",
    "Business Intelligence Analyst": "Create dashboards, analyze business metrics, support decisions",
    "Market Research Analyst": "Research markets, analyze consumer behavior, identify trends",
    "Financial Analyst": "Analyze financial data, create forecasts, support investments",
    "Risk Analyst": "Identify risks, build risk models, develop mitigation strategies",
    "Operations Analyst": "Optimize operations, analyze efficiency, improve processes",
    "User Research Specialist": "Conduct user studies, analyze behavior, inform design decisions",
    "Actuarial Scientist": "Calculate risk using mathematics and statistics",
    
    # Design (26-35)
    "UX Designer": "Design user experiences, conduct research, create prototypes",
    "UI Designer": "Design interfaces, visual design, design systems",
    "Product Designer": "Design products, user research, prototyping, strategy",
    "Graphic Designer": "Create visual designs, branding, marketing materials",
    "UX Researcher": "Conduct user research, analyze behavior, inform design",
    "Interaction Designer": "Design interactions, user flows, digital experiences",
    "Service Designer": "Design services, customer journeys, touchpoints",
    "Illustration & Animation": "Create illustrations, animations, visual storytelling",
    "Web Designer": "Design websites, visual design, user experience",
    "Industrial Designer": "Design physical products, ergonomics, manufacturing",
    
    # Product & Strategy (36-45)
    "Product Manager": "Define product strategy, roadmap, work with teams",
    "Product Owner": "Manage backlog, prioritize features, represent stakeholders",
    "Strategic Planner": "Develop business strategies, market analysis, planning",
    "Management Consultant": "Advise companies, solve business problems, strategy",
    "Innovation Manager": "Drive innovation, manage new initiatives, R&D",
    "Operations Manager": "Manage operations, teams, efficiency, planning",
    "Programme Manager": "Manage large programmes, stakeholders, delivery",
    "Venture Capitalist": "Evaluate investments, support startups, portfolio management",
    "Entrepreneur": "Create businesses, innovate, take risk, leadership",
    "Chief Technology Officer": "Technology strategy, innovation, leadership",
    
    # Leadership & Management (46-55)
    "Engineering Manager": "Lead engineering teams, career development, strategy",
    "Technical Lead": "Lead technical direction, mentor engineers, architecture",
    "Director of Engineering": "Oversee engineering organization, strategy, hiring",
    "Chief Executive Officer": "Lead organization, vision, strategy, Board accountability",
    "Chief Financial Officer": "Manage finances, strategy, reporting, investors",
    "Chief Product Officer": "Lead product organization, strategy, vision",
    "Head of Marketing": "Marketing strategy, campaigns, brand, team leadership",
    "Sales Manager": "Lead sales team, targets, client relationships, strategy",
    "HR Manager": "People management, hiring, culture, development",
    "Project Manager": "Plan projects, manage teams, timelines, stakeholders",
    
    # Marketing & Communications (56-65)
    "Marketing Manager": "Plan campaigns, content, analytics, strategy",
    "Content Strategist": "Plan content, strategy, analytics, storytelling",
    "Digital Marketer": "Lead digital campaigns, SEO, social, analytics",
    "Brand Manager": "Manage brand, messaging, positioning, strategy",
    "Product Marketing Manager": "Market products, positioning, messaging, launch",
    "Communications Manager": "Internal/external communications, messaging, PR",
    "Social Media Manager": "Manage social presence, content, community engagement",
    "SEO Specialist": "Optimize search, keywords, analytics, strategy",
    "Email Marketing Specialist": "Plan email campaigns, analytics, automation",
    "Copywriter": "Write marketing copy, communications, brand voice",
    
    # Sales & Business Development (66-72)
    "Enterprise Sales Manager": "Manage enterprise accounts, relationships, targets",
    "Sales Representative": "Sell products/services, manage accounts, achieve targets",
    "Business Development Manager": "Build partnerships, identify opportunities, strategy",
    "Account Manager": "Manage client relationships, retention, growth",
    "Sales Manager": "Lead sales team, targets, hiring, strategy",
    "Channel Manager": "Manage partner channels, relationships, growth",
    "Procurement Manager": "Manage vendor relationships, buying, negotiations",
    
    # Finance & Accounting (73-80)
    "Accountant": "Manage financial records, reporting, compliance, analysis",
    "Financial Controller": "Financial planning, reporting, compliance, teams",
    "Investment Banker": "M&A, capital raising, financial advisory",
    "Treasurer": "Manage cash, funding, financial risks, strategy",
    "Tax Consultant": "Tax planning, compliance, strategy, advisory",
    "Auditor": "Audit financial statements, compliance, risk",
    "Cost Analyst": "Analyze costs, budgeting, optimization, reporting",
    "Credit Analyst": "Evaluate creditworthiness, risk assessment, lending",
    
    # Science & Research (81-85)
    "Research Scientist": "Conduct research, publish papers, advance knowledge",
    "Biotechnologist": "Apply biology to create products, research, development",
    "Chemist": "Conduct chemical research, product development, analysis",
    "Physicist": "Conduct physics research, theory, experiments",
    "Environmental Scientist": "Research environment, sustainability, impact",
    
    # Education & Training (86-90)
    "University Professor": "Teach, research, publish, guide students",
    "Teacher": "Teach students, curriculum design, assessment",
    "Corporate Trainer": "Design training, deliver workshops, build skills",
    "Instructional Designer": "Design learning experiences, curriculum, content",
    "Technical Writer": "Write documentation, guides, user materials",
}


def create_career_vectors():
    """
    Create 90 career vectors with thoughtful dimension assignments.
    
    Vector dimensions (0-39):
    [0-19]: Scale questions (Q1-Q20)
        Q1-Q5 (0-4): Cognitive & Problem Solving
        Q6-Q10 (5-9): Creativity & Innovation
        Q11-Q15 (10-14): Communication & Leadership
        Q16-Q20 (15-19): Academic & Technical
    
    [20-39]: Choice questions one-hot encoded
        Q21 (20-23): Work Environment
        Q22 (24-27): Problem Type
        Q23 (28-31): Career Values
        Q24 (32-35): Work Style
        Q25 (36-39): Success Measure
    """
    
    vectors = {}
    
    # Software Engineer - HIGH cognitive/academic, MEDIUM creativity
    vectors["Software Engineer"] = np.array([
        8, 9, 8, 7, 9,  # Q1-5: High cognitive
        5, 4, 6, 7, 5,  # Q6-10: Medium creativity
        4, 3, 4, 3, 3,  # Q11-15: Low communication
        8, 6, 9, 9, 8,  # Q16-20: High academic
        0, 0, 1, 0,  # Q21: Independent (C)
        1, 0, 0, 0,  # Q22: Technical (A)
        0, 0, 1, 0,  # Q23: Learning (C)
        1, 0, 0, 0,  # Q24: Hands-on (A)
        0, 1, 0, 0   # Q25: Mastery (B)
    ]) / 10.0
    
    # Machine Learning Engineer - VERY HIGH cognitive/academic, MEDIUM-HIGH creativity
    vectors["Machine Learning Engineer"] = np.array([
        9, 10, 9, 8, 8,  # Q1-5: Very high cognitive
        6, 4, 7, 8, 6,  # Q6-10: Medium-high creativity
        4, 3, 3, 3, 2,  # Q11-15: Low communication
        9, 8, 9, 10, 9,  # Q16-20: Very high academic
        0, 0, 0, 1,  # Q21: Structured (D)
        1, 0, 0, 0,  # Q22: Technical (A)
        0, 0, 1, 0,  # Q23: Learning (C)
        1, 0, 0, 0,  # Q24: Hands-on (A)
        0, 0, 1, 0   # Q25: Thought leadership (D)
    ]) / 10.0
    
    # Data Scientist - HIGH cognitive/academic, MEDIUM creativity
    vectors["Data Scientist"] = np.array([
        8, 9, 8, 7, 7,  # Q1-5: High cognitive
        5, 4, 6, 7, 5,  # Q6-10: Medium creativity
        3, 3, 3, 3, 3,  # Q11-15: Low communication
        9, 7, 8, 8, 8,  # Q16-20: High academic
        0, 0, 1, 0,  # Q21: Independent (C)
        1, 0, 0, 0,  # Q22: Technical (A)
        0, 0, 1, 0,  # Q23: Learning (C)
        0, 1, 0, 0,  # Q24: Analysis (B)
        0, 0, 1, 0   # Q25: Results (A)
    ]) / 10.0
    
    # UX Designer - MEDIUM cognitive, HIGH creativity, HIGH communication
    vectors["UX Designer"] = np.array([
        6, 6, 6, 7, 5,  # Q1-5: Medium cognitive
        9, 9, 9, 8, 9,  # Q6-10: Very high creativity
        8, 6, 7, 6, 5,  # Q11-15: High communication
        5, 4, 4, 6, 7,  # Q16-20: Medium-low academic
        0, 1, 0, 0,  # Q21: Collaborative (B)
        0, 0, 1, 0,  # Q22: Human problems (B)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 0, 0, 1,  # Q24: Creative (D)
        0, 0, 0, 1   # Q25: Innovation (D)
    ]) / 10.0
    
    # Product Manager - MEDIUM-HIGH cognitive, MEDIUM-HIGH communication, HIGH leadership
    vectors["Product Manager"] = np.array([
        7, 7, 7, 8, 6,  # Q1-5: Medium-high cognitive
        6, 5, 8, 7, 7,  # Q6-10: Medium-high creativity
        8, 7, 7, 8, 8,  # Q11-15: High communication/leadership
        6, 5, 5, 6, 8,  # Q16-20: Medium academic
        1, 0, 0, 0,  # Q21: Collaborative (B)
        0, 0, 1, 0,  # Q22: Strategic (C)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 1, 0, 0,  # Q24: Analysis (B)
        0, 0, 0, 1   # Q25: Thought leadership (D)
    ]) / 10.0
    
    # Sales Manager - LOW-MEDIUM cognitive, HIGH communication, HIGH leadership
    vectors["Sales Manager"] = np.array([
        5, 4, 5, 5, 4,  # Q1-5: Low cognitive
        5, 4, 7, 6, 6,  # Q6-10: Medium creativity
        9, 8, 9, 9, 9,  # Q11-15: Very high communication/leadership
        4, 3, 3, 5, 7,  # Q16-20: Low-medium academic
        1, 0, 0, 0,  # Q21: Fast-paced (A)
        0, 0, 1, 0,  # Q22: Human problems (B)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 0, 1, 0,  # Q24: Relationship building (C)
        1, 0, 0, 0   # Q25: Results (A)
    ]) / 10.0
    
    # Frontend Developer - MEDIUM-HIGH cognitive, MEDIUM-HIGH creativity, MEDIUM-LOW communication
    vectors["Frontend Developer"] = np.array([
        7, 6, 6, 6, 7,  # Q1-5: Medium-high cognitive
        8, 8, 7, 8, 7,  # Q6-10: High creativity
        4, 3, 5, 4, 3,  # Q11-15: Low-medium communication
        7, 4, 8, 8, 7,  # Q16-20: Medium-high academic
        0, 0, 1, 0,  # Q21: Independent (C)
        1, 0, 0, 0,  # Q22: Technical (A)
        0, 0, 1, 0,  # Q23: Learning (C)
        1, 0, 0, 0,  # Q24: Hands-on (A)
        1, 0, 0, 0   # Q25: Results (A)
    ]) / 10.0
    
    # DevOps Engineer - HIGH cognitive, HIGH academic, LOW-MEDIUM creativity, LOW communication
    vectors["DevOps Engineer"] = np.array([
        8, 8, 8, 7, 9,  # Q1-5: High cognitive
        4, 3, 5, 6, 5,  # Q6-10: Low-medium creativity
        3, 2, 3, 3, 2,  # Q11-15: Low communication
        8, 5, 8, 9, 8,  # Q16-20: High academic
        0, 0, 0, 1,  # Q21: Structured (D)
        1, 0, 0, 0,  # Q22: Technical (A)
        1, 0, 0, 0,  # Q23: Stability (B)
        1, 0, 0, 0,  # Q24: Hands-on (A)
        1, 0, 0, 0   # Q25: Results (A)
    ]) / 10.0
    
    # Cloud Architect - HIGH cognitive, HIGH academic, MEDIUM creativity, MEDIUM communication
    vectors["Cloud Architect"] = np.array([
        8, 8, 8, 8, 8,  # Q1-5: High cognitive
        5, 4, 6, 7, 6,  # Q6-10: Medium creativity
        5, 5, 5, 5, 6,  # Q11-15: Medium communication
        8, 6, 8, 9, 8,  # Q16-20: High academic
        0, 0, 1, 0,  # Q21: Independent (C)
        1, 0, 0, 0,  # Q22: Technical (A)
        0, 0, 1, 0,  # Q23: Learning (C)
        0, 1, 0, 0,  # Q24: Analysis (B)
        0, 1, 0, 0   # Q25: Mastery (B)
    ]) / 10.0
    
    # Business Analyst - MEDIUM-HIGH cognitive, MEDIUM communication, MEDIUM academic
    vectors["Business Analyst"] = np.array([
        7, 7, 7, 7, 6,  # Q1-5: Medium-high cognitive
        5, 4, 6, 6, 6,  # Q6-10: Medium creativity
        6, 5, 6, 7, 6,  # Q11-15: Medium communication
        6, 5, 6, 6, 7,  # Q16-20: Medium academic
        1, 0, 0, 0,  # Q21: Collaborative (B)
        0, 0, 1, 0,  # Q22: Strategic (C)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 1, 0, 0,  # Q24: Analysis (B)
        0, 0, 1, 0   # Q25: Results (A)
    ]) / 10.0
    
    # Graphic Designer - MEDIUM cognitive, VERY HIGH creativity, MEDIUM communication
    vectors["Graphic Designer"] = np.array([
        5, 4, 5, 5, 4,  # Q1-5: Medium-low cognitive
        10, 9, 9, 9, 9,  # Q6-10: Very high creativity
        6, 5, 6, 5, 4,  # Q11-15: Medium communication
        4, 3, 3, 5, 6,  # Q16-20: Low-medium academic
        1, 0, 0, 0,  # Q21: Collaborative (B)
        0, 0, 0, 1,  # Q22: Creative (D)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 0, 0, 1,  # Q24: Creative (D)
        0, 0, 0, 1   # Q25: Innovation (D)
    ]) / 10.0
    
    # Marketing Manager - LOW-MEDIUM cognitive, HIGH creativity, HIGH communication
    vectors["Marketing Manager"] = np.array([
        5, 5, 5, 6, 4,  # Q1-5: Low-medium cognitive
        8, 7, 8, 7, 7,  # Q6-10: High creativity
        8, 7, 8, 7, 7,  # Q11-15: High communication
        5, 4, 4, 5, 7,  # Q16-20: Low-medium academic
        1, 0, 0, 0,  # Q21: Collaborative (B)
        0, 0, 1, 0,  # Q22: Human problems (B)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 0, 0, 1,  # Q24: Creative (D)
        0, 0, 0, 1   # Q25: Innovation (D)
    ]) / 10.0
    
    # Financial Analyst - HIGH cognitive, HIGH academic, MEDIUM communication
    vectors["Financial Analyst"] = np.array([
        8, 9, 8, 7, 7,  # Q1-5: High cognitive
        4, 3, 5, 6, 4,  # Q6-10: Low-medium creativity
        5, 4, 5, 6, 5,  # Q11-15: Medium communication
        9, 6, 6, 7, 8,  # Q16-20: High academic
        0, 0, 1, 0,  # Q21: Independent (C)
        0, 0, 1, 0,  # Q22: Strategic (C)
        1, 0, 0, 0,  # Q23: Stability (B)
        0, 1, 0, 0,  # Q24: Analysis (B)
        1, 0, 0, 0   # Q25: Results (A)
    ]) / 10.0
    
    # Accountant - MEDIUM cognitive, HIGH academic, LOW communication
    vectors["Accountant"] = np.array([
        6, 7, 6, 6, 6,  # Q1-5: Medium cognitive
        3, 2, 3, 4, 3,  # Q6-10: Low creativity
        3, 2, 3, 3, 2,  # Q11-15: Low communication
        8, 4, 5, 7, 7,  # Q16-20: High academic
        0, 0, 0, 1,  # Q21: Structured (D)
        1, 0, 0, 0,  # Q22: Technical (A)
        1, 0, 0, 0,  # Q23: Stability (B)
        0, 1, 0, 0,  # Q24: Analysis (B)
        1, 0, 0, 0   # Q25: Results (A)
    ]) / 10.0
    
    # HR Manager - MEDIUM cognitive, LOW-MEDIUM academic, HIGH communication, HIGH leadership
    vectors["HR Manager"] = np.array([
        6, 5, 5, 5, 5,  # Q1-5: Medium cognitive
        6, 5, 7, 6, 6,  # Q6-10: Medium creativity
        9, 9, 8, 8, 9,  # Q11-15: Very high communication/leadership
        4, 3, 3, 4, 7,  # Q16-20: Low-medium academic
        1, 0, 0, 0,  # Q21: Collaborative (B)
        0, 1, 0, 0,  # Q22: Human problems (B)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 0, 1, 0,  # Q24: Relationship building (C)
        0, 0, 1, 0   # Q25: Team satisfaction (C)
    ]) / 10.0
    
    # Engineering Manager - HIGH cognitive, HIGH academic, MEDIUM-HIGH communication, HIGH leadership
    vectors["Engineering Manager"] = np.array([
        8, 8, 7, 7, 7,  # Q1-5: High cognitive
        5, 4, 6, 6, 5,  # Q6-10: Medium creativity
        7, 8, 6, 7, 8,  # Q11-15: Medium-high communication/leadership
        8, 5, 8, 8, 8,  # Q16-20: High academic
        1, 0, 0, 0,  # Q21: Collaborative (B)
        1, 0, 0, 0,  # Q22: Technical (A)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 0, 0, 1,  # Q24: Strategic (ignored, use B for analysis)
        0, 0, 1, 0   # Q25: Team satisfaction (C)
    ]) / 10.0
    
    # Entrepreneur - MEDIUM-HIGH cognitive, HIGH creativity, HIGH communication, VERY HIGH leadership
    vectors["Entrepreneur"] = np.array([
        7, 6, 7, 8, 6,  # Q1-5: Medium-high cognitive
        9, 8, 9, 8, 9,  # Q6-10: Very high creativity
        8, 7, 7, 8, 9,  # Q11-15: High communication/leadership
        5, 4, 5, 6, 8,  # Q16-20: Low-medium academic
        1, 0, 0, 0,  # Q21: Fast-paced (A)
        0, 0, 1, 0,  # Q22: Strategic (C)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 0, 0, 1,  # Q24: Creative (D)
        0, 0, 0, 1   # Q25: Innovation (D)
    ]) / 10.0
    
    # Teacher - MEDIUM cognitive, MEDIUM-HIGH communication, MEDIUM-LOW academic
    vectors["Teacher"] = np.array([
        6, 5, 5, 5, 4,  # Q1-5: Medium cognitive
        6, 5, 7, 6, 6,  # Q6-10: Medium creativity
        9, 9, 8, 6, 6,  # Q11-15: High communication
        5, 6, 4, 5, 9,  # Q16-20: Medium academic/learning
        1, 0, 0, 0,  # Q21: Collaborative (B)
        0, 1, 0, 0,  # Q22: Human problems (B)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 0, 1, 0,  # Q24: Teaching/guiding (C)
        0, 0, 1, 0   # Q25: Team satisfaction (C)
    ]) / 10.0
    
    # Project Manager - MEDIUM-HIGH cognitive, MEDIUM communication, HIGH leadership
    vectors["Project Manager"] = np.array([
        7, 6, 7, 7, 6,  # Q1-5: Medium-high cognitive
        5, 4, 6, 6, 5,  # Q6-10: Medium creativity
        7, 7, 7, 7, 8,  # Q11-15: High communication/leadership
        5, 4, 4, 5, 7,  # Q16-20: Low-medium academic
        1, 0, 0, 0,  # Q21: Collaborative (B)
        0, 0, 1, 0,  # Q22: Strategic (C)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 1, 0, 0,  # Q24: Analysis (B)
        1, 0, 0, 0   # Q25: Results (A)
    ]) / 10.0
    
    # Consultant - HIGH cognitive, HIGH communication, MEDIUM academic, MEDIUM-HIGH creativity
    vectors["Management Consultant"] = np.array([
        8, 8, 8, 8, 7,  # Q1-5: High cognitive
        6, 5, 7, 7, 6,  # Q6-10: Medium-high creativity
        8, 7, 8, 8, 8,  # Q11-15: High communication/leadership
        6, 5, 5, 6, 8,  # Q16-20: Medium academic
        1, 0, 0, 0,  # Q21: Collaborative (B)
        0, 0, 1, 0,  # Q22: Strategic (C)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 1, 0, 0,  # Q24: Analysis (B)
        0, 0, 0, 1   # Q25: Innovation (D)
    ]) / 10.0
    
    # Content Strategist - LOW-MEDIUM cognitive, VERY HIGH creativity, HIGH communication
    vectors["Content Strategist"] = np.array([
        5, 5, 5, 6, 4,  # Q1-5: Low-medium cognitive
        9, 8, 9, 8, 8,  # Q6-10: Very high creativity
        8, 6, 8, 6, 5,  # Q11-15: High communication
        4, 3, 3, 5, 8,  # Q16-20: Low-medium academic
        1, 0, 0, 0,  # Q21: Collaborative (B)
        0, 1, 0, 0,  # Q22: Human problems (B)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 0, 0, 1,  # Q24: Creative (D)
        0, 0, 0, 1   # Q25: Innovation (D)
    ]) / 10.0
    
    # Security Engineer - HIGH cognitive, HIGH academic, MEDIUM-LOW creativity, MEDIUM-LOW communication
    vectors["Security Engineer"] = np.array([
        9, 9, 8, 7, 8,  # Q1-5: High cognitive
        4, 3, 5, 6, 4,  # Q6-10: Medium creativity
        3, 3, 3, 4, 3,  # Q11-15: Low-medium communication
        8, 6, 8, 8, 8,  # Q16-20: High academic
        0, 0, 0, 1,  # Q21: Structured (D)
        1, 0, 0, 0,  # Q22: Technical (A)
        1, 0, 0, 0,  # Q23: Stability (B)
        1, 0, 0, 0,  # Q24: Hands-on (A)
        1, 0, 0, 0   # Q25: Results (A)
    ]) / 10.0
    
    # Data Engineer - HIGH cognitive, HIGH academic, MEDIUM creativity, LOW-MEDIUM communication
    vectors["Data Engineer"] = np.array([
        8, 9, 8, 7, 8,  # Q1-5: High cognitive
        5, 4, 6, 7, 5,  # Q6-10: Medium creativity
        3, 2, 3, 3, 2,  # Q11-15: Low communication
        8, 5, 8, 8, 8,  # Q16-20: High academic
        0, 0, 1, 0,  # Q21: Independent (C)
        1, 0, 0, 0,  # Q22: Technical (A)
        0, 0, 1, 0,  # Q23: Learning (C)
        1, 0, 0, 0,  # Q24: Hands-on (A)
        1, 0, 0, 0   # Q25: Results (A)
    ]) / 10.0
    
    # UX Researcher - MEDIUM cognitive, MEDIUM creativity, MEDIUM-HIGH communication, MEDIUM academic
    vectors["UX Researcher"] = np.array([
        6, 7, 6, 6, 6,  # Q1-5: Medium cognitive
        6, 5, 6, 6, 7,  # Q6-10: Medium creativity
        7, 6, 6, 6, 5,  # Q11-15: Medium-high communication
        6, 5, 4, 6, 8,  # Q16-20: Medium academic
        1, 0, 0, 0,  # Q21: Collaborative (B)
        0, 1, 0, 0,  # Q22: Human problems (B)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 0, 1, 0,  # Q24: Analysis (B)
        0, 0, 1, 0   # Q25: Mastery (B)
    ]) / 10.0
    
    # Product Manager (continued from above, already added)
    
    # Now add more unique careers to reach 90...
    
    # Game Developer - MEDIUM-HIGH cognitive, HIGH creativity, MEDIUM academic
    vectors["Game Developer"] = np.array([
        7, 6, 7, 6, 7,  # Q1-5: Medium-high cognitive
        9, 9, 8, 8, 9,  # Q6-10: High creativity
        4, 3, 4, 4, 3,  # Q11-15: Low-medium communication
        6, 4, 7, 7, 7,  # Q16-20: Medium academic
        0, 0, 1, 0,  # Q21: Independent (C)
        0, 0, 0, 1,  # Q22: Creative (D)
        0, 0, 1, 0,  # Q23: Learning (C)
        1, 0, 0, 0,  # Q24: Hands-on (A)
        0, 0, 0, 1   # Q25: Innovation (D)
    ]) / 10.0
    
    # Mobile App Developer - MEDIUM-HIGH cognitive, MEDIUM-HIGH creativity, MEDIUM academic
    vectors["Mobile App Developer"] = np.array([
        7, 6, 7, 6, 7,  # Q1-5: Medium-high cognitive
        7, 6, 7, 7, 6,  # Q6-10: Medium-high creativity
        4, 3, 4, 4, 3,  # Q11-15: Low-medium communication
        7, 5, 8, 8, 7,  # Q16-20: Medium-high academic
        0, 0, 1, 0,  # Q21: Independent (C)
        1, 0, 0, 0,  # Q22: Technical (A)
        0, 0, 1, 0,  # Q23: Learning (C)
        1, 0, 0, 0,  # Q24: Hands-on (A)
        1, 0, 0, 0   # Q25: Results (A)
    ]) / 10.0
    
    # AI Research Scientist - VERY HIGH cognitive, VERY HIGH academic, MEDIUM creativity, LOW communication
    vectors["AI Research Scientist"] = np.array([
        9, 10, 9, 8, 9,  # Q1-5: Very high cognitive
        6, 4, 7, 7, 6,  # Q6-10: Medium creativity
        3, 2, 3, 3, 2,  # Q11-15: Low communication
        10, 8, 8, 9, 9,  # Q16-20: Very high academic
        0, 0, 1, 0,  # Q21: Independent (C)
        1, 0, 0, 0,  # Q22: Technical (A)
        0, 0, 1, 0,  # Q23: Learning (C)
        0, 0, 0, 1,  # Q24: Creative (D)
        0, 1, 0, 0   # Q25: Knowledge/mastery (B)
    ]) / 10.0
    
    # UI Designer - MEDIUM cognitive, VERY HIGH creativity, MEDIUM-HIGH communication, MEDIUM academic
    vectors["UI Designer"] = np.array([
        5, 5, 5, 5, 4,  # Q1-5: Medium cognitive
        10, 10, 9, 9, 9,  # Q6-10: Very high creativity
        7, 5, 6, 5, 4,  # Q11-15: Medium-high communication
        5, 3, 4, 6, 6,  # Q16-20: Medium academic
        1, 0, 0, 0,  # Q21: Collaborative (B)
        0, 0, 0, 1,  # Q22: Creative (D)
        0, 1, 0, 0,  # Q23: Impact (A)
        0, 0, 0, 1,  # Q24: Creative (D)
        0, 0, 0, 1   # Q25: Innovation (D)
    ]) / 10.0
    
    # Backend Developer - HIGH cognitive, HIGH academic, MEDIUM-LOW creativity, LOW communication
    vectors["Backend Developer"] = np.array([
        8, 8, 8, 7, 8,  # Q1-5: High cognitive
        5, 3, 6, 7, 5,  # Q6-10: Medium creativity
        3, 2, 3, 3, 2,  # Q11-15: Low communication
        8, 5, 8, 8, 8,  # Q16-20: High academic
        0, 0, 1, 0,  # Q21: Independent (C)
        1, 0, 0, 0,  # Q22: Technical (A)
        0, 0, 1, 0,  # Q23: Learning (C)
        1, 0, 0, 0,  # Q24: Hands-on (A)
        1, 0, 0, 0   # Q25: Results (A)
    ]) / 10.0
    
    # Full Stack Developer - HIGH cognitive, MEDIUM-HIGH creativity, HIGH academic, LOW-MEDIUM communication
    vectors["Full Stack Developer"] = np.array([
        8, 7, 7, 7, 8,  # Q1-5: High cognitive
        7, 5, 7, 7, 6,  # Q6-10: Medium-high creativity
        4, 3, 4, 3, 3,  # Q11-15: Low communication
        8, 5, 9, 9, 8,  # Q16-20: High academic
        0, 0, 1, 0,  # Q21: Independent (C)
        1, 0, 0, 0,  # Q22: Technical (A)
        0, 0, 1, 0,  # Q23: Learning (C)
        1, 0, 0, 0,  # Q24: Hands-on (A)
        1, 0, 0, 0   # Q25: Results (A)
    ]) / 10.0
    
    # Continue with remaining 62 careers...
    # I'll generate them with diverse profiles
    
    remaining_careers = [
        # Systems Administrator
        ("Systems Administrator", np.array([
            7, 7, 7, 6, 8, 4, 3, 5, 6, 4, 4, 3, 4, 3, 3, 7, 4, 7, 8, 7,
            0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # QA Engineer
        ("QA Engineer", np.array([
            7, 7, 6, 6, 7, 4, 3, 5, 5, 4, 4, 3, 4, 3, 3, 7, 4, 7, 7, 6,
            0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0
        ]) / 10.0),
        
        # Database Administrator
        ("Database Administrator", np.array([
            7, 8, 7, 6, 7, 3, 2, 4, 5, 3, 3, 2, 3, 3, 2, 8, 4, 7, 8, 7,
            0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Technical Lead
        ("Technical Lead", np.array([
            8, 8, 8, 7, 8, 5, 4, 6, 7, 5, 6, 7, 5, 6, 7, 8, 5, 9, 9, 9,
            0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0
        ]) / 10.0),
        
        # Product Designer
        ("Product Designer", np.array([
            6, 6, 6, 6, 5, 9, 9, 9, 8, 9, 7, 6, 7, 6, 5, 5, 4, 4, 6, 7,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1
        ]) / 10.0),
        
        # Strategic Planner
        ("Strategic Planner", np.array([
            7, 7, 8, 8, 6, 6, 5, 7, 7, 6, 7, 6, 7, 7, 7, 6, 5, 5, 6, 8,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1
        ]) / 10.0),
        
        # Operations Manager
        ("Operations Manager", np.array([
            7, 6, 7, 7, 6, 5, 4, 6, 6, 5, 7, 7, 6, 7, 7, 5, 4, 4, 5, 7,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Innovation Manager
        ("Innovation Manager", np.array([
            7, 6, 7, 8, 6, 8, 7, 9, 8, 8, 7, 6, 7, 7, 7, 6, 6, 5, 6, 8,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1
        ]) / 10.0),
        
        # Venture Capitalist
        ("Venture Capitalist", np.array([
            7, 7, 8, 8, 6, 6, 4, 7, 7, 6, 8, 7, 7, 8, 8, 7, 6, 5, 7, 8,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0
        ]) / 10.0),
        
        # Chief Executive Officer
        ("Chief Executive Officer", np.array([
            8, 7, 8, 8, 7, 7, 5, 8, 8, 7, 9, 8, 8, 9, 10, 7, 6, 5, 7, 8,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0
        ]) / 10.0),
        
        # Chief Financial Officer
        ("Chief Financial Officer", np.array([
            8, 9, 8, 7, 7, 4, 3, 5, 6, 4, 7, 6, 6, 7, 8, 9, 6, 5, 6, 8,
            0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Chief Product Officer
        ("Chief Product Officer", np.array([
            8, 7, 8, 8, 7, 7, 6, 8, 8, 7, 8, 7, 7, 8, 9, 6, 5, 5, 6, 8,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1
        ]) / 10.0),
        
        # Head of Marketing
        ("Head of Marketing", np.array([
            6, 5, 6, 7, 5, 8, 6, 8, 7, 7, 9, 7, 8, 8, 8, 5, 4, 4, 5, 7,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1
        ]) / 10.0),
        
        # Director of Engineering
        ("Director of Engineering", np.array([
            8, 8, 8, 8, 8, 5, 4, 6, 7, 5, 7, 8, 6, 7, 8, 8, 6, 9, 9, 9,
            1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0
        ]) / 10.0),
        
        # Digital Marketer
        ("Digital Marketer", np.array([
            6, 6, 6, 7, 5, 7, 6, 7, 6, 6, 7, 6, 7, 6, 5, 5, 4, 5, 6, 7,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0
        ]) / 10.0),
        
        # Social Media Manager
        ("Social Media Manager", np.array([
            5, 4, 5, 5, 4, 8, 7, 8, 7, 7, 8, 6, 8, 6, 5, 4, 3, 4, 5, 7,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1
        ]) / 10.0),
        
        # Brand Manager
        ("Brand Manager", np.array([
            6, 5, 6, 7, 5, 8, 7, 8, 7, 6, 7, 6, 7, 6, 5, 5, 4, 4, 5, 7,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1
        ]) / 10.0),
        
        # Enterprise Sales Manager
        ("Enterprise Sales Manager", np.array([
            6, 5, 6, 6, 5, 5, 4, 6, 6, 5, 9, 8, 9, 9, 9, 5, 4, 4, 5, 6,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Sales Representative
        ("Sales Representative", np.array([
            5, 4, 5, 5, 4, 5, 4, 6, 5, 5, 9, 7, 9, 8, 8, 4, 3, 3, 4, 5,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Business Development Manager
        ("Business Development Manager", np.array([
            7, 6, 7, 8, 6, 6, 5, 7, 7, 6, 8, 7, 7, 8, 7, 6, 5, 5, 6, 7,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0
        ]) / 10.0),
        
        # Account Manager
        ("Account Manager", np.array([
            6, 5, 6, 6, 5, 5, 4, 6, 6, 5, 8, 7, 7, 7, 6, 5, 4, 4, 5, 6,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0
        ]) / 10.0),
        
        # Channel Manager
        ("Channel Manager", np.array([
            6, 5, 6, 7, 5, 5, 4, 6, 6, 5, 7, 6, 6, 7, 6, 5, 4, 4, 5, 6,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0
        ]) / 10.0),
        
        # Copywriter
        ("Copywriter", np.array([
            5, 4, 5, 5, 4, 9, 8, 9, 8, 8, 7, 5, 7, 5, 4, 4, 3, 3, 5, 7,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1
        ]) / 10.0),
        
        # SEO Specialist
        ("SEO Specialist", np.array([
            6, 7, 6, 6, 5, 5, 5, 6, 6, 5, 6, 5, 6, 5, 4, 5, 4, 6, 6, 6,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Email Marketing Specialist
        ("Email Marketing Specialist", np.array([
            5, 5, 5, 5, 4, 6, 5, 6, 5, 5, 6, 4, 6, 5, 4, 4, 3, 5, 5, 6,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Tax Consultant
        ("Tax Consultant", np.array([
            7, 8, 7, 6, 6, 3, 2, 4, 5, 3, 6, 5, 5, 6, 5, 8, 5, 4, 6, 7,
            0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Investment Banker
        ("Investment Banker", np.array([
            8, 8, 8, 8, 7, 4, 3, 5, 6, 4, 7, 6, 6, 8, 7, 9, 6, 5, 6, 7,
            1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Treasury Manager
        ("Treasurer", np.array([
            7, 8, 7, 7, 6, 4, 3, 5, 6, 4, 6, 5, 5, 6, 6, 8, 5, 4, 6, 7,
            0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Auditor
        ("Auditor", np.array([
            6, 7, 6, 6, 6, 3, 2, 4, 4, 3, 4, 3, 4, 4, 3, 7, 4, 4, 6, 6,
            0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Cost Analyst
        ("Cost Analyst", np.array([
            7, 8, 7, 6, 6, 4, 3, 5, 5, 4, 5, 4, 5, 5, 4, 7, 4, 6, 6, 6,
            0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Credit Analyst
        ("Credit Analyst", np.array([
            7, 8, 7, 6, 6, 4, 3, 5, 5, 4, 5, 4, 5, 5, 4, 8, 5, 5, 6, 6,
            0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Research Scientist
        ("Research Scientist", np.array([
            9, 9, 8, 8, 8, 6, 5, 7, 7, 6, 4, 3, 4, 4, 3, 9, 8, 6, 8, 9,
            0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0
        ]) / 10.0),
        
        # Biotechnologist
        ("Biotechnologist", np.array([
            8, 8, 7, 7, 7, 5, 4, 6, 6, 5, 4, 3, 4, 4, 3, 8, 8, 6, 7, 8,
            0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0
        ]) / 10.0),
        
        # Chemist
        ("Chemist", np.array([
            8, 8, 7, 7, 7, 5, 4, 6, 6, 5, 4, 3, 4, 4, 3, 8, 8, 5, 7, 8,
            0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0
        ]) / 10.0),
        
        # Physicist
        ("Physicist", np.array([
            9, 9, 8, 8, 8, 6, 5, 7, 7, 6, 4, 3, 4, 4, 3, 9, 9, 5, 8, 9,
            0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0
        ]) / 10.0),
        
        # Environmental Scientist
        ("Environmental Scientist", np.array([
            7, 7, 7, 7, 6, 6, 5, 7, 6, 6, 6, 6, 5, 5, 5, 7, 8, 5, 7, 9,
            0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1
        ]) / 10.0),
        
        # University Professor
        ("University Professor", np.array([
            7, 6, 6, 7, 5, 6, 5, 7, 6, 6, 8, 8, 7, 6, 6, 8, 8, 5, 7, 10,
            1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0
        ]) / 10.0),
        
        # Corporate Trainer
        ("Corporate Trainer", np.array([
            6, 5, 5, 5, 4, 7, 6, 7, 6, 6, 9, 9, 8, 6, 6, 5, 6, 4, 5, 9,
            1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0
        ]) / 10.0),
        
        # Instructional Designer
        ("Instructional Designer", np.array([
            6, 5, 5, 6, 5, 8, 7, 7, 7, 6, 7, 7, 6, 5, 5, 5, 6, 5, 6, 8,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1
        ]) / 10.0),
        
        # Technical Writer
        ("Technical Writer", np.array([
            5, 5, 5, 5, 4, 6, 5, 6, 6, 5, 7, 5, 6, 5, 4, 5, 4, 6, 6, 7,
            0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0
        ]) / 10.0),
        
        # Product Marketing Manager
        ("Product Marketing Manager", np.array([
            6, 6, 6, 7, 5, 7, 6, 7, 7, 6, 7, 6, 7, 6, 5, 5, 4, 5, 5, 6,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1
        ]) / 10.0),
        
        # Communications Manager
        ("Communications Manager", np.array([
            6, 5, 5, 6, 5, 7, 6, 7, 6, 6, 8, 7, 8, 6, 6, 5, 4, 4, 5, 7,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1
        ]) / 10.0),
        
        # Procurement Manager
        ("Procurement Manager", np.array([
            6, 6, 6, 7, 5, 5, 4, 6, 6, 5, 7, 6, 6, 7, 6, 5, 4, 4, 5, 6,
            0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Financial Controller
        ("Financial Controller", np.array([
            8, 9, 8, 7, 7, 4, 3, 5, 6, 4, 7, 6, 6, 7, 8, 9, 6, 5, 6, 8,
            0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Service Designer
        ("Service Designer", np.array([
            6, 6, 6, 6, 5, 9, 8, 8, 7, 8, 7, 6, 6, 6, 5, 5, 4, 4, 5, 6,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1
        ]) / 10.0),
        
        # Interaction Designer
        ("Interaction Designer", np.array([
            6, 6, 6, 6, 5, 9, 8, 8, 8, 8, 6, 5, 6, 5, 4, 5, 4, 5, 6, 6,
            1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1
        ]) / 10.0),
        
        # Illustration & Animation
        ("Illustration & Animation", np.array([
            5, 4, 4, 4, 3, 10, 10, 9, 9, 9, 5, 4, 5, 4, 3, 4, 3, 3, 4, 6,
            1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1
        ]) / 10.0),
        
        # Web Designer
        ("Web Designer", np.array([
            5, 5, 5, 5, 4, 9, 9, 8, 8, 8, 6, 5, 5, 5, 4, 5, 3, 6, 6, 6,
            1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1
        ]) / 10.0),
        
        # Industrial Designer
        ("Industrial Designer", np.array([
            6, 5, 5, 6, 5, 9, 9, 8, 8, 8, 6, 5, 5, 5, 4, 5, 4, 4, 5, 6,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1
        ]) / 10.0),
        
        # Product Owner
        ("Product Owner", np.array([
            7, 6, 7, 7, 6, 6, 5, 7, 7, 6, 7, 6, 6, 7, 7, 6, 5, 5, 6, 7,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1
        ]) / 10.0),
        
        # Market Research Analyst
        ("Market Research Analyst", np.array([
            6, 7, 6, 6, 5, 5, 4, 6, 6, 6, 6, 5, 6, 5, 4, 6, 5, 5, 6, 7,
            1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Risk Analyst
        ("Risk Analyst", np.array([
            7, 8, 7, 6, 6, 4, 3, 5, 5, 4, 5, 4, 5, 5, 4, 7, 4, 6, 6, 6,
            0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Operations Analyst
        ("Operations Analyst", np.array([
            7, 7, 7, 6, 6, 4, 3, 5, 5, 4, 5, 4, 5, 5, 4, 6, 4, 6, 6, 6,
            0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Analytics Engineer
        ("Analytics Engineer", np.array([
            7, 8, 7, 7, 6, 5, 4, 6, 7, 5, 4, 3, 4, 3, 3, 7, 5, 7, 7, 7,
            0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0
        ]) / 10.0),
        
        # Programme Manager
        ("Programme Manager", np.array([
            7, 6, 7, 7, 6, 5, 4, 6, 6, 5, 7, 7, 6, 7, 7, 5, 4, 4, 5, 7,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0
        ]) / 10.0),
    ]
    
    for career_name, career_vector in remaining_careers:
        vectors[career_name] = career_vector
    
    return vectors


def _extend_career_vectors(career_vectors_40d):
    """
    Extend 40-dimensional career vectors to 50 dimensions.
    
    NEW DIMENSIONS (10):
    - [40-47]: Interest Profile (Q26-Q33) 
      Q26: Technology, Q27: Business, Q28: Creative, Q29: Social
      Q30: Analytical, Q31: Product/Strategy, Q32: Education, Q33: Operations
    
    - [48-49]: Work Style (Q34-Q35)
      Q34: Autonomy (1=independent, 10=structured) 
      Q35: Risk (1=stable, 10=risk-taking)
    
    This function maps known career traits to the new dimensions.
    Each dimension value is normalized to 0-1 (value/10 equivalent).
    
    SAFETY: Only APPENDS new dimensions, never modifies original 40.
    """
    # Mapping of careers to their interest/work style profiles
    # Format: career_name -> (tech, business, creative, social, analytical, product, education, operations, autonomy, risk)
    # Values are 0-10 then normalized to 0-1
    
    CAREER_PROFILES = {
        # Tech careers - HIGH tech interest
        "Software Engineer": (9, 4, 5, 2, 7, 8, 3, 6, 9, 6),
        "Machine Learning Engineer": (10, 3, 4, 2, 10, 7, 2, 5, 8, 7),
        "Data Scientist": (9, 5, 4, 3, 10, 7, 3, 7, 7, 6),
        "DevOps Engineer": (9, 5, 3, 2, 8, 6, 2, 9, 8, 5),
        "Cloud Architect": (9, 6, 3, 2, 7, 9, 2, 8, 8, 6),
        "Frontend Developer": (9, 4, 8, 2, 6, 8, 3, 5, 8, 6),
        "Backend Developer": (9, 4, 4, 2, 8, 7, 3, 6, 8, 5),
        "Full Stack Developer": (9, 4, 5, 2, 7, 8, 3, 5, 8, 6),
        "Database Administrator": (8, 4, 2, 2, 9, 6, 2, 9, 7, 4),
        "Systems Administrator": (8, 4, 2, 2, 7, 5, 3, 9, 7, 4),
        "Security Engineer": (10, 5, 2, 2, 8, 7, 3, 8, 7, 5),
        "QA Engineer": (8, 5, 3, 2, 8, 6, 4, 7, 6, 5),
        "Game Developer": (9, 3, 9, 3, 6, 7, 2, 4, 7, 7),
        "Mobile App Developer": (9, 4, 6, 2, 7, 8, 3, 5, 8, 6),
        "AI Research Scientist": (10, 3, 4, 2, 10, 6, 4, 4, 9, 7),
        "IT Support Specialist": (7, 4, 2, 4, 5, 4, 5, 7, 5, 3),
        "Network Engineer": (8, 4, 2, 2, 7, 5, 3, 9, 7, 4),
        "Web Developer": (9, 4, 7, 2, 6, 8, 3, 5, 8, 6),
        "Systems Architect": (8, 6, 2, 2, 8, 8, 2, 8, 8, 6),
        "Computer Vision Engineer": (10, 4, 5, 2, 9, 7, 3, 5, 8, 6),
        
        # Data & Analytics - ANALYTICAL + business
        "Business Analyst": (5, 9, 4, 3, 8, 8, 4, 7, 7, 5),
        "Analytics Engineer": (7, 6, 3, 2, 9, 7, 3, 8, 7, 5),
        "Data Engineer": (8, 5, 3, 2, 9, 7, 3, 8, 7, 5),
        "Business Intelligence Analyst": (7, 8, 4, 2, 9, 7, 3, 8, 6, 5),
        "Market Research Analyst": (5, 9, 4, 6, 8, 7, 3, 5, 6, 6),
        "Financial Analyst": (5, 10, 3, 2, 9, 7, 2, 7, 6, 7),
        "Risk Analyst": (5, 8, 2, 2, 10, 6, 2, 8, 6, 5),
        "Operations Analyst": (5, 8, 3, 3, 8, 7, 3, 9, 6, 4),
        "User Research Specialist": (6, 6, 6, 8, 7, 8, 5, 4, 7, 5),
        "Actuarial Scientist": (3, 8, 2, 1, 10, 5, 2, 7, 6, 8),
        
        # Creative & Design
        "UX Designer": (6, 5, 10, 5, 5, 8, 4, 3, 7, 6),
        "UI Designer": (6, 4, 10, 4, 4, 7, 3, 3, 7, 5),
        "Graphic Designer": (4, 4, 10, 4, 3, 6, 3, 3, 8, 6),
        "Product Designer": (7, 8, 9, 5, 7, 10, 4, 4, 8, 6),
        "Brand Manager": (4, 9, 10, 6, 5, 8, 3, 3, 7, 6),
        
        # Product & Strategy
        "Product Manager": (7, 10, 6, 4, 7, 10, 4, 6, 8, 7),
        "Product Marketing Manager": (6, 10, 8, 5, 6, 9, 4, 4, 7, 6),
        "Strategy Consultant": (5, 10, 5, 4, 8, 9, 3, 7, 8, 8),
        
        # Leadership & Management 
        "Engineering Manager": (8, 7, 3, 5, 7, 7, 6, 7, 9, 5),
        "Technical Lead": (9, 6, 4, 4, 8, 8, 5, 6, 9, 5),
        "Director of Engineering": (8, 7, 3, 5, 7, 7, 7, 7, 9, 6),
        
        # Business & Commerce
        "Sales Manager": (3, 10, 4, 9, 5, 7, 4, 4, 8, 7),
        "Account Manager": (2, 9, 5, 10, 4, 6, 3, 3, 7, 6),
        "Sales Representative": (2, 9, 4, 9, 3, 5, 2, 2, 8, 8),
        "Business Development Manager": (4, 10, 6, 8, 6, 8, 3, 4, 8, 8),
        "Salesforce Administrator": (7, 7, 2, 5, 7, 7, 4, 6, 6, 5),
        
        # Finance & Accounting
        "Accountant": (3, 8, 2, 3, 9, 5, 4, 8, 5, 3),
        "Financial Planner": (3, 9, 3, 6, 8, 7, 4, 6, 7, 6),
        "CPA": (3, 8, 2, 3, 9, 5, 4, 8, 5, 3),
        "Auditor": (3, 7, 2, 2, 8, 5, 3, 9, 5, 3),
        "Tax Specialist": (3, 8, 2, 2, 8, 5, 3, 9, 5, 3),
        
        # HR & Admin
        "HR Manager": (2, 6, 5, 10, 6, 7, 8, 6, 7, 5),
        "HR Business Partner": (2, 7, 5, 9, 6, 7, 8, 6, 8, 5),
        "Recruiter": (2, 6, 4, 10, 5, 6, 5, 3, 7, 6),
        "HR Coordinator": (2, 5, 4, 9, 5, 5, 7, 5, 6, 4),
        
        # Education & Training
        "Teacher": (3, 3, 6, 10, 5, 5, 10, 4, 6, 4),
        "Instructor": (3, 3, 6, 9, 5, 5, 10, 4, 6, 4),
        "Training Manager": (3, 5, 6, 9, 5, 6, 10, 5, 7, 5),
        "Curriculum Developer": (4, 4, 7, 9, 6, 7, 10, 4, 7, 5),
        "Instructional Designer": (5, 5, 8, 8, 6, 8, 10, 4, 7, 5),
        
        # Healthcare
        "Registered Nurse": (3, 3, 2, 10, 6, 4, 8, 7, 6, 4),
        "Healthcare Administrator": (2, 7, 3, 8, 7, 7, 7, 8, 7, 5),
        "Pharmacist": (6, 4, 2, 8, 8, 5, 7, 6, 6, 4),
        "Physical Therapist": (3, 3, 4, 10, 5, 5, 8, 6, 7, 4),
        "Clinical Psychologist": (4, 2, 5, 10, 7, 4, 9, 3, 8, 5),
        
        # Social Services & Support
        "Social Worker": (2, 2, 4, 10, 5, 4, 10, 3, 5, 3),
        "Counselor": (2, 2, 5, 10, 5, 4, 9, 2, 6, 3),
        "Community Outreach Specialist": (2, 3, 6, 10, 4, 5, 8, 4, 6, 5),
        
        # Legal
        "Lawyer": (4, 7, 3, 6, 7, 7, 5, 7, 8, 7),
        "Paralegal": (4, 6, 2, 4, 6, 6, 4, 8, 6, 4),
        "Legal Secretary": (3, 5, 2, 3, 5, 5, 3, 8, 5, 3),
        
        # Creative Professionals
        "Content Strategist": (5, 7, 9, 6, 6, 9, 4, 3, 8, 6),
        "Content Writer": (4, 6, 9, 6, 5, 7, 4, 3, 8, 5),
        "Copywriter": (3, 7, 10, 5, 4, 7, 3, 2, 8, 6),
        "Journalist": (4, 5, 8, 8, 6, 6, 4, 3, 8, 7),
        "Video Producer": (6, 5, 10, 6, 6, 8, 4, 4, 8, 6),
        "Photographer": (3, 3, 10, 4, 3, 6, 3, 2, 8, 7),
        
        # Marketing
        "Marketing Manager": (5, 10, 9, 7, 7, 9, 4, 5, 8, 6),
        "Digital Marketing Specialist": (7, 9, 9, 6, 7, 8, 3, 4, 7, 6),
        "SEO Specialist": (8, 7, 5, 2, 8, 7, 2, 4, 7, 5),
        "Social Media Manager": (6, 8, 9, 9, 5, 7, 4, 3, 7, 6),
        "Market Analyst": (5, 9, 4, 5, 9, 8, 3, 6, 6, 6),
        
        # Operations & Logistics
        "Operations Manager": (3, 8, 2, 5, 7, 8, 3, 10, 7, 5),
        "Supply Chain Manager": (4, 8, 2, 4, 8, 7, 2, 10, 6, 6),
        "Logistics Coordinator": (3, 6, 2, 3, 6, 5, 2, 9, 5, 4),
        "Project Manager": (5, 7, 4, 6, 6, 8, 4, 8, 8, 6),
        "Scrum Master": (6, 6, 3, 7, 5, 7, 5, 7, 8, 5),
        
        # Manufacturing & Production
        "Production Manager": (3, 7, 2, 4, 7, 7, 3, 10, 7, 5),
        "Manufacturing Engineer": (8, 6, 3, 2, 9, 8, 2, 9, 7, 5),
        
        # Architecture & Construction
        "Architect": (2, 6, 9, 3, 6, 9, 3, 6, 8, 6),
        "Construction Manager": (3, 7, 3, 5, 6, 8, 3, 9, 8, 6),
        
        # Energy & Utilities
        "Electrical Engineer": (8, 5, 2, 2, 8, 7, 2, 8, 7, 5),
        "Mechanical Engineer": (7, 5, 4, 2, 8, 8, 2, 8, 7, 5),
        "Civil Engineer": (6, 5, 3, 3, 8, 8, 2, 9, 7, 5),
        
        # Government & Public Service
        "Government Relations Specialist": (3, 8, 5, 8, 6, 7, 5, 7, 8, 6),
        "Public Policy Analyst": (4, 6, 4, 9, 7, 7, 5, 7, 8, 7),
        "Urban Planner": (4, 6, 6, 8, 7, 9, 4, 8, 7, 6),
        
        # Science & Research
        "Research Scientist": (3, 2, 3, 3, 10, 6, 8, 4, 9, 7),
        "Quality Assurance Manager": (5, 7, 2, 4, 8, 7, 4, 9, 7, 5),
    }
    
    extended_vectors = {}
    
    for career_name, vector_40d in career_vectors_40d.items():
        # Get the profile for this career, or use default
        if career_name in CAREER_PROFILES:
            profile = CAREER_PROFILES[career_name]
        else:
            # Default profile for unlisted careers
            # (medium across all, slightly autonomous, medium stability)
            profile = (5, 5, 5, 5, 5, 5, 5, 5, 6, 5)
        
        # Normalize profile from 0-10 to 0-1 range (divide by 10)
        extended_block = np.array(profile) / 10.0
        
        # Extend the vector: append 10 new dimensions
        extended_vector = np.concatenate([vector_40d, extended_block])
        extended_vectors[career_name] = extended_vector
    
    return extended_vectors


def get_all_careers():
    """Get dictionary of all career vectors (50-dimensional)."""
    career_vectors_40d = create_career_vectors()
    return _extend_career_vectors(career_vectors_40d)


def get_career_vector(career_name):
    """Get vector for a specific career."""
    careers = create_career_vectors()
    return careers.get(career_name)


def get_career_description(career_name):
    """Get description for a specific career."""
    return CAREER_DESCRIPTIONS.get(career_name, "No description available")
