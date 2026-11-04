import json
from pathlib import Path

class DataConsolidator:
    def __init__(self):
        self.github_dir=Path("data/raw/github")
        self.linkedin_dir=Path("data/raw/linkedin")
        self.output_dir=Path("data/raw/processed")

    def load_json(self,file_path):
        if not Path(file_path).exists():
            print(f"File {file_path} does not exist.")
            return None
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    def load_github_data(self):
        print("loading github data...")
        github_profile=self.load_json(self.github_dir/"profile.json")
        github_repositories=self.load_json(self.github_dir/"repositories.json")
        github_projects=self.load_json(self.github_dir/"projects.json")
        return {
            "profile": github_profile or {},
            "repositories": github_repositories or [],
            "projects": github_projects or []
        }
    def load_linkedin_data(self):
        print("loading linkedin data")
        linkedin_profile=self.load_json(self.linkedin_dir/"linkedin_profile.json")
        return linkedin_profile or {}
    # consolidate data from both sources
    def consolidate(self):
        github = self.load_github_data()
        linkedin = self.load_linkedin_data()
        linkedin_profile = linkedin.get("profile", {})
        github_profile = github.get("profile", {})
        # LinkedIn is preferred for professional details.
        # GitHub provides additional technical information.
        unified_data = {

            "source": [
                "github",
                "linkedin"
            ],

            "profile": {

                "name": (
                    linkedin_profile.get("name")
                    or github_profile.get("name")
                ),

                "headline": linkedin_profile.get("headline"),

                "location": linkedin_profile.get("location"),

                "pronouns": linkedin_profile.get("pronouns"),

                "linkedin_url": linkedin_profile.get("profile_url"),

                "github_username": github_profile.get("login"),

                "github_url": github_profile.get("html_url"),

                "connections": linkedin_profile.get("connections"),

                "followers": linkedin_profile.get("followers")

            },

            "about": linkedin.get("about", ""),

            "education": linkedin.get("education", []),

            "skills": {

                "linkedin": linkedin.get("skills", []),

                "github_languages": list({

                    language

                    for project in github["projects"]

                    for language in project.get("languages", {}).keys()

                })

            },

            "experience": linkedin.get("experience", []),

            "projects": {

                "github": github["projects"],

                "linkedin": linkedin.get("projects", [])

            },

            "certifications": linkedin.get("certifications", []),

            "achievements": linkedin.get("achievements", []),

            "activity": linkedin.get("activity", []),

            "repositories": github["repositories"],

            "metadata": {

                "github_repository_count": len(github["repositories"]),

                "github_project_count": len(github["projects"]),

                "linkedin_skill_count": len(linkedin.get("skills", [])),

                "data_sources": 2

            }

        }

        return unified_data

    # ---------------------------------
    # Save consolidated data to a JSON file
    # ---------------------------------
    def save_data(self,data):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_file = self.output_dir / "consolidated_data.json"
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print(f"Consolidated data saved to {output_file}")

    def run(self):
        unified_data=self.consolidate()
        self.save_data(unified_data)
        print("Data consolidation complete.")
        print(
            "GitHub repositories:",
            unified_data["metadata"]["github_repository_count"]
        )

        print(
            "GitHub projects:",
            unified_data["metadata"]["github_project_count"]
        )

        print(
            "LinkedIn skills:",
            unified_data["metadata"]["linkedin_skill_count"]
        )

        return unified_data


if __name__ == "__main__":

    consolidator = DataConsolidator()

    consolidator.run()