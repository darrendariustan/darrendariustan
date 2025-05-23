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
    
    pattern = f"{start_marker}(.*?){end_marker}"
    replacement = f"{start_marker}\n{projects_md}\n{end_marker}"
    
    new_readme = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)
    
    # Write the updated README
    with open(readme_path, "w") as f:
        f.write(new_readme)
    
    print("README.md has been updated successfully!")

if __name__ == "__main__":
    main()
