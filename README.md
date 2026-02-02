# PDF CV Generator

This Python tool generates professional PDF resumes from a JSON configuration file. It supports multi-audience targeting, allowing you to maintain one source of truth for your professional experience while generating tailored CVs for different roles (e.g., Frontend, Backend, DevOps).

## Features

- **Multi-Audience Targeting:** Define specific summaries, skills, and experience bullets for different roles.
- **Automatic Formatting:** Automatically bolds common technical terms (languages, frameworks, tools) within your text.
- **Professional Layout:** Generates a clean, modern PDF layout using `ReportLab`.
- **Easy Configuration:** Simple JSON structure to manage your CV content.

## Setup

1. **Create and activate a virtual environment:**
   ```bash
   # Create the virtual environment folder called 'vend'
   python3 -m venv vend

   # Source (activate) the environment
   source vend/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Script:**
   ```bash
   python generate_resume.py
   ```
   *Note: If `content.json` does not exist, the script will automatically generate a default file for you to modify.*

## Default Content Structure

Below is the structure of the `content.json` file. You can use this as a template:

```json
{
    "name": "John Doe",
    "contact_info": {
        "phone": "+1 555-0123-456",
        "email": "john.doe@example.com",
        "linkedin_url": "https://www.linkedin.com/in/johndoe-fake/",
        "github_url": "https://github.com/johndoe-fake"
    },
    "summary": [
        {
            "text": "<b>Senior Full-Stack Engineer</b> with 8+ years of experience building scalable web applications. Expert in modern JavaScript ecosystems (React, Node.js) and cloud-native architectures. Proven ability to lead teams, design RESTful APIs, and optimize frontend performance.",
            "target_audiences": ["fullstack", "frontend", "backend"]
        },
        {
            "text": "<b>DevOps & Site Reliability Engineer</b> passionate about automation and infrastructure as code. Specialized in Kubernetes, AWS, and CI/CD pipelines. Experienced in scaling high-traffic systems and ensuring 99.99% availability through robust monitoring and security practices.",
            "target_audiences": ["devops", "backend"]
        }
    ],
    "skills": [
        {
            "text": "<b>Languages:</b> JavaScript (ES6+), TypeScript, Python, Go, Bash<br/><b>Frontend:</b> React, Next.js, Redux, Tailwind CSS, HTML5/CSS3<br/><b>Backend:</b> Node.js, Express.js, Django, PostgreSQL, Redis, MongoDB<br/><b>DevOps:</b> Docker, Kubernetes, AWS, Terraform, Jenkins, GitHub Actions, Prometheus",
            "target_audiences": ["fullstack", "backend", "devops"]
        },
        {
            "text": "<b>Languages:</b> JavaScript, TypeScript, HTML5, CSS3<br/><b>Frontend:</b> React, Vue.js, Next.js, Webpack, Babel, Sass, Jest, Cypress<br/><b>UI/UX:</b> Figma, Material-UI, Styled-Components, Accessibility (WCAG)",
            "target_audiences": ["frontend"]
        }
    ],
    "experience": [
        {
            "title": "Senior Software Engineer",
            "company": "TechNova Solutions",
            "dates": "Jan 2022 – Present",
            "intro": "Lead developer for the company's flagship e-commerce product, managing a team of 5 engineers.",
            "bullets": [
                {
                    "text": "Architected and built a microservices-based e-commerce platform using Node.js and Go, handling 10k+ concurrent users.",
                    "target_audiences": ["backend", "fullstack"]
                },
                {
                    "text": "Led the migration of the legacy monolithic frontend to a modern Next.js application, improving Core Web Vitals by 40%.",
                    "target_audiences": ["frontend", "fullstack"]
                },
                {
                    "text": "Implemented a fully automated CI/CD pipeline using GitHub Actions and ArgoCD, reducing deployment time from 1 hour to 5 minutes.",
                    "target_audiences": ["devops", "backend"]
                }
            ]
        },
        {
            "title": "Full Stack Developer",
            "company": "Orbit Systems",
            "dates": "Jun 2019 – Dec 2021",
            "intro": "",
            "bullets": [
                {
                    "text": "Developed responsive, interactive user interfaces using React and Redux, ensuring cross-browser compatibility.",
                    "target_audiences": ["frontend", "fullstack"]
                },
                {
                    "text": "Built and maintained RESTful APIs using Python (Django) and integrated with PostgreSQL databases.",
                    "target_audiences": ["backend", "fullstack"]
                }
            ]
        }
    ],
    "education": "<b>B.Sc. in Computer Science</b>, University of Technology · 2013–2017",
    "languages": "English – Native | Spanish – Fluent"
}
```

## Configuration (`content.json`)

The CV content is managed in `content.json`. Below is an explanation of the key fields:

- `name`: Your full name.
- `contact_info`: A dictionary containing your `phone`, `email`, and optional `linkedin_url` and `github_url`.
- `summary`: A list of summary objects.
- `skills`: A list of skill category objects.
- `experience`: A list of job objects, each containing `title`, `company`, `dates`, an optional `intro` (displayed above bullets), and a list of `bullets`.
- `education`: A string describing your education.
- `languages`: A string describing your language proficiencies.

### How `target_audiences` Works

The power of this tool lies in the `target_audiences` property found in `summary`, `skills`, and `experience` bullets.

1. **Defining Audiences:** You can assign a list of strings to `target_audiences` for any piece of content. For example: `"target_audiences": ["frontend", "fullstack"]`.
2. **Filtering:** When you run the script, it identifies all unique audience strings used throughout the file.
3. **Generation:** It generates one separate PDF for **every** audience found.
   - If an item has **no** `target_audiences` (or it's empty), it is considered **universal** and will appear in all generated PDFs.
   - If an item has specific audiences listed, it will **only** appear in the PDFs corresponding to those audiences.

#### Example
If your `content.json` has:
- A bullet with `"target_audiences": ["backend"]`
- A bullet with `"target_audiences": ["frontend", "fullstack"]`
- A bullet with no `target_audiences`

The script will generate three PDFs:
- `Your_Name_CV_Backend_...pdf` (contains the backend and universal bullets)
- `Your_Name_CV_Frontend_...pdf` (contains the frontend and universal bullets)
- `Your_Name_CV_Fullstack_...pdf` (contains the fullstack and universal bullets)

## Technical Term Highlighting

The script contains an extensive list of `TECH_TERMS` (like Python, React, AWS, etc.). Any matching term found in your summary or experience bullets will be automatically wrapped in `<b>` tags to be bolded in the final PDF, saving you from manual formatting.
