"""
Fibonacci Example: Focused Implementation

This example focuses specifically on creating an optimized Fibonacci implementation
to demonstrate the iterative improvement process of the multi-agent system.
"""

import asyncio
import os
from multi_agent_workflow import CodeDevelopmentWorkflow


async def fibonacci_optimization_demo():
    """Demonstrate the optimization process for Fibonacci implementation"""
    
    task = """
    Create a comprehensive Fibonacci implementation in Python with the following requirements:
    
    1. Multiple implementation approaches:
       - Naive recursive approach (for comparison)
       - Memoized recursive approach
       - Iterative approach
       - Matrix exponentiation approach (for very large n)
    
    2. A main Fibonacci class that:
       - Automatically selects the best algorithm based on input size
       - Provides performance benchmarking
       - Includes caching for frequently requested values
       - Supports both single value and sequence generation
    
    3. Advanced features:
       - Input validation with custom exceptions
       - Support for negative Fibonacci numbers
       - Floating-point precision handling for large numbers
       - Optional visualization of the sequence
       - Performance metrics and timing
    
    4. Code quality requirements:
       - Comprehensive type hints
       - Detailed docstrings with complexity analysis
       - Unit tests for all methods
       - Error handling for edge cases
       - Clean, maintainable code structure
    
    5. Optimization considerations:
       - Memory efficiency for large sequences
       - CPU optimization for repeated calls
       - Numerical stability for large values
    """
    
    print("🔢 Fibonacci Optimization Demonstration")
    print("This example shows how the agents iteratively improve code quality")
    print("=" * 70)
    
    # Use high-performance model for best results
    workflow = CodeDevelopmentWorkflow(
        model="gpt-4",
        temperature=0.1,
        max_rounds=12
    )
    
    try:
        result = await workflow.run(task, verbose=True)
        
        print("\n" + "=" * 70)
        print("📋 CONVERSATION ANALYSIS")
        print("=" * 70)
        
        # Analyze the conversation flow
        agents_messages = {"CodeWriter": [], "CodeReviewer": [], "CodeOptimizer": []}
        
        for message in result.conversation_history:
            agent = message.get('source', 'Unknown')
            if agent in agents_messages:
                agents_messages[agent].append(message.get('content', ''))
        
        print(f"\n👨‍💻 Code Writer contributed {len(agents_messages['CodeWriter'])} messages")
        print(f"🔍 Code Reviewer contributed {len(agents_messages['CodeReviewer'])} messages")
        print(f"⚡ Code Optimizer contributed {len(agents_messages['CodeOptimizer'])} messages")
        
        print("\n" + "=" * 70)
        print("📈 EVOLUTION TRACKING")
        print("=" * 70)
        
        print("\n1️⃣ INITIAL CODE (from Code Writer):")
        print("-" * 40)
        if result.initial_code and result.initial_code != "No code found":
            print(result.initial_code[:500] + "..." if len(result.initial_code) > 500 else result.initial_code)
        else:
            print("Code not properly extracted")
        
        print("\n2️⃣ REVIEW FEEDBACK (from Code Reviewer):")
        print("-" * 40)
        if result.review_feedback and result.review_feedback != "No review found":
            print(result.review_feedback[:500] + "..." if len(result.review_feedback) > 500 else result.review_feedback)
        else:
            print("Review not properly extracted")
        
        print("\n3️⃣ FINAL OPTIMIZED CODE (from Code Optimizer):")
        print("-" * 40)
        print(result.final_code)
        
        print("\n" + "=" * 70)
        print("📊 PERFORMANCE METRICS")
        print("=" * 70)
        print(f"⏱️  Total Execution Time: {result.execution_time:.2f} seconds")
        print(f"💬 Total Messages: {len(result.conversation_history)}")
        print(f"📏 Final Code Length: {len(result.final_code):,} characters")
        
        # Analyze code quality indicators
        code_quality_score = 0
        quality_checks = {
            "Has type hints": "->" in result.final_code,
            "Has docstrings": '"""' in result.final_code or "'''" in result.final_code,
            "Has error handling": "try:" in result.final_code or "except" in result.final_code,
            "Has classes": "class " in result.final_code,
            "Has main function": "def main(" in result.final_code or "if __name__" in result.final_code,
            "Has comments": "#" in result.final_code,
            "Has performance optimization": "cache" in result.final_code.lower() or "memo" in result.final_code.lower()
        }
        
        print("\n🏆 CODE QUALITY ANALYSIS:")
        for check, passed in quality_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")
            if passed:
                code_quality_score += 1
        
        print(f"\n📊 Overall Quality Score: {code_quality_score}/{len(quality_checks)} ({code_quality_score/len(quality_checks)*100:.1f}%)")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during Fibonacci demonstration: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    finally:
        await workflow.close()


async def compare_fibonacci_approaches():
    """Compare different approaches to Fibonacci implementation"""
    
    approaches = {
        "Simple Recursive": """
        Create a simple recursive Fibonacci function in Python.
        Focus on clarity and correctness, not performance.
        """,
        
        "Optimized Iterative": """
        Create an optimized iterative Fibonacci function in Python.
        Focus on performance and memory efficiency.
        Include input validation and error handling.
        """,
        
        "Enterprise-Grade": """
        Create an enterprise-grade Fibonacci implementation with:
        - Multiple algorithms (recursive, iterative, matrix)
        - Performance benchmarking
        - Caching and memoization
        - Comprehensive testing
        - Full documentation
        """
    }
    
    print("\n" + "=" * 80)
    print("🔄 FIBONACCI APPROACH COMPARISON")
    print("=" * 80)
    
    results = {}
    
    for approach_name, task in approaches.items():
        print(f"\n🚀 Testing {approach_name} Approach...")
        print("-" * 50)
        
        workflow = CodeDevelopmentWorkflow(
            model="gpt-4o-mini",  # Use faster model for comparison
            temperature=0.1,
            max_rounds=6  # Shorter rounds for comparison
        )
        
        try:
            result = await workflow.run(task, verbose=False)  # Silent mode for comparison
            results[approach_name] = result
            
            print(f"✅ {approach_name}: {result.execution_time:.2f}s, {len(result.final_code)} chars")
            
        except Exception as e:
            print(f"❌ {approach_name}: Failed - {e}")
            results[approach_name] = None
        
        finally:
            await workflow.close()
    
    # Generate comparison report
    print("\n" + "=" * 80)
    print("📊 COMPARISON RESULTS")
    print("=" * 80)
    
    for approach_name, result in results.items():
        if result:
            print(f"\n📋 {approach_name}:")
            print(f"   ⏱️  Execution Time: {result.execution_time:.2f}s")
            print(f"   📏 Code Length: {len(result.final_code):,} characters")
            print(f"   💬 Messages: {len(result.conversation_history)}")
            
            # Show a snippet of the final code
            snippet = result.final_code[:200] + "..." if len(result.final_code) > 200 else result.final_code
            print(f"   📝 Code Preview: {snippet}")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Please set your OPENAI_API_KEY environment variable")
        exit(1)
    
    async def main():
        # Run the main Fibonacci optimization demo
        await fibonacci_optimization_demo()
        
        # Run the comparison demo
        await compare_fibonacci_approaches()
        
        print("\n🎉 Fibonacci examples completed!")
        print("\nKey takeaways:")
        print("- The agents work together to iteratively improve code quality")
        print("- Each agent has a specialized role in the development process")
        print("- The round-robin approach ensures comprehensive coverage")
        print("- Different task complexities yield different optimization levels")
    
    asyncio.run(main())
