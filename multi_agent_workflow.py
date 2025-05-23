"""
Multi-Agent Code Development Workflow using AutoGen 0.4.x

This module implements a three-agent system for code development:
1. Code Writer Agent - Generates initial code
2. Code Reviewer Agent - Reviews and provides feedback
3. Code Optimizer Agent - Optimizes based on review

Author: Claude-Agent Project
License: MIT
"""

import asyncio
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

# AutoGen 0.4.x imports
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


@dataclass
class WorkflowResult:
    """Result container for the code development workflow"""
    original_task: str
    initial_code: str
    review_feedback: str
    final_code: str
    conversation_history: List[Dict[str, Any]]
    execution_time: float
    token_usage: Optional[Dict[str, int]] = None


class CodeDevelopmentWorkflow:
    """
    Multi-agent workflow for collaborative code development using AutoGen 0.4.x
    
    This class orchestrates three specialized agents in a round-robin pattern:
    - CodeWriterAgent: Generates initial code based on requirements
    - CodeReviewerAgent: Analyzes code and provides optimization suggestions
    - CodeOptimizerAgent: Refines code based on original code and review feedback
    """
    
    def __init__(
        self,
        model: str = "gpt-4",
        temperature: float = 0.1,
        max_rounds: int = 10,
        api_key: Optional[str] = None
    ):
        """
        Initialize the code development workflow
        
        Args:
            model: OpenAI model to use (e.g., "gpt-4", "gpt-4o-mini")
            temperature: Model temperature for consistency (0.0-1.0)
            max_rounds: Maximum conversation rounds
            api_key: OpenAI API key (if not set in environment)
        """
        self.model = model
        self.temperature = temperature
        self.max_rounds = max_rounds
        
        # Set up API key
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        elif not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OpenAI API key must be provided via parameter or OPENAI_API_KEY environment variable")
        
        # Initialize model client
        self.model_client = OpenAIChatCompletionClient(
            model=self.model,
            temperature=self.temperature
        )
        
        # Initialize agents
        self._create_agents()
        
        # Set up termination conditions
        self.termination_condition = (
            MaxMessageTermination(max_messages=self.max_rounds) | 
            TextMentionTermination("WORKFLOW_COMPLETE")
        )
    
    def _create_agents(self) -> None:
        """Create and configure the three specialized agents"""
        
        # Code Writer Agent
        self.code_writer = AssistantAgent(
            name="CodeWriter",
            model_client=self.model_client,
            system_message="""You are a skilled software developer specializing in writing clean, efficient code.

Your responsibilities:
1. Analyze the given requirements carefully
2. Write well-structured, functional code that meets the specifications
3. Include appropriate comments and docstrings
4. Follow best practices and coding conventions
5. Provide a brief explanation of your implementation approach

Guidelines:
- Write production-ready code with proper error handling
- Use meaningful variable and function names
- Include type hints where appropriate (Python)
- Keep code modular and maintainable
- Focus on correctness and readability

When you complete your code, end your message with "CODE_WRITTEN" to signal completion."""
        )
        
        # Code Reviewer Agent
        self.code_reviewer = AssistantAgent(
            name="CodeReviewer", 
            model_client=self.model_client,
            system_message="""You are an expert code reviewer with extensive experience in software quality assurance.

Your responsibilities:
1. Thoroughly analyze the provided code for quality, efficiency, and best practices
2. Identify potential improvements in performance, readability, and maintainability
3. Check for security vulnerabilities and edge cases
4. Suggest specific optimizations and refactoring opportunities
5. Provide constructive, actionable feedback

Review criteria:
- Code correctness and functionality
- Performance optimization opportunities
- Security considerations
- Code style and conventions
- Error handling and edge cases
- Maintainability and scalability
- Documentation quality

Provide your review in a structured format:
- Overall Assessment
- Strengths
- Areas for Improvement
- Specific Recommendations
- Security Considerations (if any)

When you complete your review, end your message with "REVIEW_COMPLETE" to signal completion."""
        )
        
        # Code Optimizer Agent
        self.code_optimizer = AssistantAgent(
            name="CodeOptimizer",
            model_client=self.model_client,
            system_message="""You are a code optimization specialist focused on improving code quality and performance.

Your responsibilities:
1. Take the original code and the reviewer's feedback
2. Implement the suggested improvements and optimizations
3. Enhance performance while maintaining functionality
4. Improve code structure and readability
5. Add any missing error handling or edge case coverage

Optimization priorities:
- Implement all valid suggestions from the code review
- Optimize for performance without sacrificing readability
- Enhance error handling and robustness
- Improve code documentation and comments
- Ensure backward compatibility if applicable
- Maintain or improve test coverage

Provide:
- The optimized code with all improvements
- A summary of changes made
- Performance improvements achieved
- Any additional considerations for future development

When you complete the optimization, end your message with "WORKFLOW_COMPLETE" to signal completion."""
        )
    
    async def run(self, task: str, verbose: bool = True) -> WorkflowResult:
        """
        Execute the complete code development workflow
        
        Args:
            task: The coding task/requirements to implement
            verbose: Whether to print conversation to console
            
        Returns:
            WorkflowResult containing all outputs and metadata
        """
        start_time = datetime.now()
        
        if verbose:
            print(f"🚀 Starting Code Development Workflow")
            print(f"📋 Task: {task}")
            print(f"🤖 Model: {self.model}")
            print("=" * 60)
        
        # Create the round-robin team
        team = RoundRobinGroupChat(
            participants=[self.code_writer, self.code_reviewer, self.code_optimizer]
        )
        
        # Set up console for output if verbose
        if verbose:
            console = Console()
        
        try:
            # Run the team workflow
            if verbose:
                result = await console.run_stream(
                    task=task,
                    team=team,
                    termination_condition=self.termination_condition
                )
            else:
                result = await team.run(
                    task=task,
                    termination_condition=self.termination_condition
                )
            
            # Extract results from conversation
            conversation_history = result.messages if hasattr(result, 'messages') else []
            
            # Parse the conversation to extract key outputs
            initial_code = self._extract_code_from_messages(conversation_history, "CodeWriter")
            review_feedback = self._extract_review_from_messages(conversation_history, "CodeReviewer")
            final_code = self._extract_code_from_messages(conversation_history, "CodeOptimizer")
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            workflow_result = WorkflowResult(
                original_task=task,
                initial_code=initial_code,
                review_feedback=review_feedback,
                final_code=final_code,
                conversation_history=conversation_history,
                execution_time=execution_time,
                token_usage=getattr(result, 'usage', None)
            )
            
            if verbose:
                print("\n" + "=" * 60)
                print("✅ Workflow completed successfully!")
                print(f"⏱️  Execution time: {execution_time:.2f} seconds")
                print("=" * 60)
            
            return workflow_result
            
        except Exception as e:
            if verbose:
                print(f"\n❌ Error during workflow execution: {str(e)}")
            raise
    
    def _extract_code_from_messages(self, messages: List[Dict], agent_name: str) -> str:
        """Extract code blocks from messages sent by a specific agent"""
        code_blocks = []
        
        for message in messages:
            if message.get('source') == agent_name:
                content = message.get('content', '')
                # Look for code blocks (markdown format)
                import re
                code_matches = re.findall(r'```(?:python)?\n(.*?)\n```', content, re.DOTALL)
                code_blocks.extend(code_matches)
        
        return '\n\n'.join(code_blocks) if code_blocks else "No code found"
    
    def _extract_review_from_messages(self, messages: List[Dict], agent_name: str) -> str:
        """Extract review content from messages sent by the reviewer agent"""
        reviews = []
        
        for message in messages:
            if message.get('source') == agent_name:
                content = message.get('content', '')
                reviews.append(content)
        
        return '\n\n'.join(reviews) if reviews else "No review found"
    
    async def close(self) -> None:
        """Clean up resources"""
        if self.model_client:
            await self.model_client.close()


# Example usage and testing
async def main():
    """Example usage of the CodeDevelopmentWorkflow"""
    
    # Example task
    task = """
    Create a Python function that calculates the Fibonacci sequence up to n terms 
    using dynamic programming for optimal performance. The function should:
    
    1. Accept an integer n as input
    2. Return a list of Fibonacci numbers up to n terms
    3. Handle edge cases (n <= 0, n = 1, n = 2)
    4. Use dynamic programming to optimize performance
    5. Include proper input validation and error handling
    6. Provide comprehensive docstring with examples
    """
    
    # Initialize workflow
    workflow = CodeDevelopmentWorkflow(
        model="gpt-4o-mini",  # Using cost-effective model for example
        temperature=0.1,
        max_rounds=12
    )
    
    try:
        # Run the workflow
        result = await workflow.run(task, verbose=True)
        
        # Display results
        print("\n" + "="*80)
        print("📊 WORKFLOW RESULTS")
        print("="*80)
        
        print("\n🎯 ORIGINAL TASK:")
        print(result.original_task)
        
        print("\n📝 INITIAL CODE:")
        print(result.initial_code)
        
        print("\n🔍 REVIEW FEEDBACK:")
        print(result.review_feedback)
        
        print("\n🚀 FINAL OPTIMIZED CODE:")
        print(result.final_code)
        
        print(f"\n⏱️ EXECUTION TIME: {result.execution_time:.2f} seconds")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    finally:
        # Clean up
        await workflow.close()


if __name__ == "__main__":
    asyncio.run(main())