from setuptools import setup, find_packages

setup(
    name="clinical-intervention-system",
    version="1.0.0",
    description="Sistema de registro individual de intervenciones clínicas",
    author="Clinical Team",
    author_email="clinical@example.com",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "sqlalchemy==2.0.23",
        "psycopg2-binary==2.9.9",
        "pymongo==4.6.0",
        "python-multipart==0.0.6",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "openai==1.3.7",
        "python-dotenv==1.0.0",
        "alembic==1.13.1"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
