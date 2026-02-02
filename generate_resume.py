import json
import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_RIGHT

# =============================================================================
# CONSTANTS & CONFIG
# =============================================================================

JSON_FILENAME = "content.json"

# Expanded Tech Terms for Bold Formatting
# Sorted by length (descending) to ensure "Spring Boot" matches before "Spring"
TECH_TERMS = sorted([
    # --- Languages (Modern & Legacy) ---
    "JavaScript", "TypeScript", "Python", "Java", "Golang", "Go", "C++", "C#", "C", "Rust",
    "Ruby", "PHP", "Swift", "Kotlin", "Objective-C", "Scala", "Elixir", "Haskell", "Lua",
    "Dart", "Solidity", "Vyper", "Perl", "Groovy", "Clojure", "F#", "OCaml", "Erlang",
    "Assembly", "VHDL", "Verilog", "R", "MATLAB", "Julia", "Bash", "Shell", "PowerShell",
    "COBOL", "Fortran", "Pascal", "Ada", "Lisp", "Scheme", "Racket", "Smalltalk", "Tcl",
    "Crystal", "Nim", "Zig", "ReasonML", "PureScript", "Elm", "Hack", "Visual Basic", "VBA",
    "ActionScript", "ColdFusion", "Delphi", "Eiffel", "FoxPro", "LabVIEW", "Ladder Logic",
    "Modula-2", "PL/SQL", "Transact-SQL", "T-SQL", "Simulink", "Standard ML", "Wolfram Language",
    "Mathematica", "APL", "J", "PostScript", "Awk", "Sed", "XSLT", "XPath",

    # --- Frontend & Web ---
    "React", "React.js", "Next.js", "Vue", "Vue.js", "Angular", "Svelte", "Ember.js",
    "Backbone.js", "jQuery", "Redux", "Jotai", "Zustand", "MobX", "Recoil", "Context API",
    "React Query", "TanStack Query", "SWR", "Formik", "React Hook Form", "Webpack", "Vite",
    "Parcel", "Rollup", "Babel", "ESBuild", "Bun", "Deno", "HTML", "HTML5", "CSS", "CSS3",
    "Sass", "SCSS", "Less", "Stylus", "Tailwind", "Tailwind CSS", "Bootstrap", "Material-UI",
    "MUI", "Chakra UI", "Ant Design", "Styled-Components", "Emotion", "Bulma", "Foundation",
    "WebAssembly", "WASM", "WebGL", "Three.js", "D3.js", "Chart.js", "Highcharts",
    "React Router", "Gatsby", "Nuxt.js", "Remix", "Astro", "SolidJS", "Qwik", "Alpine.js",
    "Lit", "Stencil", "RxJS", "Zod", "Yup", "Immer", "Lodash", "Moment.js", "Date-fns",
    "Handlebars", "Mustache", "Pug", "Jade", "EJS", "Liquid", "Nunjucks", "Smarty",
    "Blade", "Twig", "Jinja2", "HTMX", "Hyperscript", "Pico.css", "DaisyUI", "Mantine",
    "Headless UI", "Radix UI", "Shadcn", "Storybook", "Framer Motion", "GSAP", "Anime.js",
    "Leaflet", "Mapbox", "OpenLayers", "Cesium", "Video.js", "Plyr", "Howler.js",

    # --- Backend & Frameworks ---
    "Node.js", "Express.js", "Spring", "Spring Boot", "Django", "Flask", "FastAPI",
    "Ruby on Rails", "Laravel", "Symfony", "ASP.NET", ".NET", ".NET Core", "NestJS", "Koa",
    "Hapi", "Meteor", "Phoenix", "Gin", "Echo", "Fiber", "Play Framework", "Hibernate",
    "JPA", "Entity Framework", "Prisma", "TypeORM", "Sequelize", "Mongoose", "SQLAlchemy",
    "CakePHP", "CodeIgniter", "Yii", "Zend", "Slim", "Sinatra", "Hanami", "Grails", "Dropwizard",
    "Micronaut", "Quarkus", "Helidon", "Ktor", "Rocket", "Actix", "Axum", "Revel", "Beego",
    "LoopBack", "Sails.js", "AdonisJS", "Feathers", "Moleculer", "Fastify", "Restify",
    "Sanic", "Tornado", "Pyramid", "Bottle", "CherryPy", "Falcon", "Hug", "Masonite",
    "Vapor", "Kitura", "Perfect", "Buffalo", "Martini", "Iris", "Chi", "Gorilla Mux",
    "Vert.x", "Ratpack", "Spark Java", "Javalin", "Struts", "JSF", "Vaadin", "Wicket",
    "Gails", "ColdBox", "Mojolicious", "Catalyst", "Dancer", "Plack", "Laminas", "Phalcon",

    # --- Mobile & Desktop ---
    "React Native", "Flutter", "Ionic", "Xamarin", "Expo", "Electron", "Tauri",
    "SwiftUI", "UIKit", "Jetpack Compose", "Android SDK", "iOS SDK", "Cordova", "PhoneGap",
    "NativeScript", "Capacitor", "Qt", "GTK", "WPF", "WinForms", "Cocoa", "Cocoa Touch",
    "Maui", "Uno Platform", "Avalonia", "Kivy", "BeeWare", "Tkinter", "PyQt", "PySide",
    "WxPython", "Fyne", "Gio", "Sciter", "NW.js", "Neutralinojs", "Proton Native",
    "AppKit", "Carbon", "UWP", "WinUI", "MFC", "ATL", "VCL", "FireMonkey",

    # --- Database & Data ---
    "SQL", "MySQL", "PostgreSQL", "SQLite", "MariaDB", "MSSQL", "NoSQL", "MongoDB",
    "Cassandra", "DynamoDB", "CouchDB", "Redis", "Memcached", "Elasticsearch", "Neo4j",
    "ArangoDB", "Firebase", "Supabase", "Realm", "CockroachDB", "Snowflake", "BigQuery",
    "Redshift", "Hadoop", "Spark", "Hive", "Kafka", "Apache Kafka", "RabbitMQ", "ActiveMQ",
    "Pulsar", "SQS", "SNS", "Kinesis", "ZeroMQ", "NATS", "ClickHouse", "TimescaleDB",
    "InfluxDB", "ScyllaDB", "HBase", "Teradata", "Oracle DB", "DB2", "Informix", "Sybase",
    "Presto", "Trino", "Flink", "Storm", "Samza", "Beam", "Airflow", "Prefect", "Dagster",
    "dbt", "ETL", "ELT", "Data Lake", "Data Warehouse",
    "DuckDB", "Parquet", "Avro", "ORC", "Arrow", "Dremio", "Druid", "Pinot", "Kylin",
    "Vertica", "Greenplum", "Netezza", "Exasol", "SingleStore", "TiDB", "YugabyteDB",
    "FoundationDB", "RethinkDB", "RavenDB", "OrientDB", "JanusGraph", "TigerGraph",
    "FaunaDB", "SurrealDB", "MeiliSearch", "Typesense", "Solr", "Lucene", "Algolia",
    "Vector Database", "Pinecone", "Milvus", "Weaviate", "Chroma", "Qdrant",

    # --- DevOps, Cloud & Infrastructure ---
    "AWS", "Amazon Web Services", "Azure", "Google Cloud", "GCP", "Digital Ocean", "Heroku",
    "Vercel", "Netlify", "Linode", "Cloudflare", "Akamai", "Docker", "Kubernetes", "K8s",
    "Terraform", "Ansible", "Chef", "Puppet", "Vagrant", "Jenkins", "CircleCI", "Travis CI",
    "GitLab CI", "GitHub Actions", "ArgoCD", "Bamboo", "TeamCity", "Prometheus", "Grafana",
    "ELK Stack", "Splunk", "Datadog", "New Relic", "PagerDuty", "Nginx", "Apache", "HAProxy",
    "Envoy", "Istio", "Linkerd", "Linux", "Ubuntu", "Debian", "CentOS", "Red Hat", "Fedora",
    "Arch Linux", "Alpine", "Windows Server", "VirtualBox", "VMware", "OpenStack", "Openshift",
    "Rancher", "Nomad", "Consul", "Vault", "Packer", "Pulumi", "Crossplane", "Helm", "Kustomize",
    "Flux", "Tekton", "Spinnaker", "Nagios", "Zabbix", "Sentry", "Logstash", "Kibana", "Fluentd",
    "Podman", "LXC", "LXD", "Mesos", "Marathon", "SaltStack", "Fabric", "Capistrano",
    "Waypoint", "Bosh", "CloudFoundry", "AppEngine", "Lambda", "Fargate", "ECS", "EKS",
    "AKS", "GKE", "Serverless Framework", "SAM", "CDK", "CloudFormation", "Bicep",
    "Traefik", "Caddy", "Kong", "Tyk", "Ambassador", "Contour", "Gloo", "Cilium",
    "Calico", "Flannel", "Weave Net", "CoreDNS", "Etcd", "ZooKeeper", "Thanপরেos",
    "Cortex", "VictoriaMetrics", "Loki", "Tempo", "Jaeger", "Zipkin", "OpenTelemetry",
    "Checkmk", "Icinga", "Netdata", "Glances", "Htop", "Strace", "Tcpdump",

    # --- Testing & QA ---
    "Jest", "Mocha", "Chai", "Cypress", "Puppeteer", "Playwright", "Selenium", "TestNG",
    "JUnit", "PyTest", "RSpec", "Cucumber", "Appium", "Karma", "Jasmine", "Enzyme",
    "Testing Library", "Vitest", "K6", "JMeter", "Gatling", "SonarQube", "Espresso", "XCTest",
    "Detox", "Robot Framework", "Sauce Labs", "BrowserStack", "LoadRunner", "Locust",
    "TestCafe", "Nightwatch.js", "WebdriverIO", "Protractor", "Ava", "Tape", "QUnit",
    "Sinon", "Nock", "MSW", "WireMock", "Mountebank", "Postman Collections", "Newman",
    "Allure", "ReportPortal", "TestRail", "Zephyr", "Xray", "Coveralls", "Codecov",
    "Hypothesis", "Property-based Testing", "Fuzz Testing", "Chaos Monkey", "Gremlin",

    # --- Web3 & Blockchain ---
    "Web3.js", "Ethers.js", "Wagmi", "Viem", "Hardhat", "Truffle", "Foundry", "Ganache",
    "Ethereum", "Solana", "Polygon", "Arbitrum", "Optimism", "Binance Smart Chain",
    "Smart Contracts", "DeFi", "NFT", "DAO", "IPFS", "Filecoin", "Chainlink", "The Graph",
    "Privy", "RainbowKit", "WalletConnect", "Metamask", "Phantom", "Gnosis Safe",
    "Jupiter", "Uniswap", "GMX", "Aave", "Compound", "Curve", "Hyperliquid",
    "Coingecko", "BirdEye", "DexScreener", "ERC-20", "ERC-721", "ERC-1155",
    "Cosmos", "Polkadot", "Near", "Avalanche", "Fantom", "Tezos", "Cardano", "Ripple",
    "Stellar", "Monero", "Zcash", "Algorand", "Hedera", "EVM", "Solc", "Slither", "MythX",
    "OpenZeppelin", "Alchemy", "Infura", "Moralis", "Tenderly", "Dune Analytics",
    "Rust (Solana)", "Anchor", "Sealevel", "Move", "Aptos", "Sui", "Cairo", "StarkNet",
    "ZkSync", "Hermez", "Loopring", "Immutable X", "Mina", "Celestia", "EigenLayer",
    "Lens Protocol", "Farcaster", "Arweave", "Thorchain", "CosmWasm", "Substrate",
    "Ink!", "Clarity", "Cadence", "Flow", "Hyperledger", "Fabric", "Corda", "Quorum",

    # --- Architecture & Concepts ---
    "REST", "RESTful", "GraphQL", "Apollo", "gRPC", "Protobuf", "TRPC", "Socket.io",
    "WebSockets", "Microservices", "Serverless", "Monolith", "Event-Driven", "TDD", "BDD",
    "CI/CD", "OOP", "FP", "MVC", "MVVM", "SOLID", "DRY", "KISS", "YAGNI", "Agile", "Scrum",
    "Kanban", "Waterfall", "DevOps", "GitOps", "Infrastructure as Code", "IaC", "OAuth",
    "OAuth2", "OIDC", "JWT", "SAML", "LDAP", "SSO", "HTTPS", "SSL", "TLS", "SSH", "Cors",
    "PWA", "SPA", "SSR", "SSG", "ISR", "Jamstack", "12-Factor App", "Clean Architecture",
    "Hexagonal Architecture", "Domain-Driven Design", "DDD", "CQRS", "Event Sourcing",
    "Actor Model", "Reactive Programming", "Functional Reactive Programming", "FRP",
    "Design Patterns", "Singleton", "Factory", "Observer", "Strategy", "Decorator",
    "Adapter", "Facade", "Proxy", "Command", "Iterator", "Template Method",
    "Visitor", "Composite", "Bridge", "Flyweight", "Chain of Responsibility", "Mediator",
    "Memento", "Interpreter", "Anti-patterns", "Code Smells", "Technical Debt",
    "Refactoring", "Pair Programming", "Mob Programming", "Code Review", "Static Analysis",
    "Dynamic Analysis", "Profiling", "Benchmarking", "Optimization", "Scalability",
    "High Availability", "Fault Tolerance", "Disaster Recovery", "CAP Theorem", "ACID",
    "Sharding", "Replication", "Partitioning", "Caching", "Load Balancing",
    "Rate Limiting", "Throttling", "Circuit Breaker", "Bulkhead",
    "Idempotency", "Consistency", "Availability", "Partition Tolerance",

    # --- Tools & IDEs ---
    "Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Confluence", "Trello", "Asana", "Notion",
    "Slack", "Discord", "Zoom", "Teams", "Figma", "Sketch", "Adobe XD", "Postman", "Insomnia",
    "Swagger", "OpenAPI", "VS Code", "Visual Studio Code", "IntelliJ IDEA", "WebStorm",
    "PyCharm", "Eclipse", "NetBeans", "Android Studio", "Xcode", "Vim", "Neovim", "Emacs",
    "Nano", "Maven", "Gradle", "Ant", "Yarn", "NPM", "PNPM", "Pip", "Homebrew", "Chocolatey",
    "Scoop", "Apt", "Yum", "Pacman", "Make", "CMake", "Bazel", "Ninja",
    "Rider", "GoLand", "CLion", "RubyMine", "PhpStorm", "DataGrip", "AppCode",
    "Sublime Text", "Atom", "Notepad++", "TextMate", "Kakoune", "Helix", "Micro",
    "Tmux", "Zsh", "Fish", "Oh My Zsh", "Starship", "Direnv", "Nix", "NixOS", "Guix",
    "Asdf", "Nvm", "Rbenv", "Pyenv", "SDKMAN", "Volta", "Fnm", "Corepack",
    "Husky", "Lint-staged", "Commitizen", "Semantic Release", "Standard Version",
    "Lerna", "Nx", "Turborepo", "Rush", "Pants", "Buck", "Please", "Taskfile",
    "Just", "Rake", "Invoke", "Gulp", "Grunt", "Yeoman", "Cookiecutter",

    # --- Security ---
    "OWASP", "Penetration Testing", "Metasploit", "Burp Suite", "Wireshark", "Nmap", "Kali Linux",
    "Snort", "Suricata", "Osquery", "Wazuh", "CrowdStrike", "Splunk ES", "Sentinel",
    "ZAP", "Nessus", "Qualys", "OpenVAS", "ClamAV", "Yara", "Zeek", "Bro",
    "ModSecurity", "Fail2Ban", "UFW", "Iptables", "Firewalld", "SELinux", "AppArmor",
    "GPG", "PGP", "OpenSSL", "BoringSSL", "LibreSSL", "Keybase", "1Password", "LastPass",
    "Bitwarden", "Vaultwarden", "KeePass", "KeePassXC", "Authy", "Google Authenticator",
    "YubiKey", "Duo", "Okta", "Auth0", "Cognito", "Firebase Auth", "Clerk", "Supabase Auth",
    "Magic Link", "WebAuthn", "FIDO", "FIDO2", "Passkeys", "RBAC", "ABAC", "PBAC",
    "XSS", "CSRF", "SQL Injection", "RCE", "SSRF", "XXE", "IDOR", "Clickjacking",
    "Man-in-the-Middle", "Phishing", "Social Engineering", "Ransomware", "Malware",
    "Rootkit", "Bootkit", "Spyware", "Adware", "Trojan", "Worm", "Virus", "Botnet",
    "DDoS", "Zero-day", "Exploit", "Payload", "Shellcode", "Reverse Engineering",
    "Forensics", "Incident Response", "Threat Hunting", "Threat Intelligence",

    # --- AI & ML ---
    "OpenAI", "ChatGPT", "GPT-3", "GPT-4", "Claude", "Gemini", "LLM", "LangChain",
    "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy", "SciPy",
    "Jupyter Notebook", "Hugging Face", "Copilot", "Midjourney", "Stable Diffusion",
    "XGBoost", "LightGBM", "CatBoost", "OpenCV", "NLTK", "Spacy", "Gensim", "FastAI",
    "LlamaIndex", "AutoGPT", "BabyAGI", "Pinecone", "ChromaDB", "Weaviate", "Milvus",
    "Qdrant", "DeepSpeed", "Ray", "Horovod", "ONNX", "TensorRT", "OpenVINO",
    "CoreML", "TFLite", "TFX", "MLflow", "Kubeflow", "Seldon", "BentoML", "Cortex",
    "Streamlit", "Gradio", "Dash", "Shiny", "Bokeh", "Plotly", "Matplotlib", "Seaborn",
    "Altair", "Folium", "Pydeck", "Kepler.gl", "FiftyOne", "Label Studio", "Prodigy",
    "Roboflow", "YOLO", "R-CNN", "Mask R-CNN", "Faster R-CNN", "SSD", "RetinaNet",
    "EfficientNet", "ResNet", "VGG", "Inception", "MobileNet", "Transformer", "BERT",
    "RoBERTa", "DistilBERT", "ALBERT", "T5", "GPT-2", "Bloom", "Falcon", "Llama",
    "Mistral", "Vicuna", "Guanaco", "WizardLM", "Orca", "Phi", "Qwen", "Yi"
], key=len, reverse=True)


# =============================================================================
# DEFAULT MOCK DATA
# =============================================================================

DEFAULT_CONTENT = {
    "name": "John Doe",
    "contact_info": {
        "phone": "+1 555-0123-456",
        "email": "john.doe@example.com",
        "linkedin_url": "https://www.linkedin.com/in/johndoe-fake/",
        "github_url": "https://github.com/johndoe-fake"
    },
    "summary": [
        {
            "text": (
                "<b>Senior Full-Stack Engineer</b> with 8+ years of experience building scalable web applications. "
                "Expert in modern JavaScript ecosystems (React, Node.js) and cloud-native architectures. "
                "Proven ability to lead teams, design RESTful APIs, and optimize frontend performance."
            ),
            "target_audiences": ["fullstack", "frontend", "backend"]
        },
        {
            "text": (
                "<b>DevOps & Site Reliability Engineer</b> passionate about automation and infrastructure as code. "
                "Specialized in Kubernetes, AWS, and CI/CD pipelines. Experienced in scaling high-traffic systems "
                "and ensuring 99.99% availability through robust monitoring and security practices."
            ),
            "target_audiences": ["devops", "backend"]
        }
    ],
    "skills": [
        {
            "text": (
                "<b>Languages:</b> JavaScript (ES6+), TypeScript, Python, Go, Bash<br/>"
                "<b>Frontend:</b> React, Next.js, Redux, Tailwind CSS, HTML5/CSS3<br/>"
                "<b>Backend:</b> Node.js, Express.js, Django, PostgreSQL, Redis, MongoDB<br/>"
                "<b>DevOps:</b> Docker, Kubernetes, AWS, Terraform, Jenkins, GitHub Actions, Prometheus"
            ),
            "target_audiences": ["fullstack", "backend", "devops"]
        },
        {
            "text": (
                "<b>Languages:</b> JavaScript, TypeScript, HTML5, CSS3<br/>"
                "<b>Frontend:</b> React, Vue.js, Next.js, Webpack, Babel, Sass, Jest, Cypress<br/>"
                "<b>UI/UX:</b> Figma, Material-UI, Styled-Components, Accessibility (WCAG)"
            ),
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
                },
                {
                    "text": "Designed and deployed a serverless data processing pipeline on AWS Lambda to handle real-time analytics.",
                    "target_audiences": ["backend", "devops", "fullstack"]
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
                },
                {
                    "text": "Containerized application services using Docker and orchestrated deployments on an on-premise Kubernetes cluster.",
                    "target_audiences": ["devops", "backend"]
                }
            ]
        },
        {
            "title": "Junior Web Developer",
            "company": "Creative Code Studio",
            "dates": "Aug 2017 – May 2019",
            "intro": "",
            "bullets": [
                {
                    "text": "Collaborated with designers to implement pixel-perfect landing pages using HTML5, CSS3, and JavaScript.",
                    "target_audiences": ["frontend", "fullstack"]
                },
                {
                    "text": "Assisted in backend development tasks using PHP (Laravel) and MySQL for client CMS projects.",
                    "target_audiences": ["backend", "fullstack"]
                },
                {
                    "text": "Automated server provisioning and configuration management using Ansible scripts.",
                    "target_audiences": ["devops", "backend"]
                }
            ]
        }
    ],
    "education": "<b>B.Sc. in Computer Science</b>, University of Technology · 2013–2017",
    "languages": "English – Native | Spanish – Fluent"
}

# =============================================================================
# VALIDATION HELPER FUNCTIONS
# =============================================================================

def validate_json_structure(data):
    """
    Validates that the loaded JSON matches the expected structure and types.
    Returns (True, None) if valid, or (False, error_message) if invalid.
    """
    errors = []

    if not isinstance(data, dict):
        return False, "Root element must be a dictionary (object)."

    # 1. Validate top-level required keys
    required_keys = ["name", "contact_info", "summary", "skills", "experience", "education", "languages"]
    for key in required_keys:
        if key not in data:
            errors.append(f"Missing required top-level key: '{key}'")

    if errors:
        return False, "\n".join(errors)

    # 2. Validate Contact Info
    c_info = data.get("contact_info")
    if not isinstance(c_info, dict):
        errors.append("'contact_info' must be a dictionary.")
    else:
        if not isinstance(c_info.get("phone"), str):
            errors.append("'contact_info.phone' must be a string.")
        if not isinstance(c_info.get("email"), str):
            errors.append("'contact_info.email' must be a string.")

        # Optional URL fields
        if "linkedin_url" in c_info and not isinstance(c_info["linkedin_url"], str):
             errors.append("'contact_info.linkedin_url' must be a string.")
        if "github_url" in c_info and not isinstance(c_info["github_url"], str):
             errors.append("'contact_info.github_url' must be a string.")

    # 3. Validate Summary
    summary = data.get("summary")
    if not isinstance(summary, list):
        errors.append("'summary' must be a list.")
    else:
        for idx, item in enumerate(summary):
            if not isinstance(item, dict):
                errors.append(f"Summary item #{idx} must be a dictionary.")
                continue
            if "text" not in item:
                errors.append(f"Summary item #{idx} missing 'text'.")
            if "target_audiences" in item and not isinstance(item["target_audiences"], list):
                errors.append(f"Summary item #{idx} 'target_audiences' must be a list of strings.")

    # 4. Validate Skills
    skills = data.get("skills")
    if not isinstance(skills, list):
        errors.append("'skills' must be a list.")
    else:
        for idx, item in enumerate(skills):
            if not isinstance(item, dict):
                errors.append(f"Skills item #{idx} must be a dictionary.")
                continue
            if "text" not in item:
                errors.append(f"Skills item #{idx} missing 'text'.")
            if "target_audiences" in item and not isinstance(item["target_audiences"], list):
                errors.append(f"Skills item #{idx} 'target_audiences' must be a list of strings.")

    # 5. Validate Experience
    experience = data.get("experience")
    if not isinstance(experience, list):
        errors.append("'experience' must be a list.")
    else:
        for idx, job in enumerate(experience):
            if not isinstance(job, dict):
                errors.append(f"Experience item #{idx} must be a dictionary.")
                continue
            required_job_keys = ["title", "company", "dates", "bullets"]
            for k in required_job_keys:
                if k not in job:
                    errors.append(f"Experience item #{idx} missing key '{k}'.")

            # Validate bullets
            bullets = job.get("bullets", [])
            if not isinstance(bullets, list):
                errors.append(f"Experience item #{idx} 'bullets' must be a list.")
            else:
                for b_idx, bullet in enumerate(bullets):
                    if not isinstance(bullet, dict):
                        errors.append(f"Experience item #{idx} bullet #{b_idx} must be a dictionary.")
                        continue
                    if "text" not in bullet:
                        errors.append(f"Experience item #{idx} bullet #{b_idx} missing 'text'.")
                    if "target_audiences" in bullet and not isinstance(bullet["target_audiences"], list):
                        errors.append(f"Experience item #{idx} bullet #{b_idx} 'target_audiences' must be a list.")

            # Validate optional intro
            if "intro" in job and not isinstance(job["intro"], str):
                errors.append(f"Experience item #{idx} 'intro' must be a string.")

    if errors:
        return False, "\n".join(errors)

    return True, None

def collect_all_audiences(data):
    """
    Scans the JSON data to find all unique strings used in 'target_audiences'.
    Returns a set of audience strings (e.g., {'web2', 'web3', 'ios'}).
    """
    audiences = set()

    def scan_list(items):
        for item in items:
            if isinstance(item, dict):
                if "target_audiences" in item and isinstance(item["target_audiences"], list):
                    for aud in item["target_audiences"]:
                        audiences.add(aud)

    # Scan Summary
    scan_list(data.get("summary", []))
    # Scan Skills
    scan_list(data.get("skills", []))
    # Scan Experience Bullets
    for job in data.get("experience", []):
        scan_list(job.get("bullets", []))

    return audiences

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def load_content():
    """
    Load content from content.json.
    If missing, create it. If present, validate it.
    """
    if not os.path.exists(JSON_FILENAME):
        print(f"⚠ {JSON_FILENAME} not found. Creating template file...")
        with open(JSON_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONTENT, f, indent=4)
        print(f"✓ Created {JSON_FILENAME}. Using template data.")
        return DEFAULT_CONTENT
    else:
        print(f"✓ Found {JSON_FILENAME}. Loading data...")
        try:
            with open(JSON_FILENAME, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate
            is_valid, error_msg = validate_json_structure(data)
            if not is_valid:
                print("\n❌ DATA VALIDATION FAILED:")
                print(error_msg)
                print("\nPlease fix 'content.json' and try again.")
                exit(1)

            print("✓ Data validation passed.")
            return data

        except json.JSONDecodeError as e:
            print(f"❌ Error decoding JSON: {e}")
            exit(1)

def format_text_with_bold_tech(text):
    """
    Bold technical terms using Regex to handle punctuation.
    """
    terms = sorted(TECH_TERMS, key=len, reverse=True)

    for term in terms:
        escaped_term = re.escape(term)
        # Matches term if NOT already surrounded by bold tags, and NOT part of another word.
        pattern = r"(<b>" + escaped_term + r"</b>)|((?<![a-zA-Z0-9])" + escaped_term + r"(?![a-zA-Z0-9]))"

        def replace_func(match):
            if match.group(1): return match.group(1)
            return f"<b>{match.group(2)}</b>"

        text = re.sub(pattern, replace_func, text, flags=re.IGNORECASE)

    return text

def filter_content(items, target_audience):
    """
    Filter list items based on target_audience.
    Item is kept if:
    1. It has NO 'target_audiences' key (implies universal).
    2. 'target_audiences' is empty (implies universal).
    3. 'target_audience' is present in the item's 'target_audiences' list.
    """
    filtered = []
    for item in items:
        audiences = item.get("target_audiences", [])

        # Universal content (no specific target defined)
        if not audiences:
            filtered.append(item)
            continue

        # Targeted content
        if target_audience in audiences:
            filtered.append(item)

    return filtered

def create_pdf(filename, content, target_audience):
    """Generate PDF resume for a specific target audience."""

    # Extract Contact Info logic
    c_info = content.get("contact_info", {})

    phone = c_info.get("phone", "")
    email = c_info.get("email", "")

    # Build contact parts list
    contact_parts = []
    if phone:
        contact_parts.append(phone)
    if email:
        contact_parts.append(email)

    # Optional URLs
    linkedin = c_info.get("linkedin_url", "").strip()
    if linkedin:
        contact_parts.append(f"<a href='{linkedin}' color='#005b96'>LinkedIn</a>")

    github = c_info.get("github_url", "").strip()
    if github:
        contact_parts.append(f"<a href='{github}' color='#005b96'>GitHub</a>")

    current_contact_info = " | ".join(contact_parts)
    name = content.get("name", "Unknown Name")

    doc = SimpleDocTemplate(
        filename,
        pagesize=LETTER,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.4*inch,
        bottomMargin=0.4*inch
    )

    styles = getSampleStyleSheet()

    style_name = ParagraphStyle(
        'NameTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.HexColor("#2C3E50"),
        leading=28,
        spaceAfter=4
    )

    style_contact = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor("#7F8C8D"),
        alignment=TA_RIGHT,
        leading=12
    )

    style_section = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.HexColor("#2C3E50"),
        spaceBefore=6,
        spaceAfter=2
    )

    style_body = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
        leftIndent=0,
        firstLineIndent=0,
        spaceAfter=4
    )

    style_bullet = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        leftIndent=16,
        firstLineIndent=-10,
        spaceAfter=2
    )

    story = []

    # Header
    header_data = [[Paragraph(name, style_name), Paragraph(current_contact_info, style_contact)]]
    t_header = Table(header_data, colWidths=[3.5*inch, 4.0*inch])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_header)

    story.append(Spacer(1, 2))

    # Summary
    summary_items = filter_content(content.get("summary", []), target_audience)
    if summary_items:
        formatted_summary = format_text_with_bold_tech(summary_items[0]["text"])
        story.append(Paragraph(formatted_summary, style_body))
        story.append(Spacer(1, 1))

    # Skills
    story.append(Paragraph("TECHNICAL SKILLS", style_section))
    t_line = Table([[""]], colWidths=[7.5*inch], rowHeights=1)
    t_line.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,-1), 1, colors.HexColor("#BDC3C7"))]))
    story.append(t_line)
    story.append(Spacer(1, 2))

    skills_items = filter_content(content.get("skills", []), target_audience)
    if skills_items:
        story.append(Paragraph(skills_items[0]["text"], style_body))

    story.append(Spacer(1, 1))

    # Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", style_section))
    story.append(t_line)
    story.append(Spacer(1, 2))

    for job in content.get("experience", []):
        filtered_bullets = filter_content(job.get("bullets", []), target_audience)
        if not filtered_bullets:
            continue

        title_text = f"<font name='Helvetica-Bold' size=11>{job['title']}</font> | <font color='#555555'>{job['company']}</font>"
        date_text = f"<font color='#555555'>{job['dates']}</font>"

        row_data = [[
            Paragraph(title_text, style_body),
            Paragraph(date_text, ParagraphStyle('DateRight', parent=style_body, alignment=TA_RIGHT))
        ]]
        t_job = Table(row_data, colWidths=[5.5*inch, 2.0*inch], hAlign='LEFT')
        t_job.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(t_job)

        # Optional Intro
        if "intro" in job and job["intro"].strip():
            formatted_intro = format_text_with_bold_tech(job["intro"])
            story.append(Paragraph(formatted_intro, style_body))
            story.append(Spacer(1, 2))

        for bullet in filtered_bullets:
            formatted_bullet = format_text_with_bold_tech(bullet["text"])
            story.append(Paragraph(f"•&nbsp;&nbsp;{formatted_bullet}", style_bullet))

        story.append(Spacer(1, 2))

    # Education
    story.append(Paragraph("EDUCATION", style_section))
    story.append(t_line)
    story.append(Spacer(1, 2))
    story.append(Paragraph(content.get("education", ""), style_body))

    # Languages
    story.append(Paragraph("LANGUAGES", style_section))
    story.append(t_line)
    story.append(Spacer(1, 2))
    story.append(Paragraph(content.get("languages", ""), style_body))

    doc.build(story)
    print(f"✓ Generated: {filename}")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # 1. Load Data
    data = load_content()

    # 2. Identify all unique audiences
    audiences = collect_all_audiences(data)
    if not audiences:
        print("⚠ No specific audiences found (e.g. 'fullstack', 'backend'). Generating a generic 'General' resume.")
        audiences = {"General"}
    else:
        print(f"✓ Found target audiences: {', '.join(audiences)}")

    # 3. Generate Filenames
    today_str = datetime.now().strftime("%Y_%b_%d")

    # Snake case the name for filename (e.g., "John Doe" -> "John_Doe")
    raw_name = data.get("name", "Resume")
    snake_name = raw_name.replace(" ", "_")

    # 4. Loop through every audience found and create a resume
    print("\n--- Generating PDFs ---")
    for audience in audiences:
        clean_audience = audience.capitalize().replace(" ", "_")
        filename = f"{snake_name}_CV_{clean_audience}_{today_str}.pdf"
        create_pdf(filename, data, target_audience=audience)

    print("\n✓ All resumes generated successfully!")
