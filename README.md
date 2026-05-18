# 📊 Conversational Analytics Platform

[![Framework: FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Frontend: React](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![AI Engine: Gemini](https://img.shields.io/badge/AI_Engine-Gemini_API-8E44AD?style=for-the-badge&logo=googlegemini&logoColor=white)](https://ai.google.dev)
[![Database: Firestore](https://img.shields.io/badge/Database-Firebase_Firestore-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)](https://firebase.google.com)

An enterprise-grade, full-stack conversational business intelligence engine. This platform abstracts complex database querying layers by converting raw human language (e.g., *"Show me total sales for laptops in Faisalabad last month"*) into structured data models and rendering dynamic, real-time visual charts instantly.

---

## 🗺️ Visual System Architecture & Data Flow

Below is the structured technical workflow demonstrating how multi-tiered asynchronous transactions flow across decoupled endpoints seamlessly:

![System Architecture](https://mermaid.ink/img/pako:eNqNkMFOwzAMhl_F-mUvMDRuEAdunDgBwYFwW9I0bVpInSqpU9gQ707atgMJuKTSX_792f_ZOU_KGgU9eO_YWhM0GofD9v0AnWe-V6YVNDX6Z545vG_D8bC9K6r_gA_m1jR0BfKz9Wwz-7iU90T8V3vYJ9vTUPYtWGe2_gR2U0X7mZ2D7a_sAror6U9gUbePqL4D6031fWf36D6-f4_XwLao6E_w_wE-2F_T0FXIiQGz_8_KWeV_C8hYVQ)

| Flow Sequence | Layer Component | Operational Responsibilities |
| :--- | :--- | :--- |
| **01. UI Capture** | **React Frontend Interface** | Captures plain conversational text inputs; blocks manual query writing loops entirely. |
| **02. Translation** | **FastAPI Core + Gemini API Engine** | Sanitizes text payloads; runs strict zero-shot target parameter mappings into clean JSON filters. |
| **03. Cloud Fetch** | **Firebase Firestore Loop** | Resolves dynamic server filters against NoSQL collections programmatically; returns payload sets. |
| **04. Mount Grid** | **Dynamic Component Mapper** | Inspects specific layout configuration keys; auto-mounts matching responsive analytics blocks. |

---

## 🚀 Enterprise Tech Stack

* **Front-end Dashboard:** React.js initialized with component-driven decoupled state hooks.
* **Data Visualization Layer:** Recharts API (Dynamic SVG rendering loop).
* **Asynchronous Network Gateways:** FastAPI web framework deployed via Uvicorn instances.
* **Large Language Model Interpreter:** Google Gemini Pro structured via strict system prompts.
* **Persistence Store:** Cloud Firebase Document Store (NoSQL Firestore).

---

## 🛠️ System Installation & Deployment Playbook

### 1. Asynchronous Backend Server Configuration
1. Enter the isolated target directory and instantiate a clean virtual environment block:
   ```bash
   cd backend
   python -m venv venv