#!/usr/bin/env python3
"""
KPI AI Agent - Main Application Entry Point
"""

import argparse
import sys
import os
from src.core.factory import KPIAgentFactory

def main():
    parser = argparse.ArgumentParser(description="KPI AI Agent System")
    parser.add_argument(
        "--mode", 
        choices=["dashboard", "cli", "api"], 
        default="dashboard",
        help="Run mode (default: dashboard)"
    )
    parser.add_argument(
        "--config", 
        help="Path to configuration file"
    )
    
    args = parser.parse_args()
    
    if args.mode == "dashboard":
        run_dashboard_mode()
    elif args.mode == "cli":
        run_cli_mode()
    elif args.mode == "api":
        run_api_mode()

def run_dashboard_mode():
    """Run in dashboard mode"""
    try:
        import streamlit as st
        from src.dashboard.app import main as dashboard_main
        dashboard_main()
    except ImportError:
        print("Streamlit not installed. Install with: pip install streamlit")
        sys.exit(1)

def run_cli_mode():
    """Run in CLI mode for direct interaction"""
    print("KPI AI Agent - CLI Mode")
    print("Type 'quit' to exit")
    
    agent_system = KPIAgentFactory.create_agent_system()
    
    while True:
        try:
            query = input("\n> ")
            if query.lower() in ['quit', 'exit']:
                break
            
            result = agent_system.execute_analysis(query)
            if result["success"]:
                print(result["result"])
            else:
                print(f"Error: {result['error']}")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def run_api_mode():
    """Run in API mode"""
    print("API mode not yet implemented")
    # Implementation for API server would go here

if __name__ == "__main__":
    main()