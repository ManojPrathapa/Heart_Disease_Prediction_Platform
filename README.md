🩺 Healthcare MLOps — Production-Grade Heart Disease Prediction Platform
<p align="center"> <strong>From ML notebook → production API → Kubernetes → CI/CD → observability → fairness → drift detection</strong> </p> <p align="center"> A cloud-native machine learning system demonstrating how a healthcare prediction model can be engineered, deployed, monitored, and continuously evaluated beyond the notebook. </p> <p align="center">







</p> <p align="center">





</p>
📌 Table of Contents
Overview
Why This Project Exists
What This Project Demonstrates
Architecture
End-to-End MLOps Lifecycle
Explainable AI
Algorithmic Fairness
Production API
Containerization
Google Cloud Deployment
Kubernetes & Autoscaling
Deployment Strategy
Load & Stress Testing
Observability
Data Drift Detection
MLOps Feedback Loop
Engineering Challenges
Repository Structure
Infrastructure
Security Roadmap
CI/CD
Getting Started
Results
Lessons Learned
Roadmap
Disclaimer
🚀 Overview
Most machine-learning projects stop at:

Train model
     ↓
Achieve accuracy
     ↓
Save .pkl file
     ↓
Done

This project focuses on what happens after the model works.

It takes a heart-disease prediction model and moves it through a production-oriented MLOps lifecycle:

┌─────────────────────────────────────────────────────────────┐
│                    HEALTHCARE ML SYSTEM                     │
└─────────────────────────────────────────────────────────────┘

       Clinical Dataset
              │
              ▼
       Model Training
              │
              ▼
       Model Artifact
              │
       ┌──────┼──────────┬─────────────┐
       ▼      ▼          ▼             ▼
     SHAP  Fairlearn  KS Drift     Evaluation
       │      │          │             │
       └──────┴──────────┴─────────────┘
                      │
                      ▼
                FastAPI API
                      │
                      ▼
               Docker Container
                      │
                      ▼
             Artifact Registry
                      │
                      ▼
               GitHub Actions
                      │
                      ▼
                    GKE
                      │
             ┌────────┴────────┐
             ▼                 ▼
       LoadBalancer            HPA
             │              1 → 3 Pods
             └────────┬────────┘
                      ▼
              Production Traffic
                      │
                      ▼
             Google Cloud Logging

The objective is not to claim that this is a hospital-ready diagnostic platform.

The objective is to demonstrate the engineering discipline required to move an ML workload from experimentation toward a repeatable, observable, scalable cloud-native system.

🎯 Why This Project Exists
Healthcare ML introduces requirements that go beyond model accuracy.

A production-oriented system needs to answer questions such as:

Can the model be served reliably?
Can it handle increased traffic?
Can deployments be automated?
Can model decisions be investigated?
Can demographic disparities be measured?
Can changes in incoming data be detected?
Can inference activity be observed?
What happens when infrastructure reaches its limits?
Can the environment be reproduced from source control?
What happens after the model is deployed?
This repository explores those questions through a deliberately small but complete MLOps architecture.

🧠 Engineering Philosophy
A model is not a production system.
A production ML system is the combination of:

                 ┌──────────────┐
                 │    Model     │
                 └──────┬───────┘
                        │
              ┌─────────▼─────────┐
              │       Data        │
              └─────────┬─────────┘
                        │
              ┌─────────▼─────────┐
              │        API        │
              └─────────┬─────────┘
                        │
              ┌─────────▼─────────┐
              │    Container      │
              └─────────┬─────────┘
                        │
              ┌─────────▼─────────┐
              │  Infrastructure   │
              └─────────┬─────────┘
                        │
              ┌─────────▼─────────┐
              │      CI/CD        │
              └─────────┬─────────┘
                        │
              ┌─────────▼─────────┐
              │  Observability    │
              └─────────┬─────────┘
                        │
              ┌─────────▼─────────┐
              │ Responsible AI    │
              └─────────┬─────────┘
                        │
              ┌─────────▼─────────┐
              │   Governance      │
              └───────────────────┘

The project intentionally explores each layer.

🏗️ Architecture
High-Level Architecture
                              ┌─────────────────┐
                              │     GitHub      │
                              │   Source Code   │
                              └────────┬────────┘
                                       │
                                  git push
                                       │
                                       ▼
                              ┌─────────────────┐
                              │ GitHub Actions  │
                              │     CI / CD     │
                              └────────┬────────┘
                                       │
                              Build + Authenticate
                                       │
                                       ▼
                              ┌─────────────────┐
                              │ Docker Image    │
                              │ FastAPI + Model │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │ Artifact        │
                              │ Registry        │
                              └────────┬────────┘
                                       │
                                       ▼
                    ┌───────────────────────────────────┐
                    │                GKE                │
                    │                                   │
                    │     ┌────────────────────────┐    │
                    │     │ Kubernetes LoadBalancer │    │
                    │     └────────────┬───────────┘    │
                    │                  │                │
                    │          ┌───────┴───────┐        │
                    │          ▼               ▼        │
                    │     ┌──────────┐    ┌──────────┐ │
                    │     │ FastAPI  │    │ FastAPI  │ │
                    │     │   Pod    │    │   Pod    │ │
                    │     └────┬─────┘    └────┬─────┘ │
                    │          │               │        │
                    │          └───────┬───────┘        │
                    │                  │                │
                    │             Kubernetes HPA        │
                    │                  │                │
                    └──────────────────┼────────────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │ Google Cloud    │
                              │    Logging      │
                              └─────────────────┘

🔄 End-to-End MLOps Lifecycle
1. Model Development
The training pipeline generates the model artifact from the clinical dataset.

data.csv
   │
   ▼
train.py
   │
   ├── Load data
   ├── Prepare features
   ├── Train model
   └── Serialize artifact
          │
          ▼
    Model Artifact

The resulting artifact becomes the deployable ML component of the API.

2. Model Analysis
Before deployment, the model is evaluated from multiple perspectives:

                    Model
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
      SHAP         Fairlearn      Drift
  Explainability    Fairness     Detection

This moves evaluation beyond a single accuracy metric.

🔍 Explainable AI with SHAP
Black-box behavior introduces additional risk in high-impact domains.

This project therefore includes a dedicated explainability stage using SHAP — SHapley Additive exPlanations.

                 Trained Model
                      │
                      ▼
                    SHAP
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
     Feature       Model       Decision
  Contributions   Behavior   Investigation

The analysis identified features such as:

fbs
restecg
trestbps
as having relatively low impact on the current model's predictive thresholds.

⚠️ Important Interpretation
This does not mean these clinical variables are medically unimportant.

It means that, for this particular trained model and evaluated dataset, their contribution to the model's predictions was comparatively low.

That distinction is critical when communicating machine-learning results in healthcare.

⚖️ Algorithmic Fairness
The project includes demographic fairness analysis using Fairlearn.

The continuous age feature was divided into cohorts:

Age
 │
 ├── Young
 │
 ├── Middle
 │
 └── Senior

The analysis measured differences in positive prediction rates between these groups.

Observed Result
Maximum demographic parity difference: 0.0000

On the evaluated dataset, the measured positive prediction rates were equal across the tested age cohorts.

What does 0.0000 mean?
It means:

No measured demographic-parity difference was observed across the evaluated age cohorts on this dataset.

What it does NOT mean
It does not prove that the model is universally fair.

Fairness analysis depends on:

Dataset composition
Cohort definitions
Sample size
Protected attributes
Metric selection
Decision threshold
Population shift
Therefore, the result should be interpreted as an evaluation finding, not as a claim that the model is "bias-free."

⚡ Production API
The trained model is exposed through a lightweight FastAPI inference service.

The request lifecycle is:

HTTP Request
     │
     ▼
┌───────────────┐
│    FastAPI    │
└───────┬───────┘
        │
        ▼
Input Validation
        │
        ▼
Feature Preparation
        │
        ▼
   ML Model
        │
        ▼
  Prediction
        │
        ▼
JSON Response

This separates the model from the client application and provides a clean HTTP interface for inference.

🐳 Containerization
The API and model artifacts are packaged into a Docker image.

Docker Image
│
├── Python Runtime
├── Dependencies
├── FastAPI Application
├── ML Model
└── Runtime Configuration

Containerization provides:

Reproducible runtime environments
Dependency isolation
Consistent local/cloud execution
Portable deployments
Simplified infrastructure management
☁️ Google Cloud Deployment
The cloud deployment uses Google Cloud Platform.

Layer	Technology
Cloud Provider	Google Cloud Platform
Kubernetes	Google Kubernetes Engine
Container Registry	Google Artifact Registry
API	FastAPI
Container Runtime	Docker
Autoscaling	Kubernetes HPA
Logging	Google Cloud Logging
CI/CD	GitHub Actions

☸️ Kubernetes & Autoscaling
The Kubernetes deployment consists of:

                  LoadBalancer
                       │
                       ▼
                 Kubernetes
                  Service
                       │
              ┌────────┴────────┐
              ▼                 ▼
          FastAPI Pod       FastAPI Pod
              │                 │
              └────────┬────────┘
                       │
                       ▼
                      HPA
                       │
                 1 → 3 Pods

Autoscaling Configuration
Setting	Value
Minimum replicas	1
Maximum replicas	3
CPU target	50%
Scaling mechanism	Horizontal Pod Autoscaler

This provides a basic horizontal scaling mechanism for CPU-driven workloads.

🔁 Deployment Strategy
The Kubernetes deployment uses:

strategy:
  type: Recreate

instead of the default RollingUpdate.

Why Recreate?
The target GKE environment uses constrained resources.

During testing, rolling replacement could create scheduling pressure because old and new pods temporarily competed for limited cluster resources.

The Recreate strategy ensures:

Terminate old workload
        ↓
Release resources
        ↓
Schedule new workload

Trade-off
The advantage is predictable resource usage.

The disadvantage is a potential temporary availability gap during deployment.

For a larger production cluster, a more sophisticated deployment strategy would generally be preferable:

Rolling deployments
Readiness probes
Multiple replicas
PodDisruptionBudgets
Resource requests/limits
Canary releases
Blue/green deployments
Progressive delivery
The use of Recreate is therefore an intentional environment-specific trade-off.

📈 Load & Stress Testing
The API was stress-tested using wrk.

Observed Test
Metric	Result
Concurrent connections	~2,050
Average latency	~1.22 s
Infrastructure	GKE e2-small

Under extreme concurrency, the constrained infrastructure eventually reached socket/resource limitations.

The purpose of this experiment was not to claim a universal production throughput benchmark.

Instead, it was used to investigate:

API resilience
Kubernetes behavior
Resource exhaustion
Failure characteristics
Infrastructure bottlenecks
Application behavior under pressure
Engineering Takeaway
Application performance and infrastructure capacity are separate problems.

The experiment demonstrated that the underlying compute environment can become the limiting factor even when the application itself remains operational.

📊 Observability & Audit Logging
A production ML service needs visibility after deployment.

This project integrates Google Cloud Logging through the Python client.

The prediction simulator sends inference requests to the live GKE endpoint.

Structured information can be captured for operational analysis:

{
  "timestamp": "...",
  "features": "...",
  "prediction": "..."
}

The observability flow is:

Client
  │
  ▼
GKE API
  │
  ▼
Prediction
  │
  ▼
Structured Log
  │
  ▼
Google Cloud Logging
  │
  ▼
Logs Explorer

Why This Matters
Observability makes it possible to investigate:

Request behavior
Prediction activity
Application failures
Deployment issues
Unexpected traffic
Model behavior over time
🔐 Healthcare Logging Considerations
In a real healthcare production environment, raw clinical payloads should not simply be logged without appropriate controls.

A production implementation should consider:

Data minimization
PHI/PII redaction
Encryption
IAM
Retention policies
Access auditing
Least-privilege service accounts
Regulatory requirements
This project demonstrates the technical observability pattern, not regulatory certification.

📉 Data Drift Detection
A deployed ML model can degrade even when the application code remains unchanged.

Why?

Because real-world data changes.

This project implements statistical drift detection using the Kolmogorov-Smirnov two-sample test.

          Training Distribution
                    │
                    ▼
               ┌─────────┐
               │ KS Test │
               └────┬────┘
                    ▲
                    │
          Live Inference Data

The detector compares:

Baseline Training Distribution
              VS
Live Inference Distribution

using:

scipy.stats.ks_2samp

The configured statistical threshold is:

α = 0.05

A sufficiently low p-value can trigger a drift signal.

Why Drift Detection Matters
Distribution changes can occur because:

Patient populations change
Data collection processes change
Sensors or devices change
Clinical workflows change
Feature distributions shift
Therefore:

Model deployment is not the end of the ML lifecycle.

🔬 MLOps Feedback Loop
The complete system can be viewed as a continuous feedback loop:

                    ┌──────────────────┐
                    │  Training Data   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Model Training   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Model Artifact   │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
          ┌────────┐    ┌──────────┐   ┌─────────┐
          │  SHAP  │    │ Fairlearn│   │   KS    │
          │  XAI   │    │ Fairness │   │  Drift  │
          └────┬───┘    └────┬─────┘   └────┬────┘
               │             │              │
               └─────────────┼──────────────┘
                             ▼
                    ┌──────────────────┐
                    │    Deployment    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     GKE API      │
                    └────────┬─────────┘
                             │
                  ┌──────────┼──────────┐
                  ▼          ▼          ▼
              Traffic     Logging   Predictions
                  │          │          │
                  └──────────┼──────────┘
                             ▼
                    ┌──────────────────┐
                    │ Drift Detection  │
                    └────────┬─────────┘
                             │
                    Investigation /
                      Retraining
                             │
                             └──────────────►
                                  Training

This feedback loop is one of the core ideas behind production MLOps.

🧪 Engineering Challenges Solved
1. Python Binary Compatibility
The Docker environment initially encountered C-level binary compatibility problems involving versions of:

NumPy
pandas
Other compiled scientific Python dependencies
These issues can be particularly difficult because the source code may appear correct while the runtime fails during import or execution.

Resolution
Dependencies were explicitly pinned in requirements.txt to create a reproducible runtime environment.

Engineering Lesson
Dependency management is part of ML engineering — not housekeeping.

2. Kubernetes Resource Deadlocks
The constrained GKE cluster experienced scheduling pressure during deployments.

The combination of limited node resources and replacement pods could leave workloads pending.

Resolution
The deployment strategy was changed from:

RollingUpdate

to:

Recreate

This reduced simultaneous resource requirements during deployment.

3. Infrastructure Became the Bottleneck
Stress testing demonstrated that increasing application concurrency eventually exposed the limits of the underlying small-node infrastructure.

The full request path is:

Client
  ↓
Network
  ↓
Load Balancer
  ↓
Kubernetes Service
  ↓
Pod
  ↓
FastAPI
  ↓
ML Model
  ↓
CPU / Memory

Optimizing only the Python application would not remove an infrastructure bottleneck.

📁 Repository Structure
.
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── data/
│   └── data.csv
│
├── k8s/
│   └── manifests.yaml
│
├── app.py
├── train.py
├── explain.py
├── fairness.py
├── run_predictions.py
├── drift.py
│
├── Dockerfile
├── requirements.txt
├── README.md
└── AI_USAGE_DOC.md

File Responsibilities
File	Responsibility
train.py	Model training and artifact generation
app.py	FastAPI inference service
explain.py	SHAP explainability analysis
fairness.py	Fairlearn fairness evaluation
drift.py	KS-test data drift detection
run_predictions.py	Live API prediction + GCP logging simulation
Dockerfile	Container image definition
k8s/manifests.yaml	Kubernetes Deployment, Service and HPA
.github/workflows/deploy.yml	CI/CD automation
requirements.txt	Reproducible Python dependencies
data/data.csv	Model development dataset

⚙️ Infrastructure Configuration
Component	Configuration
Cloud	Google Cloud Platform
Kubernetes	Google Kubernetes Engine
Node Type	e2-small
Container Registry	Google Artifact Registry
API	FastAPI
ML Framework	Scikit-Learn
Explainability	SHAP
Fairness	Fairlearn
Drift Detection	SciPy KS Test
CI/CD	GitHub Actions
Scaling	Kubernetes HPA
Minimum Pods	1
Maximum Pods	3
HPA Target	50% CPU
Deployment Strategy	Recreate
Logging	Google Cloud Logging
Load Testing	wrk

🔐 Security & Production Hardening Roadmap
This project focuses on demonstrating an end-to-end MLOps architecture.

A real healthcare production environment would require substantially stronger controls.

Application Security
Authentication
Authorization
API keys or OAuth2/OIDC
Request validation
Rate limiting
TLS
Secrets management
API versioning
Kubernetes Security
Non-root containers
Read-only root filesystem
Kubernetes SecurityContext
NetworkPolicies
Resource requests and limits
Pod security controls
Dedicated service accounts
Cloud Security
Workload Identity
Least-privilege IAM
Secret Manager
Private networking
Artifact vulnerability scanning
Cloud audit logging
ML Governance
Model registry
Model versioning
Dataset versioning
Experiment tracking
Model approval workflows
Reproducible training
Automated evaluation gates
Healthcare Data Protection
PHI/PII minimization
De-identification
Encryption in transit and at rest
Strict retention policies
Access auditing
Appropriate regulatory/compliance controls
🚀 CI/CD Pipeline
A push to main triggers the deployment workflow.

git push
    │
    ▼
┌────────────────────┐
│   GitHub Actions   │
└─────────┬──────────┘
          │
          ├── Authenticate to GCP
          │
          ├── Build Docker image
          │
          ├── Push to Artifact Registry
          │
          └── Deploy to GKE
                    │
                    ▼
             Kubernetes Rollout

The resulting delivery path is:

Source Code
     ↓
Docker Image
     ↓
Artifact Registry
     ↓
GKE
     ↓
Running API

This removes the need for manual image-building and deployment steps.

🧭 Local Development
1. Clone the Repository
git clone <your-repository-url>
cd <your-repository-name>

2. Create a Virtual Environment
python3.10 -m venv .venv
source .venv/bin/activate

3. Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

4. Train the Model
python train.py

5. Run the API
uvicorn app:app --host 0.0.0.0 --port 8000

The FastAPI service can then be accessed locally through the endpoint defined in app.py.

🐳 Build & Run with Docker
Build
docker build -t heart-disease-api .

Run
docker run -p 8000:8000 heart-disease-api

The application will then be available through the mapped local port.

☸️ Kubernetes Deployment
After configuring the appropriate:

GCP project
GKE cluster
Kubernetes credentials
Artifact Registry repository
apply the Kubernetes configuration:

kubectl apply -f k8s/manifests.yaml

Inspect the Deployment
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get hpa

Inspect Pod Logs
kubectl logs <pod-name>

📌 API Design
The inference layer is intentionally lightweight.

JSON Request
     │
     ▼
Schema Validation
     │
     ▼
Feature Preparation
     │
     ▼
ML Model
     │
     ▼
Prediction
     │
     ▼
JSON Response

Future API improvements could include:

Request IDs
Authentication
API versioning
Health checks
Readiness probes
Liveness probes
Structured application logging
Prometheus metrics
Distributed tracing
Rate limiting
Request-level monitoring
📊 Current Results
Area	Result
Model Serving	FastAPI inference API
Containerization	Docker
Cloud Deployment	GKE
Registry	Artifact Registry
Autoscaling	HPA
Pod Range	1–3
CPU Target	50%
Explainability	SHAP
Fairness	Fairlearn
Age Demographic Parity Difference	0.0000
Drift Detection	KS two-sample test
Drift Threshold	p < 0.05
Stress Test	~2,050 concurrent connections
Observed Average Latency	~1.22 s
Logging	Google Cloud Logging
CI/CD	GitHub Actions

Performance note: The stress-test measurements are environment-specific observations from a constrained GKE configuration. They should not be interpreted as universal production capacity benchmarks.

💡 What I Learned
The biggest lesson from this project was that production ML is fundamentally different from notebook ML.

A model can have strong offline metrics and still fail operationally because of:

Dependency conflicts
Container configuration
Insufficient compute
Deployment deadlocks
Missing observability
Data drift
Fairness concerns
Poor API design
Weak security boundaries
Building the complete system exposed these challenges much earlier than model experimentation alone would have.

🧠 Engineering Takeaways
1. ML is a systems problem
Model quality is only one component of production reliability.

2. Infrastructure decisions involve trade-offs
Recreate solved a constrained-cluster deployment problem, but introduced a temporary availability gap.

3. Metrics require context
A fairness metric of 0.0000 is meaningful only relative to the dataset, cohorts, metric and threshold used.

4. Stress testing reveals architecture limits
The application does not exist in isolation. The underlying infrastructure can become the bottleneck.

5. Observability must be designed
Without structured telemetry, production ML systems become difficult to debug and govern.

6. Drift detection closes the loop
Deployment is the beginning of the ML operational lifecycle — not the end.

🛣️ Roadmap
The next evolution of this platform could include:

🧪 Testing & Quality
 Automated unit tests
 Integration tests
 End-to-end API tests
 Automated model evaluation gates
 CI-based regression testing
🤖 ML Platform
 Model versioning
 Dataset versioning
 MLflow experiment tracking
 Model registry
 Automated retraining
 Model approval workflow
📊 Observability
 Prometheus metrics
 Grafana dashboards
 OpenTelemetry tracing
 Automated drift alerts
 Model performance monitoring
☸️ Kubernetes
 Readiness probes
 Liveness probes
 Resource requests/limits
 PodDisruptionBudget
 NetworkPolicies
 Canary deployments
 Blue/green deployments
🔐 Security
 Secret Manager integration
 Workload Identity
 Container vulnerability scanning
 Non-root container execution
 API authentication
 Rate limiting
 Privacy-aware logging
⚖️ Responsible AI
 Additional fairness metrics
 Calibration analysis
 Threshold analysis
 Additional protected attributes
 CI-based fairness regression checks
 Model cards / governance documentation
🏆 Why This Repository Matters
This project is deliberately small enough to understand while being broad enough to demonstrate the core responsibilities of an ML platform.

It demonstrates the transition from:

"I trained a model."

to:

"I built a system that can train, explain, evaluate, containerize, deploy, scale, observe and monitor a model."

That distinction is at the heart of MLOps engineering.

👨‍💻 Project Focus
This repository sits at the intersection of:

Machine Learning Engineering
             ×
Cloud Infrastructure
             ×
Kubernetes
             ×
MLOps
             ×
Responsible AI
             ×
Healthcare AI

The emphasis is on understanding the engineering trade-offs involved in taking an ML model beyond experimentation and toward a repeatable production workflow.

⭐ Interested in the Project?
If you're interested in:

ML infrastructure
MLOps
Kubernetes
Cloud-native systems
Responsible AI
Healthcare AI
Production ML
Developer infrastructure
feel free to explore the repository, inspect the architecture, and experiment with the deployment pipeline.

⚠️ Disclaimer
This project is an engineering and educational demonstration.

It is not a medical device, clinical decision-support system, or validated diagnostic tool and must not be used to make real-world medical decisions.

The model, fairness measurements, performance results, and infrastructure configuration are specific to the dataset and experimental environment used in this repository.

📬 Final Note
The purpose of this project is not to present a perfect production system.

It is to demonstrate the mindset required to build one:

             BUILD
               ↓
             DEPLOY
               ↓
             OBSERVE
               ↓
             MEASURE
               ↓
             EVALUATE
               ↓
             IMPROVE
               │
               └───────────────┐
                               ▼
                              BUILD

Build models. Ship systems. Measure everything.

<p align="center"> <strong>🩺 Healthcare ML × ☁️ Cloud × ☸️ Kubernetes × 🤖 MLOps × ⚖️ Responsible AI</strong> </p>


