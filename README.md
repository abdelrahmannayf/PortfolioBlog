# 🌐 Portfolio Blog — Multi-Tier DevOps Project

A production-grade multi-tier web application featuring a personal portfolio and blog, built with Flask, PostgreSQL, and Nginx — fully containerized, orchestrated on Kubernetes via Helm, and monitored with Prometheus & Grafana.

---

## 🏗️ Architecture Diagram

```
                         ┌──────────────┐
                         │   Developer  │
                         └──────┬───────┘
                                │ git push
                                ▼
                         ┌──────────────┐
                         │    GitHub    │
                         └──────┬───────┘
                                │ trigger
                                ▼
┌───────────────────────────────────────────────────────┐
│                    Jenkins Pipeline                    │
│                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐ │
│  │ Checkout │─►│   Run    │─►│  Build Docker Image  │ │
│  │   SCM    │  │  Tests   │  │  (BUILD_NUMBER tag)  │ │
│  └──────────┘  └──────────┘  └──────────┬───────────┘ │
│                                          │             │
│  ┌──────────┐  ┌──────────┐  ┌──────────▼───────────┐ │
│  │ Cleanup  │◄─│  Deploy  │◄─│   Push to DockerHub  │ │
│  │          │  │ with Helm│  │                      │ │
│  └──────────┘  └──────────┘  └──────────────────────┘ │
└───────────────────────────────────────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │   DockerHub Registry  │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────────────────┐
                    │       Kubernetes Cluster           │
                    │                                    │
                    │  ┌─────────────────────────────┐  │
                    │  │     namespace: monitoring    │  │
                    │  │                             │  │
                    │  │  ┌──────────────────────┐  │  │
                    │  │  │   Nginx (NodePort)   │  │  │
                    │  │  │     Port: 30009      │  │  │
                    │  │  └──────────┬───────────┘  │  │
                    │  │             │               │  │
                    │  │  ┌──────────▼───────────┐  │  │
                    │  │  │  Flask (2 replicas)  │  │  │
                    │  │  │     Port: 5000       │  │  │
                    │  │  └──────────┬───────────┘  │  │
                    │  │             │               │  │
                    │  │  ┌──────────▼───────────┐  │  │
                    │  │  │      PostgreSQL       │  │  │
                    │  │  │     Port: 5432        │  │  │
                    │  │  └──────────────────────┘  │  │
                    │  │                             │  │
                    │  │  ┌──────────┐ ┌──────────┐  │  │
                    │  │  │Prometheus│►│ Grafana  │  │  │
                    │  │  └──────────┘ └──────────┘  │  │
                    │  └─────────────────────────────┘  │
                    └───────────────────────────────────┘
```

---

## ⚙️ Jenkins Pipeline Stages

| # | Stage | Description | Time |
|---|---|---|---|
| 1 | **Checkout SCM** | Clone repo from GitHub | ~31s |
| 2 | **Checkout** | Verify workspace | ~2s |
| 3 | **Run Tests** | Flask test client validates all routes | ~1s |
| 4 | **Build Docker Image** | Multi-stage build tagged with BUILD_NUMBER | ~2s |
| 5 | **Push to DockerHub** | Push image with version + latest tags | ~17s |
| 6 | **Deploy with Helm** | `helm upgrade --install` on Kubernetes | ~10s |
| 7 | **Cleanup** | Remove old local Docker images | ~1s |
| 8 | **Post Actions** | Print success/failure message | ~77ms |

---

## 🛠️ Tech Stack

| Category | Tool |
|---|---|
| Backend | Flask + Python |
| Database | PostgreSQL |
| Reverse Proxy | Nginx |
| Containerization | Docker Multi-stage |
| Container Registry | DockerHub |
| Orchestration | Kubernetes (Kind) |
| Package Manager | Helm |
| CI/CD | Jenkins |
| Monitoring | Prometheus + Grafana |

---

## 📁 Project Structure

```
PortfolioBlog/
├── app/                        # Flask Application
│   ├── app.py                  # Routes + DB models
│   ├── requirements.txt
│   ├── templates/
│   │   ├── index.html          # Portfolio page
│   │   ├── blog.html           # Blog listing
│   │   ├── post.html           # Single post
│   │   └── new_post.html       # Create post
│   └── static/css/
│       └── style.css
│
├── nginx/
│   └── nginx.conf              # Reverse proxy config
│
├── portfoliochart/             # Helm Chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml     # Flask + Postgres + Nginx
│       ├── service.yaml
│       └── configmap.yaml      # Nginx config
│
├── docker-compose.yml          # Local development
├── Dockerfile                  # Multi-stage build
└── Jenkinsfile                 # CI/CD Pipeline
```

---

## 🚀 Setup & Deployment

### Prerequisites
- Docker + Docker Compose
- Kubernetes cluster (Kind)
- Helm 3
- Jenkins

---

### 1️⃣ Clone Repository

```bash
git clone https://github.com/abdelrahmannayf/PortfolioBlog.git
cd PortfolioBlog
```

---

### 2️⃣ Run Locally with Docker Compose

```bash
docker-compose up --build -d
```

Open: `http://localhost:8090`

---

### 3️⃣ Build & Push Docker Image

```bash
docker build -t abdelrahmannayf/portfolioblog:latest .
docker push abdelrahmannayf/portfolioblog:latest
```

---

### 4️⃣ Deploy on Kubernetes with Helm

```bash
kubectl create namespace monitoring
helm install portfolio ./portfoliochart -n monitoring
kubectl get pods -n monitoring
```

Access the app:
```
http://NODE_IP:30009
```

---

### 5️⃣ Monitor with Prometheus + Grafana

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring
kubectl port-forward svc/prometheus-grafana -n monitoring 3000:80
```

Open Grafana: `http://localhost:3000`

Import Dashboard ID: **15760**

---

## 🔄 CI/CD Flow

```
Push code → Jenkins → Test → Build → Push → Helm Deploy → Monitor ✅
```

---

## 🔐 Jenkins Credentials Required

| ID | Type | Used In |
|---|---|---|
| `dockerhub-cred` | Username/Password | Push image to DockerHub |

---

## 👤 Author

**Abdelrahman Nayf**

- 🐙 GitHub: [@abdelrahmannayf](https://github.com/abdelrahmannayf)
- 💼 LinkedIn: [abdelrahman-nayf](https://www.linkedin.com/in/abdelrahman-nayf-b0a365214)
- 📧 Email: abdelrahmannayf@gmail.com
