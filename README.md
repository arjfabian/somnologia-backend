# Somnologia Backend API

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Django](https://img.shields.io/badge/Django-4.x-green.svg)
![Django REST Framework](https://img.shields.io/badge/DRF-3.x-red.svg)
![Database](https://img.shields.io/badge/SQLite-DB-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📜 Project Overview

For years, I meticulously recorded dreams – from haunting nightmares to vivid lucid experiences and even perplexing premonitions. Over time, a profound realization emerged: these nocturnal narratives weren't random; they were a deeply personal chronicle of my hopes, fears, and forgotten memories. To truly understand this intricate story and illuminate a clearer path forward, I decided to harness the power of Artificial Intelligence for interpretation. From this challenge, **Somnologia** was born.

This repository hosts the **backend API** for the Somnologia application, built with Django and Django REST Framework. It provides robust endpoints for managing dream entries, interacting with an AI interpreter for analysis and image generation, and aggregating data for insightful dashboards.

## ✨ Features

The Somnologia Backend API currently provides the following core functionalities:

- **Dream Management:** Full CRUD (Create, Read, Update, Delete) operations for `Dream` entries, allowing users to log and manage their nocturnal narratives.

- **Person Management:** CRUD operations for `Person` entities (e.g., individuals, archetypes, fictional characters) associated with dreams.

- **Tag Management:** CRUD operations for `Tag` entities, enabling categorization and organization of dreams (e.g., "lucid," "nightmare," "recurring").

- **AI Dream Interpretation:** An endpoint to send dream descriptions for AI-powered analysis, generating interpretations and suggesting relevant `Persons` and `Tags`.

- **AI Image Generation (Placeholder):** Integration with an AI image generation module (currently a placeholder) to produce visual representations based on dream descriptions or interpretations.

- **Dashboard Data:** An endpoint providing aggregated data for analytics, such as the latest dream entries and counts of dreams associated with each person, ready for frontend visualization.

## 🚀 Getting Started

These instructions will get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10+
- pip (Python package installer)
- Git

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/your-username/somnologia-backend.git](https://github.com/your-username/somnologia-backend.git)
    cd somnologia-backend
    ```

    (Replace `your-username` with your actual GitHub username)

2.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On macOS/Linux
    # .venv\Scripts\activate   # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run database migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **(Optional) Create a superuser to access the Django Admin:**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    The API will be available at `http://127.0.0.1:8000/`.

## 📚 API Endpoints

The API is served under the `/api/v1/` prefix.

| Method | Endpoint                | Description                                       |
| :----- | :---------------------- | :------------------------------------------------ |
| `GET`  | `/api/v1/persons/`      | List all persons                                  |
| `POST` | `/api/v1/persons/`      | Create a new person                               |
| `GET`  | `/api/v1/persons/{id}/` | Retrieve a person by ID                           |
| `PUT`  | `/api/v1/persons/{id}/` | Update a person by ID                             |
| `DEL`  | `/api/v1/persons/{id}/` | Delete a person by ID                             |
| `GET`  | `/api/v1/dreams/`       | List all dreams                                   |
| `POST` | `/api/v1/dreams/`       | Create a new dream                                |
| `GET`  | `/api/v1/dreams/{id}/`  | Retrieve a dream by ID                            |
| `PUT`  | `/api/v1/dreams/{id}/`  | Update a dream by ID                              |
| `DEL`  | `/api/v1/dreams/{id}/`  | Delete a dream by ID                              |
| `GET`  | `/api/v1/tags/`         | List all tags                                     |
| `POST` | `/api/v1/tags/`         | Create a new tag                                  |
| `GET`  | `/api/v1/tags/{id}/`    | Retrieve a tag by ID                              |
| `PUT`  | `/api/v1/tags/{id}/`    | Update a tag by ID                                |
| `DEL`  | `/api/v1/tags/{id}/`    | Delete a tag by ID                                |
| `GET`  | `/api/v1/dashboard/`    | Get aggregated dashboard data                     |
| `POST` | `/api/v1/interpret/`    | Get AI interpretation and suggestions for a dream |

_(For detailed request/response examples, consult the browsable API at `http://127.0.0.1:8000/api/v1/` when the server is running.)_

## 🛣️ Future Enhancements

- Integration with AI models for dream interpretation (e.g. ChatGPT, Gemini) and image generation (e.g., DALL-E, Midjourney API).
- User authentication and authorization.
- Detailed logging and error handling.
- Deployment to a production environment.

## 🤝 Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 📧 Contact

For any questions or feedback, feel free to contact me at:

- **LinkedIn:** [linkedin.com/in/arjfabian](https://www.linkedin.com/in/arjfabian)

- **GitHub:** [github.com/arjfabian](https://github.com/arjfabian)

- **Email:** [jfabian@datorum.net](mailto:jfabian@datorum.net)

---
