"""
Test cases for NSAKCET College Chatbot
"""

import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestNSAKCETChatbot(unittest.TestCase):
    """Test cases for the NSAKCET chatbot application"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_page_loads(self):
        """Test that the home page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'NSAKCET', response.data)
    
    def test_get_response_endpoint_exists(self):
        """Test that the get_response endpoint exists"""
        response = self.app.post('/get_response', 
                               json={'message': 'Hello'})
        self.assertEqual(response.status_code, 200)
    
    def test_get_response_returns_json(self):
        """Test that get_response returns valid JSON"""
        response = self.app.post('/get_response', 
                               json={'message': 'Hello'})
        self.assertEqual(response.content_type, 'application/json')
        
        data = json.loads(response.data)
        self.assertIn('response', data)
    
    def test_greeting_response(self):
        """Test greeting responses"""
        test_messages = ['Hi', 'Hello', 'Hey', 'Good morning']
        
        for message in test_messages:
            with self.subTest(message=message):
                response = self.app.post('/get_response', 
                                       json={'message': message})
                data = json.loads(response.data)
                
                # Should get a greeting response
                self.assertIn('response', data)
                self.assertIsInstance(data['response'], str)
                self.assertGreater(len(data['response']), 0)
    
    def test_affiliation_query(self):
        """Test affiliation-related queries"""
        test_messages = [
            'What is the affiliation?',
            'Which university is NSAKCET affiliated with?',
            'Is NSAKCET under Osmania University?'
        ]
        
        for message in test_messages:
            with self.subTest(message=message):
                response = self.app.post('/get_response', 
                                       json={'message': message})
                data = json.loads(response.data)
                
                self.assertIn('response', data)
                # Should mention Osmania University
                self.assertIn('Osmania', data['response'])
    
    def test_programs_query(self):
        """Test programs-related queries"""
        test_messages = [
            'What programs are available?',
            'Tell me about B.Tech programs',
            'What courses does NSAKCET offer?'
        ]
        
        for message in test_messages:
            with self.subTest(message=message):
                response = self.app.post('/get_response', 
                                       json={'message': message})
                data = json.loads(response.data)
                
                self.assertIn('response', data)
                # Should mention some programs
                self.assertTrue(
                    any(program in data['response'] for program in 
                        ['CSE', 'Civil', 'Mechanical', 'B.Tech', 'M.Tech'])
                )
    
    def test_fees_query(self):
        """Test fees-related queries"""
        test_messages = [
            'What are the fees?',
            'How much does B.Tech cost?',
            'Fee structure'
        ]
        
        for message in test_messages:
            with self.subTest(message=message):
                response = self.app.post('/get_response', 
                                       json={'message': message})
                data = json.loads(response.data)
                
                self.assertIn('response', data)
                # Should mention some fee information
                self.assertTrue(
                    any(fee in data['response'] for fee in 
                        ['₹', 'fee', 'Fee', 'cost', 'Cost'])
                )
    
    def test_facilities_query(self):
        """Test facilities-related queries"""
        test_messages = [
            'What facilities are available?',
            'Does the college have a library?',
            'Campus facilities'
        ]
        
        for message in test_messages:
            with self.subTest(message=message):
                response = self.app.post('/get_response', 
                                       json={'message': message})
                data = json.loads(response.data)
                
                self.assertIn('response', data)
                # Should mention some facilities
                self.assertTrue(
                    any(facility in data['response'] for facility in 
                        ['library', 'Library', 'lab', 'Lab', 'cafeteria', 'Cafeteria'])
                )
    
    def test_admission_query(self):
        """Test admission-related queries"""
        test_messages = [
            'How to get admission?',
            'What is the admission process?',
            'How to apply for B.Tech?'
        ]
        
        for message in test_messages:
            with self.subTest(message=message):
                response = self.app.post('/get_response', 
                                       json={'message': message})
                data = json.loads(response.data)
                
                self.assertIn('response', data)
                # Should mention admission process
                self.assertTrue(
                    any(term in data['response'] for term in 
                        ['EAMCET', 'admission', 'Admission', 'apply', 'Apply'])
                )
    
    def test_unknown_query(self):
        """Test response to unknown queries"""
        response = self.app.post('/get_response', 
                               json={'message': 'xyzabc123random'})
        data = json.loads(response.data)
        
        self.assertIn('response', data)
        # Should get a default response
        self.assertIn('sorry', data['response'].lower())
    
    def test_empty_message(self):
        """Test response to empty message"""
        response = self.app.post('/get_response', 
                               json={'message': ''})
        data = json.loads(response.data)
        
        self.assertIn('response', data)
        self.assertIsInstance(data['response'], str)
    
    def test_intents_json_structure(self):
        """Test that intents.json has proper structure"""
        with open('intents.json', 'r', encoding='utf-8') as f:
            intents = json.load(f)
        
        self.assertIn('intents', intents)
        self.assertIsInstance(intents['intents'], list)
        
        for intent in intents['intents']:
            self.assertIn('tag', intent)
            self.assertIn('patterns', intent)
            self.assertIn('responses', intent)
            
            self.assertIsInstance(intent['patterns'], list)
            self.assertIsInstance(intent['responses'], list)
            
            self.assertGreater(len(intent['patterns']), 0)
            self.assertGreater(len(intent['responses']), 0)

if __name__ == '__main__':
    unittest.main()
