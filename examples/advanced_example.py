"""
Advanced Example: Complex Code Development with Custom Configuration

This example shows advanced usage patterns and configuration options.
"""

import asyncio
import os
from typing import Dict, Any
from multi_agent_workflow import CodeDevelopmentWorkflow, WorkflowResult


class AdvancedWorkflowManager:
    """Advanced workflow manager with custom configuration and monitoring"""
    
    def __init__(self):
        self.results: Dict[str, WorkflowResult] = {}
        self.performance_metrics: Dict[str, Any] = {}
    
    async def run_complex_task(self, task_name: str, task_description: str) -> WorkflowResult:
        """Run a complex coding task with advanced configuration"""
        
        print(f"\n🚀 Advanced Example: {task_name}")
        print("=" * 60)
        
        # Advanced configuration
        workflow = CodeDevelopmentWorkflow(
            model="gpt-4",          # High-performance model
            temperature=0.05,       # Very low temperature for consistency
            max_rounds=15           # More rounds for complex tasks
        )
        
        try:
            # Run with timing
            result = await workflow.run(task_description, verbose=True)
            
            # Store results
            self.results[task_name] = result
            
            # Calculate metrics
            self._calculate_metrics(task_name, result)
            
            return result
            
        finally:
            await workflow.close()
    
    def _calculate_metrics(self, task_name: str, result: WorkflowResult):
        """Calculate performance metrics for the workflow"""
        
        metrics = {
            'execution_time': result.execution_time,
            'message_count': len(result.conversation_history),
            'code_length': len(result.final_code),
            'has_docstring': '"""' in result.final_code or "'''" in result.final_code,
            'has_type_hints': '->' in result.final_code,
            'has_error_handling': 'try:' in result.final_code or 'except:' in result.final_code
        }
        
        self.performance_metrics[task_name] = metrics
    
    def print_summary_report(self):
        """Print a summary report of all workflow executions"""
        
        print("\n" + "=" * 80)
        print("📊 ADVANCED WORKFLOW SUMMARY REPORT")
        print("=" * 80)
        
        for task_name, metrics in self.performance_metrics.items():
            print(f"\n📋 Task: {task_name}")
            print(f"   ⏱️  Execution Time: {metrics['execution_time']:.2f}s")
            print(f"   💬 Messages: {metrics['message_count']}")
            print(f"   📏 Code Length: {metrics['code_length']} characters")
            print(f"   📚 Has Docstring: {'✅' if metrics['has_docstring'] else '❌'}")
            print(f"   🏷️  Has Type Hints: {'✅' if metrics['has_type_hints'] else '❌'}")
            print(f"   🛡️  Error Handling: {'✅' if metrics['has_error_handling'] else '❌'}")


async def data_structure_example():
    """Advanced example: Implement a complex data structure"""
    
    task = """
    Create a Python implementation of a Binary Search Tree (BST) with the following requirements:
    
    1. A Node class with value, left, and right attributes
    2. A BST class with methods:
       - insert(value): Insert a new value
       - search(value): Search for a value, return True/False
       - delete(value): Delete a value from the tree
       - inorder_traversal(): Return list of values in sorted order
       - get_height(): Return the height of the tree
       - is_balanced(): Check if the tree is balanced
    
    3. Include comprehensive error handling
    4. Add type hints for all methods
    5. Include detailed docstrings with complexity analysis
    6. Handle edge cases (empty tree, single node, etc.)
    7. Optimize for performance
    """
    
    manager = AdvancedWorkflowManager()
    result = await manager.run_complex_task("Binary Search Tree", task)
    
    print("\n" + "=" * 60)
    print("🌳 BINARY SEARCH TREE IMPLEMENTATION:")
    print("=" * 60)
    print(result.final_code)
    
    return manager


async def api_client_example():
    """Advanced example: Create a robust API client"""
    
    task = """
    Create a robust HTTP API client class with the following features:
    
    1. Support for GET, POST, PUT, DELETE methods
    2. Automatic retry logic with exponential backoff
    3. Request/response logging
    4. Authentication handling (API key, Bearer token)
    5. Rate limiting with configurable limits
    6. Timeout handling
    7. JSON serialization/deserialization
    8. Custom exception classes for different error types
    9. Async/await support
    10. Connection pooling
    11. Request/response middleware support
    12. Comprehensive error handling and recovery
    
    Requirements:
    - Use aiohttp for async HTTP requests
    - Include type hints for all methods
    - Add comprehensive docstrings
    - Handle network errors gracefully
    - Support configuration via environment variables
    - Include usage examples in docstrings
    """
    
    manager = AdvancedWorkflowManager()
    result = await manager.run_complex_task("Robust API Client", task)
    
    print("\n" + "=" * 60)
    print("🌐 ROBUST API CLIENT IMPLEMENTATION:")
    print("=" * 60)
    print(result.final_code)
    
    return manager


async def machine_learning_example():
    """Advanced example: ML model implementation"""
    
    task = """
    Create a complete machine learning pipeline implementation with the following components:
    
    1. A DataProcessor class that:
       - Loads data from various sources (CSV, JSON, databases)
       - Handles missing values with multiple strategies
       - Performs feature scaling and normalization
       - Splits data into train/validation/test sets
       - Provides data visualization methods
    
    2. A SimpleLinearRegression class that:
       - Implements linear regression from scratch (no sklearn)
       - Uses gradient descent optimization
       - Includes regularization (L1, L2)
       - Provides model evaluation metrics
       - Supports feature importance analysis
       - Includes prediction confidence intervals
    
    3. A ModelEvaluator class that:
       - Calculates various regression metrics (MSE, MAE, R²)
       - Performs cross-validation
       - Generates learning curves
       - Provides model comparison utilities
    
    Requirements:
    - Use only numpy and pandas (no sklearn)
    - Include comprehensive type hints
    - Add detailed mathematical explanations in docstrings
    - Implement proper error handling
    - Optimize for numerical stability
    - Include usage examples and test cases
    """
    
    manager = AdvancedWorkflowManager()
    result = await manager.run_complex_task("ML Pipeline", task)
    
    print("\n" + "=" * 60)
    print("🤖 MACHINE LEARNING PIPELINE IMPLEMENTATION:")
    print("=" * 60)
    print(result.final_code)
    
    return manager


async def run_all_advanced_examples():
    """Run all advanced examples and generate comprehensive report"""
    
    print("🎯 Starting Advanced Examples Suite")
    print("This will demonstrate complex code generation across multiple domains")
    print("=" * 80)
    
    managers = []
    
    try:
        # Run all examples
        print("\n1️⃣ Running Data Structure Example...")
        manager1 = await data_structure_example()
        managers.append(manager1)
        
        print("\n2️⃣ Running API Client Example...")
        manager2 = await api_client_example()
        managers.append(manager2)
        
        print("\n3️⃣ Running Machine Learning Example...")
        manager3 = await machine_learning_example()
        managers.append(manager3)
        
        # Generate combined report
        print("\n" + "=" * 80)
        print("📈 COMBINED PERFORMANCE ANALYSIS")
        print("=" * 80)
        
        total_time = 0
        total_messages = 0
        total_code_length = 0
        
        for i, manager in enumerate(managers, 1):
            print(f"\n📊 Example {i} Results:")
            manager.print_summary_report()
            
            # Aggregate metrics
            for metrics in manager.performance_metrics.values():
                total_time += metrics['execution_time']
                total_messages += metrics['message_count']
                total_code_length += metrics['code_length']
        
        print("\n" + "=" * 80)
        print("🏆 OVERALL STATISTICS")
        print("=" * 80)
        print(f"📊 Total Execution Time: {total_time:.2f} seconds")
        print(f"💬 Total Messages Exchanged: {total_messages}")
        print(f"📏 Total Code Generated: {total_code_length:,} characters")
        print(f"⚡ Average Time per Task: {total_time/3:.2f} seconds")
        print(f"💡 Average Messages per Task: {total_messages/3:.1f}")
        
    except Exception as e:
        print(f"❌ Error during advanced examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Please set your OPENAI_API_KEY environment variable")
        print("   You can do this by:")
        print("   1. Creating a .env file with OPENAI_API_KEY=your_key")
        print("   2. Or: export OPENAI_API_KEY=your_key")
        exit(1)
    
    # Run all advanced examples
    asyncio.run(run_all_advanced_examples())
