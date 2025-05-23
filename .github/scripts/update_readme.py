#!/usr/bin/env python
import os
import re
from datetime import datetime
from github import Github

def main():
    """
    Main function to update the README.md with repository information.
    """
    print("Starting README update process...")
    
    # List files in current directory for debugging
    print("Files in current directory:")
    try:
        for file in os.listdir('.'):
            print(f"  - {file}")
        
        if os.path.exists('.github'):
            print("Files in .github directory:")
            for file in os.listdir('.github'):
                print(f"  - .github/{file}")
                
            if os.path.exists('.github/scripts'):
                print("Files in .github/scripts directory:")
                for file in os.listdir('.github/scripts'):
                    print(f"  - .github/scripts/{file}")
    except Exception as e:
        print(f"Error listing files: {str(e)}")
    
    # Get GitHub token from environment variable
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("No GITHUB_TOKEN found in environment variables")
    
    # Initialize GitHub API client
    g = Github(github_token)
    user = g.get_user()
    username = user.login
    
    print(f"Fetching repositories for {username}...")
    
    # Get all repositories
    repos = user.get_repos()
    
    # Create the project list in markdown format
    projects_md = f"\n## 📊 Projects Overview\n\n"
    projects_md += "| Repository | Description | Language | Last Updated |\n"
    projects_md += "|------------|-------------|----------|-------------|\n"
    
    # Add repository information to the table
    for repo in repos:
        if not repo.fork:  # Skip forked repositories
            name = repo.name
            url = repo.html_url
            description = repo.description or "No description"
            language = repo.language or "N/A"
            last_updated = repo.updated_at.strftime("%Y-%m-%d")
            
            projects_md += f"| [{name}]({url}) | {description} | {language} | {last_updated} |\n"
    
    projects_md += f"\n*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    # Read the existing README file
    readme_path = "README.md"
    with open(readme_path, "r") as f:
        readme_content = f.read()
    
    # Replace the content between the markers
    start_marker = "<!-- PROJECTS_LIST:START -->"
    end_marker = "<!-- PROJECTS_LIST:END -->"
    
    # Print debug information
    print(f"Looking for markers in README content of length {len(readme_content)}")
    if start_marker not in readme_content:
        print(f"ERROR: Start marker '{start_marker}' not found in README.md")
        # Add markers if they don't exist
        readme_content += f"\n{start_marker}\n{end_marker}\n"
    if end_marker not in readme_content:
        print(f"ERROR: End marker '{end_marker}' not found in README.md")
    
    # More robust pattern matching
    pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
    replacement = f"{start_marker}\n{projects_md}\n{end_marker}"
    
    new_readme = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)
    
    # Write the updated README
    with open(readme_path, "w") as f:
        f.write(new_readme)
    
    print("README.md has been updated successfully!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: Script failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
