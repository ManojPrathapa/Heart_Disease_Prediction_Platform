🩺 Healthcare MLOps — Production-Grade Heart Disease Prediction Platform
<p align="center"> <strong>From ML notebook → production API → Kubernetes → CI/CD → observability → fairness → drift detection</strong> </p> <p align="center">










</p>
🚀 What This Project Demonstrates
Most machine-learning projects stop at:

Train model → achieve accuracy → save .pkl file → done.

This project focuses on what happens after the model works.

It takes a heart-disease prediction model through an end-to-end production-oriented MLOps lifecycle:

                    ┌─────────────────────┐
                    │   Clinical Dataset  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Model Training    │
                    │    Scikit-Learn     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Model Artifact      │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌──────────┐     ┌───────────┐    ┌───────────┐
        │  SHAP    │     │ Fairlearn │    │ KS Drift  │
        │   XAI    │     │  Audit    │    │ Detection │
        └──────────┘     └───────────┘    └───────────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI         │
                    │  Inference Service  │
                    └──────────┬──────────┘
                               │
                        Docker Container
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Google Artifact     │
                    │      Registry       │
                    └──────────┬──────────┘
                               │
                         GitHub Actions
                               │
                               ▼
                    ┌─────────────────────┐
                    │       GKE           │
                    │ Kubernetes Cluster  │
                    └──────────┬──────────┘
                               │
                   ┌───────────┴───────────┐
                   ▼                       ▼
             LoadBalancer                 HPA
                   │                 1 → 3 Pods
                   │                       │
                   └───────────┬───────────┘
                               ▼
                    Production API Traffic
                               │
                               ▼
                    ┌─────────────────────┐
                    │ GCP Cloud Logging   │
                    │   Audit / Telemetry │
                    └─────────────────────┘

The goal isn't to claim this is a hospital-ready diagnostic system.

The goal is to demonstrate the engineering discipline required to move an ML workload toward production.

🎯 Why This Project Exists
Healthcare ML introduces requirements that go beyond model accuracy.

A production system needs to answer questions such as:

Can the model be served reliably?
Can it scale when traffic increases?
Can deployments be automated?
Can model decisions be investigated?
Can potential demographic disparities be measured?
Can input distribution changes be detected?
Can inference activity be audited?
What happens when infrastructure reaches its resource limits?
Can the entire system be reproduced from source control?
This repository addresses those questions through a deliberately small but complete cloud-native ML system.

🧠 Engineering Philosophy
The central principle of this project is:

A model is not a production system.

A production ML system is the combination of:

Model
  +
Data
  +
API
  +
Container
  +
Infrastructure
  +
CI/CD
  +
Observability
  +
Testing
  +
Governance

This repository intentionally explores each layer.

🏗️ System Architecture
High-Level Architecture
                           GitHub
                             │
                             │ push to main
                             ▼
                    ┌──────────────────┐
                    │ GitHub Actions   │
                    │   CI/CD Pipeline  │
                    └────────┬─────────┘
                             │
                    Build + Authenticate
                             │
                             ▼
                    ┌──────────────────┐
                    │ Docker Image     │
                    │ FastAPI + Model  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Artifact Registry│
                    └────────┬─────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │            GKE               │
              │                              │
              │   ┌──────────────────────┐   │
Internet ────►│   │ LoadBalancer Service │   │
              │   └──────────┬───────────┘   │
              │              │               │
              │       ┌──────┴──────┐        │
              │       ▼             ▼        │
              │    FastAPI        FastAPI     │
              │      Pod            Pod       │
              │       │             │         │
              │       └──────┬──────┘         │
              │              │               │
              │             HPA              │
              └──────────────┼───────────────┘
                             │
                             ▼
                    GCP Cloud Logging

🔄 End-to-End MLOps Lifecycle
1. Model Development
The training pipeline produces the model artifact from the clinical dataset.

data.csv
   │
   ▼
train.py
   │
   ├── Data loading
   ├── Preprocessing
   ├── Model training
   └── Artifact serialization
          │
          ▼
     Model Artifact

2. Explainability
The trained model is analyzed with SHAP to understand feature contributions.

The analysis identified features such as:

fbs
restecg
trestbps
as having relatively low impact on the current model's predictive thresholds.

This does not mean these clinical variables are medically unimportant.

It means their contribution to this particular trained model was comparatively low.

That distinction matters when communicating ML results in healthcare.

🔍 Explainable AI with SHAP
Black-box behavior creates additional risk in high-impact domains.

This project therefore includes a dedicated explainability stage:

Trained Model
      │
      ▼
    SHAP
      │
      ├── Feature contribution
      ├── Model behavior analysis
      └── Interpretability investigation

The purpose is not merely to generate a visualization.

It is to create a mechanism for asking:

"Why did the model make this prediction?"

This is especially important when model outputs could influence downstream clinical workflows.

⚖️ Algorithmic Fairness
The project also includes demographic fairness analysis using Fairlearn.

The continuous age variable was transformed into demographic cohorts:

Age
 │
 ├── Young
 ├── Middle
 └── Senior

The analysis measured differences in positive prediction rates between groups.

Observed Result
Maximum demographic parity difference: 0.0000

This indicates that, on the evaluated dataset, the measured positive prediction rates were equal across the tested age cohorts.

Important Caveat
A fairness metric of 0.0000 should not be interpreted as proof that the model is universally fair.

Fairness depends on:

Dataset composition
Cohort definitions
Sample size
Choice of protected attribute
Metric selection
Threshold
Real-world population shift
Therefore, this result should be understood as:

No measured demographic-parity difference was observed across the evaluated age cohorts on this dataset.

That is a substantially more defensible engineering claim than declaring the model "bias-free."

⚡ Production API
The trained model is exposed through a lightweight FastAPI inference service.

Conceptually:

HTTP Request
     │
     ▼
FastAPI
     │
     ├── Validate input
     │
     ├── Load model
     │
     ├── Generate prediction
     │
     └── Return structured response

This separates the model from the client application and provides a clean HTTP interface for inference.

🐳 Containerization
The API and model artifacts are packaged into a Docker image.

Docker Image
│
├── Python runtime
├── Application dependencies
├── FastAPI application
├── Scikit-Learn model
└── Runtime configuration

Containerization provides:

Reproducible runtime environments
Consistent local/cloud behavior
Easier deployment
Dependency isolation
Portable infrastructure
☁️ Google Cloud Deployment
The production deployment uses:

Cloud Platform
Google Cloud Platform

Container Registry
Google Artifact Registry

Compute / Orchestration
Google Kubernetes Engine (GKE)

Networking
Kubernetes LoadBalancer Service

Autoscaling
Horizontal Pod Autoscaler

☸️ Kubernetes Architecture
The Kubernetes deployment includes:

Deployment
   │
   ├── Pod
   ├── Pod
   └── Pod
        ▲
        │
        │ HPA
        │
LoadBalancer Service

The configured autoscaling policy is:

Minimum replicas: 1
Maximum replicas: 3
CPU target:       50%

This provides a basic horizontal scaling mechanism for CPU-driven workloads.

🔁 Deployment Strategy
The deployment uses:

strategy:
  type: Recreate

rather than the Kubernetes default RollingUpdate.

Why?
The deployment was intentionally optimized for a constrained-resource GKE environment.

During testing, rolling replacement could create scheduling pressure where old and new pods competed for limited cluster resources.

Recreate ensures:

Terminate old workload
        ↓
Free resources
        ↓
Schedule new workload

This introduces a temporary availability trade-off, but makes the deployment more predictable for a small experimental cluster.

Production Trade-Off
For a larger production cluster, a more sophisticated strategy would likely be preferable:

Rolling deployments
Readiness probes
PodDisruptionBudgets
Multiple replicas
Resource requests/limits
Dedicated node pools
Progressive delivery
Canary deployments
The configuration here is therefore an intentional infrastructure trade-off, not an assertion that Recreate is universally superior.

📈 Load & Stress Testing
The API was stress-tested using wrk.

Observed Test Result
Concurrent connections: ~2,050
Average latency:        ~1.22 seconds

The constrained e2-small infrastructure eventually reached socket/resource limitations under extreme concurrency.

Rather than interpreting this as a production capacity benchmark, the test was used to investigate:

API resilience
Kubernetes behavior
Resource exhaustion
Failure characteristics
Infrastructure limits
Engineering Takeaway
The system remained operational under significant connection pressure until the underlying constrained infrastructure became the bottleneck.

This highlights an important production principle:

Application performance and infrastructure capacity are separate problems.

📊 Observability & Audit Logging
Inference systems need visibility into what is happening after deployment.

This project integrates Google Cloud Logging through the Python client.

The prediction simulator sends clinical inference requests to the live GKE endpoint.

Structured information can then be captured for operational analysis, including:

{
  "timestamp": "...",
  "features": "...",
  "prediction": "..."
}

This enables workflows such as:

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
GCP Logs Explorer

Why This Matters
Observability makes it possible to investigate:

Request behavior
Prediction activity
Application failures
Deployment issues
Unexpected traffic
Model behavior over time
Healthcare Consideration
In a real healthcare deployment, logging raw clinical payloads requires strict privacy controls.

A production implementation should consider:

Data minimization
PHI/PII redaction
Encryption
IAM
Retention policies
Access auditing
Least-privilege service accounts
Regulatory requirements
This repository demonstrates the technical observability pattern, not a claim of regulatory certification.

📉 Data Drift Detection
A deployed model can become less reliable when the distribution of incoming data changes.

This project implements statistical drift detection using the Kolmogorov-Smirnov two-sample test.

Training Distribution
        │
        │
        ▼
     KS Test
        ▲
        │
        │
Live Inference Distribution

The detector compares:

Baseline training data
          vs.
Live inference data

using:

scipy.stats.ks_2samp

The configured statistical threshold is:

α = 0.05

A sufficiently low p-value can trigger a drift signal.

Why Drift Detection Matters
Model degradation can occur without any code changing.

The production environment can change because:

Patient populations change
Data collection processes change
Sensors/devices change
Clinical workflows change
Feature distributions shift
Therefore:

Model deployment is not the end of the ML lifecycle.

🔬 MLOps Control Loop
The complete lifecycle can be viewed as a feedback system:

       ┌─────────────────────────┐
       │     Training Data       │
       └────────────┬────────────┘
                    ▼
             Model Training
                    │
                    ▼
              Model Artifact
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
       Explainability      Fairness
          │                   │
          └─────────┬─────────┘
                    ▼
                Deployment
                    │
                    ▼
                 GKE API
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
       Logging   Predictions  Traffic
          │
          ▼
      Drift Detection
          │
          ▼
   Retraining / Investigation
          │
          └──────────► Model Training

This feedback loop is the foundation of production ML engineering.

🧪 Engineering Challenges Solved
1. Python Binary Compatibility
The Docker environment initially experienced C-level compatibility issues involving versions of:

NumPy
pandas
Other compiled Python dependencies
These failures are particularly painful because the code itself may appear correct while the runtime fails during import or execution.

Resolution
Dependencies were explicitly pinned in requirements.txt to establish a reproducible environment.

Lesson
Dependency management is part of ML engineering, not housekeeping.

2. Kubernetes Resource Deadlocks
The constrained GKE cluster experienced scheduling pressure during deployments.

The combination of limited node resources and replacement pods could result in workloads remaining pending.

Resolution
The deployment strategy was changed from:

RollingUpdate

to:

Recreate

for the target environment.

This reduced simultaneous resource requirements during deployment.

3. Infrastructure Became the Bottleneck
Stress testing showed that increasing application concurrency eventually exposed the limits of the underlying small-node infrastructure.

This demonstrated why production performance testing must consider the complete stack:

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
Application
  ↓
Model
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
k8s/manifests.yaml	Kubernetes deployment, service and HPA
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
This project intentionally focuses on demonstrating an end-to-end MLOps architecture.

For a real healthcare production environment, additional controls would be required.

Application Security
Authentication
Authorization
API keys or OAuth2/OIDC
Request validation
Rate limiting
TLS termination
Secrets management
Kubernetes Security
Non-root containers
Read-only root filesystem
SecurityContext
NetworkPolicies
Resource requests/limits
Pod security controls
Dedicated service accounts
Cloud Security
Workload Identity
Least-privilege IAM
Secret Manager
Private networking
Artifact vulnerability scanning
Audit logging
ML Governance
Model registry
Model versioning
Dataset versioning
Experiment tracking
Model approval workflow
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
GitHub Actions
   │
   ├── Authenticate to GCP
   │
   ├── Build Docker image
   │
   ├── Push image to Artifact Registry
   │
   └── Deploy to GKE
            │
            ▼
       Kubernetes Rollout

This eliminates manual image-building and deployment steps.

The result is a repeatable path from:

Source Code
     ↓
Container
     ↓
Registry
     ↓
Cluster
     ↓
Running API

🧭 Local Development
Clone
git clone <your-repository-url>
cd <your-repository-name>

Create Environment
python3.10 -m venv .venv
source .venv/bin/activate

Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

Train the Model
python train.py

Run the API
uvicorn app:app --host 0.0.0.0 --port 8000

The API can then be tested locally through the FastAPI endpoint exposed by the application.

🐳 Build the Docker Image
docker build -t heart-disease-api .

Run locally:

docker run -p 8000:8000 heart-disease-api

☸️ Kubernetes Deployment
After configuring the appropriate GCP project, cluster, credentials, and Artifact Registry repository:

kubectl apply -f k8s/manifests.yaml

Inspect the deployment:

kubectl get deployments
kubectl get pods
kubectl get services
kubectl get hpa

Inspect logs:

kubectl logs <pod-name>

📌 API Design
The inference layer is intentionally lightweight.

A typical prediction lifecycle is:

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

For production, the API could be extended with:

OpenAPI schema validation
Request IDs
Structured application logs
Authentication
Versioned endpoints
Health checks
Readiness/liveness probes
Prometheus metrics
Distributed tracing
📊 Current Results
Area	Result
Model Serving	FastAPI production-style inference API
Containerization	Docker
Cloud Deployment	GKE
Registry	Artifact Registry
Autoscaling	HPA, 1–3 pods
Explainability	SHAP
Fairness	Fairlearn
Measured Age Demographic Parity Difference	0.0000
Drift Detection	KS two-sample test
Drift Threshold	p < 0.05
Stress Test	~2,050 concurrent connections
Observed Avg. Latency	~1.22 s
Logging	GCP Cloud Logging
CI/CD	GitHub Actions

Note: Performance figures are environment-specific measurements from a constrained GKE configuration and should not be interpreted as universal production capacity benchmarks.

💡 What I Learned
The biggest lesson from this project was that production ML is fundamentally different from notebook ML.

A model can have excellent offline metrics and still fail operationally because of:

Dependency conflicts
Bad container configuration
Insufficient compute
Deployment deadlocks
Missing observability
Data drift
Fairness issues
Poor API design
Weak security boundaries
Building the complete system exposed these problems much earlier than model experimentation alone would have.

🧠 Engineering Takeaways
1. ML is a systems problem
Model quality is only one component of production reliability.

2. Infrastructure decisions have trade-offs
Recreate solved a constrained-cluster deployment problem, but at the cost of zero-overlap deployment.

3. Metrics require context
A fairness score of 0.0000 is meaningful only relative to the tested dataset, cohorts, metric and threshold.

4. Stress testing reveals architecture limits
The application did not exist in isolation. The underlying node capacity ultimately became the limiting factor.

5. Observability must be designed, not added accidentally
Without structured telemetry, production ML systems become difficult to debug and govern.

6. Drift detection closes the ML feedback loop
Deployment is the beginning of the operational lifecycle, not the end.

🛣️ Roadmap
The next evolution of this system would include:

 Automated unit and integration tests
 Automated model evaluation gates in CI
 Model versioning
 Dataset versioning
 MLflow experiment tracking
 Prometheus/Grafana metrics
 OpenTelemetry tracing
 Canary deployments
 Blue/green deployment support
 Kubernetes readiness/liveness probes
 Resource requests and limits
 PodDisruptionBudget
 NetworkPolicies
 Secret Manager integration
 Container vulnerability scanning
 Automated drift alerts
 Automated retraining pipeline
 Model registry
 Stronger privacy controls
 Calibration and threshold analysis
 Additional fairness metrics
 CI-based SHAP/fairness regression checks
🏆 Why This Repository Matters
This project is deliberately small enough to understand but broad enough to demonstrate the core responsibilities of an ML platform.

It demonstrates the transition from:

"I trained a model."

to:

"I built a system that can train, explain, evaluate,
containerize, deploy, scale, observe and monitor a model."

That distinction is the heart of MLOps engineering.

👨‍💻 Project Focus
This repository is a hands-on exploration of:

Machine Learning Engineering × Cloud Infrastructure × Kubernetes × MLOps × Responsible AI

The emphasis is on understanding the engineering trade-offs involved in taking an ML model beyond experimentation and toward a repeatable production workflow.

⭐ If You Find This Interesting
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
