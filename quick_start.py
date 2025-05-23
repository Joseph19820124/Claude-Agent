#!/usr/bin/env python3
"""
Quick Start Script for Claude-Agent
This script demonstrates the basic usage of the multi-agent system.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from multi_agent_workflow import CodeDevelopmentWorkflow
except ImportError:
    print("❌ Error: Could not import CodeDevelopmentWorkflow")
    print("   Make sure you have installed the required dependencies:")
    print("   pip install -U \"autogen-agentchat\" \"autogen-ext[openai]\"")
    sys.exit(1)


def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print(f"❌ Python 3.9+ required, found {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]}")
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OpenAI API key not found")
        print("   Please set your API key:")
        print("   export OPENAI_API_KEY='your_key_here'")
        print("   Or create a .env file with: OPENAI_API_KEY=your_key_here")
        return False
    print("✅ OpenAI API key found")
    
    # Check required packages
    try:
        import autogen_agentchat
        import autogen_ext.models.openai
        print("✅ AutoGen packages installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("   Install with: pip install -U \"autogen-agentchat\" \"autogen-ext[openai]\"")
        return False
    
    return True


async def demo_simple_function():
    """Demo: Simple function generation"""
    print("\n🚀 Demo 1: Simple Function Generation")
    print("=" * 50)
    
    workflow = CodeDevelopmentWorkflow(
        model="gpt-4o-mini",  # Cost-effective model
        temperature=0.1,
        max_rounds=6
    )
    
    task = """
    Create a Python function called 'calculate_average' that:
    1. Takes a list of numbers as input
    2. Returns the average (mean) of those numbers
    3. Handles empty lists gracefully
    4. Includes proper error handling and type hints
    """
    
    try:
        result = await workflow.run(task, verbose=True)
        
        print("\n" + "=" * 50)
        print("📋 RESULT SUMMARY:")
        print("=" * 50)
        print(f"⏱️  Execution Time: {result.execution_time:.2f} seconds")
        print(f"💬 Messages Exchanged: {len(result.conversation_history)}")
        print(f"📏 Code Length: {len(result.final_code)} characters")
        
        print("\n🎯 FINAL CODE:")
        print("-" * 30)
        print(result.final_code)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        return False
    
    finally:
        await workflow.close()


async def demo_complex_class():
    """Demo: Complex class generation"""
    print("\n🚀 Demo 2: Complex Class Generation")
    print("=" * 50)
    
    workflow = CodeDevelopmentWorkflow(
        model="gpt-4o-mini",
        temperature=0.1,
        max_rounds=8
    )
    
    task = """
    Create a Python class called 'TaskManager' that:
    1. Manages a list of tasks with priorities
    2. Can add, remove, and mark tasks as complete
    3. Can filter tasks by status and priority
    4. Includes proper initialization and string representation
    5. Uses type hints and comprehensive docstrings
    6. Handles edge cases with appropriate exceptions
    """
    
    try:
        result = await workflow.run(task, verbose=False)  # Silent mode for demo
        
        print(f"✅ Class generation completed in {result.execution_time:.2f} seconds")
        print(f"📊 Generated {len(result.final_code)} characters of code")
        
        # Show just the class definition (first few lines)
        lines = result.final_code.split('\n')
        preview_lines = []
        for line in lines[:15]:  # Show first 15 lines
            preview_lines.append(line)
        
        print("\n📝 CODE PREVIEW (first 15 lines):")
        print("-" * 40)
        print('\n'.join(preview_lines))
        if len(lines) > 15:
            print(f"... and {len(lines) - 15} more lines")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        return False
    
    finally:
        await workflow.close()


async def demo_performance_comparison():
    """Demo: Compare different models"""
    print("\n🚀 Demo 3: Model Performance Comparison")
    print("=" * 50)
    
    task = "Create a function that checks if a string is a palindrome"
    
    models = [
        ("gpt-4o-mini", "Fast & Cost-effective"),
        ("gpt-4o", "Balanced Performance"),
    ]
    
    results = []
    
    for model, description in models:
        print(f"\n🧪 Testing {model} ({description})...")
        
        workflow = CodeDevelopmentWorkflow(
            model=model,
            temperature=0.1,
            max_rounds=5
        )
        
        try:
            result = await workflow.run(task, verbose=False)
            results.append({
                'model': model,
                'description': description,
                'time': result.execution_time,
                'code_length': len(result.final_code),
                'messages': len(result.conversation_history)
            })
            print(f"   ✅ Completed in {result.execution_time:.2f}s")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            results.append({
                'model': model,
                'description': description,
                'time': None,
                'error': str(e)
            })
        
        finally:
            await workflow.close()
    
    # Show comparison
    print("\n📊 PERFORMANCE COMPARISON:")
    print("-" * 60)
    print(f"{'Model':<15} {'Time (s)':<10} {'Code Length':<12} {'Messages':<10}")
    print("-" * 60)
    
    for result in results:
        if 'error' not in result:
            print(f"{result['model']:<15} {result['time']:<10.2f} {result['code_length']:<12} {result['messages']:<10}")
        else:
            print(f"{result['model']:<15} {'ERROR':<10} {'-':<12} {'-':<10}")
    
    return True


async def main():
    """Main function to run all demos"""
    print("🎉 Welcome to Claude-Agent Quick Start!")
    print("This demo will show you the multi-agent code development system in action.")
    print("=" * 70)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix the issues above and try again.")
        return
    
    print("\n✅ All prerequisites met! Starting demos...")
    
    try:
        # Run demos
        success1 = await demo_simple_function()
        
        if success1:
            input("\n⏸️  Press Enter to continue to Demo 2...")
            success2 = await demo_complex_class()
            
            if success2:
                input("\n⏸️  Press Enter to continue to Demo 3...")
                await demo_performance_comparison()
        
        print("\n" + "=" * 70)
        print("🎉 Quick Start Demo Completed!")
        print("=" * 70)
        print("\n📚 Next Steps:")
        print("1. Check out examples/ directory for more advanced usage")
        print("2. Read docs/ for detailed documentation")
        print("3. Customize agent system messages for your needs")
        print("4. Explore different models and configurations")
        print("\n💡 Tips:")
        print("- Use gpt-4o-mini for cost-effective development")
        print("- Use gpt-4 for complex production tasks")
        print("- Adjust max_rounds based on task complexity")
        print("- Lower temperature (0.1) gives more consistent results")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Handle Windows event loop policy
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Run the demo
    asyncio.run(main())
