"""Portfolio content data — edit this file to customize all content."""

PERSONAL = {
    "name": "Sharath Dinesh",
    "title": "Data Analyst & FastAPI Developer",
    "tagline": "Transforming complex data into actionable insights and high-performance APIs.",
    "bio": "Specializing in building scalable backend architectures and precision-driven data pipelines.",
    "email": "work.sharathdinesh@gmail.com",
    "github": "https://github.com/sharatdinesh23",
    "linkedin": "https://www.linkedin.com/in/sharath-dinesh/",
    "location": "Remote/Mumbai",
    "contact_webhook": "", # PASTE YOUR WEBHOOK URL HERE
}

TECH_SKILLS = [
    {"name": "Python", "icon": "🐍", "level": "Expert"},
    {"name": "FastAPI", "icon": "⚡", "level": "Intermediate"},
    {"name": "PostgreSQL", "icon": "🐘", "level": "Intermediate"},
    {"name": "Pandas", "icon": "🐼", "level": "Beginer"},
    {"name": "Scikit-learn", "icon": "🤖", "level": "Beginer"},
    {"name": "Pydantic", "icon": "✅", "level": "Intermediate"},
    {"name": "Reconciliation","icon":"⚖️","level":"Expert"}

]

PROJECTS = [
    {
        "title": "E-commerce Data Pipeline",
        "description": "Built a real-time data ingestion pipeline processing 10k+ events per minute using FastAPI and PostgreSQL with automated reporting features.",
        "tags": ["FastAPI", "PostgreSQL", "Pandas", "Redis"],
        "github": "https://github.com/sharatdinesh23/ecom-pipeline",
        "demo": "#",
        "highlight": "10k+ events/min",
    },
    {
        "title": "Stock API v2",
        "description": "High-frequency financial data API built for sub-50ms response times. Serves real-time OHLCV data with WebSocket streaming.",
        "tags": ["FastAPI", "WebSockets", "PostgreSQL", "Redis"],
        "github": "https://github.com/sharatdinesh23/stock-api",
        "demo": "#",
        "highlight": "<50ms response",
    },
    {
        "title": "Customer Segmentation",
        "description": "K-Means clustering model deployed as a microservice for personalized marketing. Segments 500k+ customer records daily.",
        "tags": ["Scikit-learn", "FastAPI", "Docker", "Pandas"],
        "github": "https://github.com/sharatdinesh23/segmentation",
        "demo": "#",
        "highlight": "500k+ records/day",
    },
    {
        "title": "Automated BI Sync",
        "description": "A middleware service that synchronizes PostgreSQL production data with Tableau Server cloud instance every hour.",
        "tags": ["PostgreSQL", "Python", "Tableau", "Airflow"],
        "github": "https://github.com/sharatdinesh23/bi-sync",
        "demo": "#",
        "highlight": "Hourly sync",
    },
]

EXPERIENCE = [
    {
        "role": "Senior Data Analyst",
        "company": "Precision Layers Tech",
        "period": "2022 — Present",
        "description": "Leading the architecture of internal data APIs and optimizing SQL queries that reduced dashboard load times by 60%. Built real-time analytics pipelines serving 500k+ daily active users.",
        "achievements": ["60% faster dashboards", "500k+ daily users", "Team of 5 engineers"],
    },
    {   
        "role": "Junior Data Scientist",
        "company": "Nexus Core Solutions",
        "period": "2020 — 2022",
        "description": "Developed predictive models for customer churn and built automated Excel-to-SQL migration tools. Saved 40+ hours/week in manual reporting tasks.",
        "achievements": ["Reduced churn 15%", "40+ hrs/week saved", "ML model deployment"],
    },
]

EDUCATION = {
    "degree": "MS in Data Science",
    "school": "Tech University of Excellence",
    "period": "2018 — 2020",
    "description": "Specialized in High-Performance Computing and Statistical Learning. Graduated with Honors.",
    "thesis": "Optimizing Microservice Communication for Big Data Streams",
    "certifications": [
        {"name": "AWS Certified Solutions Architect", "issuer": "Amazon Web Services"},
        {"name": "Google Data Analytics Professional", "issuer": "Google"},
        {"name": "TensorFlow Developer Certificate", "issuer": "Google"},
    ],
}

TESTIMONIALS = [
    {
        "quote": "The FastAPI architecture built by this team handled our peak holiday traffic without a single millisecond of degradation. Truly world-class engineering.",
        "name": "Sarah Chen",
        "role": "Lead Data Scientist, FinStream",
        "avatar": "SC",
    },
    {
        "quote": "Transformed our messy legacy data into a streamlined, automated BI system. The insights we gained in the first month paid for the project twice over.",
        "name": "Marcus Knight",
        "role": "Project Manager, Nexus Core",
        "avatar": "MK",
    },
    {
        "quote": "Rare to find someone who understands both the deep mathematics of data science and the practicalities of high-performance API development.",
        "name": "Alex Rivera",
        "role": "CTO, DataLayers Tech",
        "avatar": "AR",
    },
]

BLOG_POSTS = [
    {
        "title": "Architecting Real-time Analytics with FastAPI and WebSockets",
        "description": "Dive deep into building a production-grade real-time analytics system that handles thousands of concurrent connections.",
        "date": "Mar 15, 2024",
        "read_time": "12 min read",
        "tags": ["FastAPI", "WebSockets", "Architecture"],
        "featured": True,
    },
    {
        "title": "Efficient Data Validation with Pydantic v2",
        "description": "Exploring the performance gains and new features in the latest Pydantic release for data analysts.",
        "date": "Feb 28, 2024",
        "read_time": "8 min read",
        "tags": ["Pydantic", "Python", "Validation"],
        "featured": False,
    },
    {
        "title": "Visualizing Geographic Trends with Deck.gl",
        "description": "How to render millions of data points smoothly in the browser using WebGL-powered layers.",
        "date": "Feb 10, 2024",
        "read_time": "10 min read",
        "tags": ["Visualization", "JavaScript", "Data"],
        "featured": False,
    },
    {
        "title": "Mastering Window Functions for Data Cleaning",
        "description": "Advanced SQL techniques that will save you hours of preprocessing in Python or R.",
        "date": "Jan 22, 2024",
        "read_time": "7 min read",
        "tags": ["SQL", "PostgreSQL", "Data Cleaning"],
        "featured": False,
    },
    {
        "title": "Dependency Injection: The Secret to Scalable APIs",
        "description": "Why FastAPI's dependency system is its greatest strength and how to use it for database sessions.",
        "date": "Jan 8, 2024",
        "read_time": "9 min read",
        "tags": ["FastAPI", "Python", "Architecture"],
        "featured": False,
    },
    {
        "title": "The Full-Stack Analyst: Why Back-end Skills Matter",
        "description": "Breaking the mold: How knowing how to build APIs changed my career trajectory as a data analyst.",
        "date": "Dec 20, 2023",
        "read_time": "6 min read",
        "tags": ["Career", "Python", "FastAPI"],
        "featured": False,
    },
    {
        "title": "Automating ETL Pipelines with GitHub Actions",
        "description": "Moving beyond local scripts to serverless data pipelines that run on a schedule.",
        "date": "Dec 5, 2023",
        "read_time": "11 min read",
        "tags": ["ETL", "GitHub Actions", "Automation"],
        "featured": False,
    },
]
