"""
Integration tests for the full-stack career guidance system.
Tests: ML service + database + API layer
Run: python manage.py test
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from career_app.models import Career, Skill, CareerSkill
from career_app.services import PredictionService, SkillGapService, UserService
from ml.ml_service import Preprocessor, MLService


class PreprocessorTestCase(TestCase):
    """Test the ML preprocessor."""
    
    def test_valid_answers(self):
        """Test valid answer conversion to vector."""
        answers = {i: (i % 10) + 1 for i in range(1, 36)}
        # Q21-Q25 should be letters
        for q in [21, 22, 23, 24, 25]:
            answers[q] = chr(65 + ((q - 21) % 4))
        
        is_valid, errors = Preprocessor.validate_answers(answers)
        self.assertTrue(is_valid, f"Should be valid but got errors: {errors}")
    
    def test_invalid_scale_values(self):
        """Test invalid scale values are caught."""
        answers = {i: 15 for i in range(1, 36)}  # 15 is out of range
        is_valid, errors = Preprocessor.validate_answers(answers)
        self.assertFalse(is_valid)
        self.assertTrue(len(errors) > 0)
    
    def test_vector_dimensions(self):
        """Test output vector has correct dimensions."""
        answers = {i: (i % 10) + 1 for i in range(1, 36)}
        for q in [21, 22, 23, 24, 25]:
            answers[q] = chr(65 + ((q - 21) % 4))
        
        vector, errors = Preprocessor.answers_to_vector(answers)
        self.assertEqual(len(vector), 50, "Vector should have 50 dimensions")


class PredictionServiceTestCase(TestCase):
    """Test the prediction service."""
    
    def setUp(self):
        """Create test user and careers."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123'
        )
        
        # Create test career
        self.career = Career.objects.create(
            name='Test Career',
            description='A test career',
            salary_min=50000,
            salary_max=100000,
            demand_level='high'
        )
    
    def test_prediction_success(self):
        """Test successful prediction."""
        answers = {i: (i % 10) + 1 for i in range(1, 36)}
        for q in [21, 22, 23, 24, 25]:
            answers[q] = chr(65 + ((q - 21) % 4))
        
        result = PredictionService.predict_and_save(
            user=self.user,
            answers=answers,
            save_result=True
        )
        
        self.assertTrue(result['success'])
        self.assertIn('predictions', result)
        self.assertIn('result_id', result)
    
    def test_invalid_answers_rejected(self):
        """Test that invalid answers are rejected."""
        answers = {1: 'invalid'}  # Invalid answer
        
        result = PredictionService.predict_and_save(
            user=self.user,
            answers=answers,
            save_result=False
        )
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)


class SkillGapServiceTestCase(TestCase):
    """Test the skill gap analysis service."""
    
    def setUp(self):
        """Create test user, career, and skills."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123'
        )
        
        # Create test career with skills
        self.career = Career.objects.create(
            name='Software Engineer',
            description='Write software',
            salary_min=100000,
            salary_max=200000,
            demand_level='high'
        )
        
        # Create skills
        self.skill1 = Skill.objects.create(
            name='Python',
            category='technical'
        )
        self.skill2 = Skill.objects.create(
            name='Problem Solving',
            category='soft'
        )
        
        # Link skills to career
        CareerSkill.objects.create(
            career=self.career,
            skill=self.skill1,
            proficiency_level='expert'
        )
        CareerSkill.objects.create(
            career=self.career,
            skill=self.skill2,
            proficiency_level='intermediate'
        )
    
    def test_skill_gap_analysis(self):
        """Test skill gap analysis."""
        gap_data = SkillGapService.analyze_gap(self.user, 'Software Engineer')
        
        self.assertIn('gap_analysis', gap_data)
        self.assertIn('missing', gap_data['gap_analysis'])
        # User has no skills, so all should be missing
        self.assertEqual(len(gap_data['gap_analysis']['missing']), 2)


class UserServiceTestCase(TestCase):
    """Test user management service."""
    
    def test_create_user_success(self):
        """Test successful user creation."""
        success, message, user = UserService.create_user(
            email='newuser@example.com',
            username='newuser',
            password='SecurePass123',
            first_name='John'
        )
        
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newuser@example.com')
    
    def test_create_user_duplicate_email(self):
        """Test that duplicate email is rejected."""
        # Create first user
        UserService.create_user(
            email='test@example.com',
            username='user1',
            password='pass123'
        )
        
        # Try to create second with same email
        success, message, user = UserService.create_user(
            email='test@example.com',
            username='user2',
            password='pass123'
        )
        
        self.assertFalse(success)
        self.assertIsNone(user)
    
    def test_authenticate_user_success(self):
        """Test successful authentication."""
        # Create user
        UserService.create_user(
            email='test@example.com',
            username='testuser',
            password='SecurePass123'
        )
        
        # Authenticate
        success, message, user = UserService.authenticate_user(
            email='test@example.com',
            password='SecurePass123'
        )
        
        self.assertTrue(success)
        self.assertIsNotNone(user)
    
    def test_authenticate_user_failure(self):
        """Test authentication with wrong password."""
        # Create user
        UserService.create_user(
            email='test@example.com',
            username='testuser',
            password='SecurePass123'
        )
        
        # Try wrong password
        success, message, user = UserService.authenticate_user(
            email='test@example.com',
            password='WrongPassword'
        )
        
        self.assertFalse(success)
        self.assertIsNone(user)


class APIEndpointTestCase(TestCase):
    """Test API endpoints."""
    
    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123'
        )
        self.token = Token.objects.create(user=self.user)
    
    def test_signup_endpoint(self):
        """Test signup endpoint."""
        response = self.client.post('/api/auth/signup/', {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'SecurePass123'
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('token', data)
    
    def test_login_endpoint(self):
        """Test login endpoint."""
        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'test123'
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('token', data)
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
    
    def test_info_endpoint(self):
        """Test info endpoint."""
        response = self.client.get('/api/info/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['platform'], 'Career Guidance System')
        self.assertIn('endpoints', data)


if __name__ == '__main__':
    import unittest
    unittest.main()
