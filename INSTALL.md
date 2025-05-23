# Installation Guide

## Quick Installation

### 1. Install Dependencies

```bash
# Install core AutoGen 0.4.x packages
pip install -U "autogen-agentchat" "autogen-ext[openai]"
```

### 2. Set API Key

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your_openai_api_key_here"
```

### 3. Run Example

```bash
# Clone and run
git clone https://github.com/Joseph19820124/Claude-Agent.git
cd Claude-Agent
python multi_agent_workflow.py
```

## Complete Installation Steps

### Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Git (for cloning the repository)

### Step-by-Step Installation

1. **Create Virtual Environment** (Recommended)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install AutoGen 0.4.x**
   ```bash
   pip install -U "autogen-agentchat>=0.4.0" "autogen-ext[openai]>=0.4.0"
   ```

3. **Install Additional Dependencies**
   ```bash
   pip install python-dotenv asyncio-compat
   ```

4. **Clone Repository**
   ```bash
   git clone https://github.com/Joseph19820124/Claude-Agent.git
   cd Claude-Agent
   ```

5. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your OpenAI API key
   ```

6. **Test Installation**
   ```bash
   python -c "import autogen_agentchat; print('AutoGen installed successfully')"
   ```

## Usage Examples

### Basic Example
```python
import asyncio
from multi_agent_workflow import CodeDevelopmentWorkflow

async def main():
    workflow = CodeDevelopmentWorkflow(model="gpt-4o-mini")
    result = await workflow.run("Create a function to calculate factorial")
    print(result.final_code)
    await workflow.close()

asyncio.run(main())
```

### Production Example
```python
import asyncio
import os
from multi_agent_workflow import CodeDevelopmentWorkflow

async def main():
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable")
        return
    
    # Initialize with production settings
    workflow = CodeDevelopmentWorkflow(
        model="gpt-4",
        temperature=0.1,
        max_rounds=12
    )
    
    try:
        task = """
        Create a robust email validation function that:
        1. Uses regex for format validation
        2. Handles international domains
        3. Includes comprehensive error handling
        4. Provides detailed docstring with examples
        """
        
        result = await workflow.run(task, verbose=True)
        
        # Save result to file
        with open("generated_code.py", "w") as f:
            f.write(result.final_code)
        
        print(f"Code generated successfully in {result.execution_time:.2f} seconds")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await workflow.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'autogen_agentchat'**
   ```bash
   # Solution: Install correct package
   pip install -U "autogen-agentchat" "autogen-ext[openai]"
   ```

2. **ValueError: OpenAI API key must be provided**
   ```bash
   # Solution: Set environment variable
   export OPENAI_API_KEY="your_key_here"
   ```

3. **ModuleNotFoundError: No module named 'openai'**
   ```bash
   # Solution: Install OpenAI package
   pip install openai>=1.0.0
   ```

### Verification

Run this verification script to ensure everything is working:

```python
import asyncio
import os

async def verify_installation():
    print("🔍 Verifying Claude-Agent installation...")
    
    # Check Python version
    import sys
    print(f"✅ Python version: {sys.version}")
    
    # Check AutoGen
    try:
        import autogen_agentchat
        print(f"✅ AutoGen AgentChat: {autogen_agentchat.__version__}")
    except ImportError:
        print("❌ AutoGen AgentChat not found")
        return False
    
    # Check OpenAI
    try:
        import openai
        print(f"✅ OpenAI: {openai.__version__}")
    except ImportError:
        print("❌ OpenAI package not found")
        return False
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OpenAI API key found")
    else:
        print("❌ OpenAI API key not found")
        return False
    
    # Test basic workflow
    try:
        from multi_agent_workflow import CodeDevelopmentWorkflow
        workflow = CodeDevelopmentWorkflow(model="gpt-4o-mini", max_rounds=3)
        
        result = await workflow.run(
            "Create a simple function that adds two numbers",
            verbose=False
        )
        await workflow.close()
        
        print("✅ Basic workflow test passed")
        print(f"📊 Generated {len(result.final_code)} characters of code")
        return True
        
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(verify_installation())
    if success:
        print("\n🎉 Installation verified successfully!")
        print("You're ready to use Claude-Agent!")
    else:
        print("\n❌ Installation verification failed.")
        print("Please check the troubleshooting section.")
```

## Advanced Configuration

### Custom Model Configuration
```python
# Using different models
workflows = {
    "fast": CodeDevelopmentWorkflow(model="gpt-4o-mini"),
    "balanced": CodeDevelopmentWorkflow(model="gpt-4o"),
    "premium": CodeDevelopmentWorkflow(model="gpt-4")
}
```

### Environment Variables
Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_MODEL=gpt-4o-mini
DEFAULT_TEMPERATURE=0.1
DEFAULT_MAX_ROUNDS=10
LOG_LEVEL=INFO
```

### Development Setup
For contributors and developers:
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run tests
pytest tests/ -v

# Format code
black .
flake8 .
mypy .
```

## Next Steps

1. **Explore Examples**: Check the `examples/` directory for more usage patterns
2. **Read Documentation**: See `docs/` for detailed API reference
3. **Run Tests**: Execute `pytest tests/` to ensure everything works
4. **Customize Agents**: Modify agent system messages for your specific needs
5. **Join Community**: Participate in GitHub Discussions for support

## Support

- 📚 **Documentation**: Check the `docs/` folder
- 🐛 **Issues**: Report bugs on GitHub Issues
- 💬 **Discussions**: Ask questions in GitHub Discussions
- 📧 **Email**: Contact through GitHub profile

Happy coding with Claude-Agent! 🚀
