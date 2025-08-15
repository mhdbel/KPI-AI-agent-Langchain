"""Integration tests for KPI AI Agent"""
import unittest
from src.core.factory import KPIAgentFactory

class TestKPIAgentIntegration(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent_system = KPIAgentFactory.create_agent_system()
    
    def test_system_initialization(self):
        """Test that the system initializes correctly"""
        status = self.agent_system.get_system_status()
        self.assertTrue(status["agent_initialized"])
        self.assertGreater(status["tools_count"], 0)
    
    def test_simple_query(self):
        """Test simple query execution"""
        result = self.agent_system.execute_analysis("Hello, what can you do?")
        self.assertTrue(result["success"])
        self.assertIn("KPI", result["result"])

if __name__ == '__main__':
    unittest.main()