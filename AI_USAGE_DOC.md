## AI Usage Documentation
# AI Tool Used

Google Gemini

The AI assistance was used as an engineering support tool during development of this MLOps project.

Gemini Conversation

The development conversation can be reviewed here:

https://share.gemini.google/9Cu5W7F2jDie

Purpose of AI Assistance

Gemini was used selectively to accelerate development and troubleshooting in several areas of the project:

1. Kubernetes Configuration

Gemini assisted with generating and structuring boilerplate Kubernetes configuration, including concepts used for:

Kubernetes Deployments
LoadBalancer Services
Horizontal Pod Autoscaling
Replica configuration
Deployment strategies

The generated configuration was subsequently reviewed and adapted to the requirements of the actual GKE environment.

2. Docker / Python Dependency Debugging

Gemini assisted in diagnosing Python dependency and binary compatibility issues encountered inside the Docker environment, particularly conflicts involving compiled dependencies such as:

NumPy
pandas
Related scientific Python packages

The recommendations were used as debugging guidance, after which dependency versions were explicitly pinned and the resulting container was tested.

3. Google Cloud Logging

Gemini assisted with the initial structure of the Python integration with Google Cloud Logging.

The resulting implementation was reviewed and adapted to the project's inference simulation and GCP deployment environment.

Human Verification

AI-generated suggestions were not treated as automatically correct or production-ready.

All relevant generated code and recommendations were manually reviewed, modified where necessary, executed, and tested by the developer in the Google Cloud Shell / GCP environment.

Verification included practical testing of:

Python execution
Model inference
Docker image construction
Kubernetes manifests
GKE deployment
API availability
Horizontal Pod Autoscaling configuration
Cloud Logging integration
Stress testing
SHAP analysis
Fairness analysis
Statistical drift detection
AI Contributions vs. Human Responsibility

AI assistance primarily accelerated:

Boilerplate generation
        +
Debugging suggestions
        +
Documentation structure
        +
Implementation ideas


The developer remained responsible for:

Architecture decisions
        +
Code review
        +
Configuration
        +
Execution
        +
Testing
        +
Debugging
        +
Cloud deployment
        +
Result interpretation
        +
Final repository contents

Important Verification Principle

AI-generated output was treated as a development aid rather than an authoritative source.

In particular, generated recommendations were validated against the behavior of the actual application and GCP environment before being incorporated into the project.

This distinction is important because AI-generated code can contain:

Incorrect assumptions
Outdated APIs
Incompatible dependency versions
Invalid Kubernetes configurations
Security weaknesses
Environment-specific failures

Therefore, successful execution and independent verification were required before accepting implementation changes.

Transparency Statement

The use of AI in this project was intended to improve development velocity and debugging efficiency while retaining human ownership of the engineering decisions and validation process.

The project should therefore be evaluated based on the implemented, tested system and its documented engineering decisions, rather than on AI assistance alone.

AI Conversation Reference

Tool: Google Gemini
Purpose: MLOps engineering assistance, debugging, Kubernetes configuration, Docker dependency troubleshooting, and GCP Cloud Logging implementation.

Conversation:
https://share.gemini.google/9Cu5W7F2jDie
