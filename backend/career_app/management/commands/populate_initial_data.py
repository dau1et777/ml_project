"""
Django management command to populate initial data.
Usage: python manage.py populate_initial_data
"""
from django.core.management.base import BaseCommand
from career_app.signals import (
    _create_quiz_questions,
    _create_careers,
    _create_skills,
    _create_career_skills
)
from career_app.models import QuizQuestion, Career, Skill, CareerSkill


class Command(BaseCommand):
    help = 'Populate initial quiz questions, careers, and skills'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )
    
    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            CareerSkill.objects.all().delete()
            Skill.objects.all().delete()
            Career.objects.all().delete()
            QuizQuestion.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data cleared'))
        
        self.stdout.write('Creating quiz questions...')
        _create_quiz_questions()
        count = QuizQuestion.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Created {count} quiz questions'))
        
        self.stdout.write('Creating careers...')
        _create_careers()
        count = Career.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Created {count} careers'))
        
        self.stdout.write('Creating skills...')
        _create_skills()
        count = Skill.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Created {count} skills'))
        
        self.stdout.write('Creating career skill relationships...')
        _create_career_skills()
        count = CareerSkill.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Created {count} career-skill relationships'))
        
        self.stdout.write(self.style.SUCCESS('Data population completed!'))
