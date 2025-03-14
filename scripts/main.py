from agents.agent_project_analyst import run

class ProjectAnalyzer:
    def __init__(self):
        print("Initializing Project Analyzer...")

    def analyze(self):
        print("Running project analysis...")
        response = run()  # Capture the response
        print("Project analysis completed.")
        return response  # Return the response for future processing

if __name__ == "__main__":
    analyzer = ProjectAnalyzer()
    response = analyzer.analyze()

    # Use the response for the next agent
    print("\nGenerated Dependency Data:")
    print(response)  # This can be passed to another agent in the future
