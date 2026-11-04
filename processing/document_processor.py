import json
import uuid
from pathlib import Path

class DocumentProcessor:
    def __init__(self):
        self.input_path=Path("data/processed/consolidated_data.json")
        self.output_path=Path("data/processed/document.json")
        self.documents=[]
    # load the consolidated profile data
    def load_data(self):
        if not self.input_path.exists():
            print(f"File {self.input_path} does not exist.")
            return None
        with open(self.input_path, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def create_document(
        self,
        content,
        category,
        source,
        metadata=None
    ):

        if not content:
            return

        document = {

            "id": str(uuid.uuid4()),

            "content": content.strip(),

            "metadata": {

                "category": category,

                "source": source,

                **(metadata or {})

            }

        }

        self.documents.append(document)

        # -----------------------------------
    # 3. Profile document
    # -----------------------------------

    def process_profile(self, data):

        profile = data.get("profile", {})

        content = f"""
        Name: {profile.get('name', '')}

        Professional Headline:
        {profile.get('headline', '')}

        Location:
        {profile.get('location', '')}

        GitHub Username:
        {profile.get('github_username', '')}

        LinkedIn Profile:
        {profile.get('linkedin_url', '')}
        """

        self.create_document(
            content=content,
            category="profile",
            source="linkedin"
        )
     # -----------------------------------
    # 4. About document
    # -----------------------------------

    def process_about(self, data):

        about = data.get("about", "")

        self.create_document(
            content=f"Professional Summary: {about}",
            category="about",
            source="linkedin"
        )
    # -----------------------------------
    # 5. Education documents
    # -----------------------------------

    def process_education(self, data):

        for education in data.get("education", []):

            content = f"""
            Institution: {education.get('institution', '')}

            School: {education.get('school', '')}

            Degree: {education.get('degree', '')}

            Field of Study:
            {education.get('field_of_study', '')}

            Duration: {education.get('duration', '')}
            """

            self.create_document(
                content=content,
                category="education",
                source="linkedin"
            )

    # -----------------------------------
    # 6. Skills document
    # -----------------------------------

    def process_skills(self, data):

        skills = data.get("skills", {})

        linkedin_skills = skills.get("linkedin", [])

        github_languages = skills.get(
            "github_languages", []
        )

        if linkedin_skills:

            content = (
                "Professional Skills: "
                + ", ".join(linkedin_skills)
            )

            self.create_document(
                content=content,
                category="skills",
                source="linkedin"
            )

        if github_languages:

            content = (
                "Programming Languages identified "
                "from GitHub repositories: "
                + ", ".join(github_languages)
            )

            self.create_document(
                content=content,
                category="programming_languages",
                source="github"
            )

    # -----------------------------------
    # 7. Experience documents
    # -----------------------------------

    def process_experience(self, data):

        for experience in data.get("experience", []):

            content = json.dumps(
                experience,
                ensure_ascii=False
            )

            self.create_document(
                content=content,
                category="experience",
                source="linkedin"
            )

    # -----------------------------------
    # 8. Project documents
    # -----------------------------------

    def process_projects(self, data):

        projects = data.get("projects", {})

        github_projects = projects.get("github", [])

        linkedin_projects = projects.get(
            "linkedin", []
        )

        # GitHub projects

        for project in github_projects:

            content = f"""
            Project Name: {project.get('name', '')}

            Description: {project.get('description', '')}

            GitHub URL: {project.get('github_url', '')}

            Primary Language:
            {project.get('primary_language', '')}

            Technologies:
            {', '.join(project.get('languages', {}).keys())}

            Topics:
            {', '.join(project.get('topics', []))}

            README:
            {project.get('readme') or ''}
            """

            self.create_document(
                content=content,
                category="project",
                source="github",
                metadata={
                    "project_name": project.get("name", ""),
                    "github_url": project.get("github_url", "")
                }
            )

        # LinkedIn projects

        for project in linkedin_projects:

            content = json.dumps(
                project,
                ensure_ascii=False
            )

            self.create_document(
                content=content,
                category="project",
                source="linkedin"
            )

    # -----------------------------------
    # 9. Certifications
    # -----------------------------------

    def process_certifications(self, data):

        for certification in data.get(
            "certifications", []
        ):

            content = json.dumps(
                certification,
                ensure_ascii=False
            )

            self.create_document(
                content=content,
                category="certification",
                source="linkedin"
            )

    # -----------------------------------
    # 10. Achievements
    # -----------------------------------

    def process_achievements(self, data):

        for achievement in data.get(
            "achievements", []
        ):

            content = json.dumps(
                achievement,
                ensure_ascii=False
            )

            self.create_document(
                content=content,
                category="achievement",
                source="linkedin"
            )

    # -----------------------------------
    # 11. LinkedIn Activity
    # -----------------------------------

    def process_activity(self, data):

        for activity in data.get("activity", []):

            content = json.dumps(
                activity,
                ensure_ascii=False
            )

            self.create_document(
                content=content,
                category="activity",
                source="linkedin"
            )

    # -----------------------------------
    # 12. Save documents
    # -----------------------------------

    def save_documents(self):

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.documents,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("\nDocuments saved successfully!")

        print(f"Output: {self.output_path}")

        print(f"Total documents: {len(self.documents)}")

    # -----------------------------------
    # 13. Execute pipeline
    # -----------------------------------

    def run(self):

        print("\nStarting Document Processing...\n")

        data = self.load_data()

        self.process_profile(data)

        self.process_about(data)

        self.process_education(data)

        self.process_skills(data)

        self.process_experience(data)

        self.process_projects(data)

        self.process_certifications(data)

        self.process_achievements(data)

        self.process_activity(data)

        self.save_documents()

        return self.documents


if __name__ == "__main__":

    processor = DocumentProcessor()

    processor.run()