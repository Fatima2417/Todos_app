try:
    import cohere
    print("cohere imported successfully")
except ImportError:
    print("cohere NOT found")

try:
    import fastmcp
    print("fastmcp imported successfully")
except ImportError:
    print("fastmcp NOT found")

try:
    import agents
    print("agents imported successfully")
except ImportError:
    print("agents NOT found")

try:
    import strands
    print("strands imported successfully")
except ImportError:
    print("strands NOT found")

try:
    import openai_agents
    print("openai_agents imported successfully")
except ImportError:
    print("openai_agents NOT found")
