# ZipCab - Dynamic Cab Fare Booking Platform

## Project Overview
ZipCab is a cab booking platform that calculates fares dynamically based on the distance between user-specified locations and the number of passengers. The project started as a simple fare-calculation script and evolved into a full-stack Django REST API with a React client application.

---

## Motivation
Initially, the task was to calculate fares based on the number of passengers. Later, I wanted to make the fare calculation dynamic based on the distance between pickup and drop-off locations. After evaluating Google Maps API, I opted for the free **Distance Matrix AI API** to integrate distance-based calculations into the project. 

---

## Features
- Dynamic fare calculation using the Distance Matrix AI API.
- Persistent storage of bookings in PostgreSQL.
- Authentication and authorization using JWT tokens.
- RESTful API architecture using Django REST Framework.
- Simple, responsive React frontend using TailwindCSS.
- Caching for faster repeated requests.
- Deployment-ready with Docker and Render.

---

## Tech Stack
| Layer          | Technology                       |
|----------------|---------------------------------|
| Backend        | Python, Django, Django REST Framework |
| Frontend       | React, TailwindCSS              |
| Database       | PostgreSQL                      |
| Authentication | JWT Tokens                       |
| Deployment     | Render                           |
| Containerization | Docker (implemented, learning in progress) |

---

## Architecture
1. **Backend**
   - Django REST Framework handles API requests.
   - `Booking` model stores trip details.
   - Utility functions calculate distance and fare.
   - JWT authentication for secure access.
   - Caching implemented for repeated requests.
   
2. **Frontend**
   - React app communicates with Django APIs.
   - Components: Login, Register, BookingForm, BookingHistory, FareCalculator.
   - TailwindCSS for simple, responsive UI.

3. **Deployment**
   - Hosted on Render.
   - Docker container used for backend and frontend (learning phase).

---

## Workflow
1. User enters pickup and drop-off locations along with passenger count.
2. Backend queries the **Distance Matrix AI API** to calculate distance.
3. Fare is computed dynamically based on distance and passenger count.
4. Booking data is stored in PostgreSQL.
5. API responses are cached for faster repeated queries.
6. Frontend fetches data from APIs and displays results to the user.

---

## Future Updates
- Complete Docker containerization for full deployment.
- Improved UI with custom design.
- Add features like ride history analytics and booking notifications.
- Integrate payment gateway for seamless transactions.

---

## Getting Started

### Prerequisites
- Python 3.x
- Node.js & npm
- PostgreSQL
- Render account (optional for deployment)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd zipcab
2. Backend setup:

  - python -m venv venv
  - source venv/bin/activate   # On Windows: venv\Scripts\activate
  - pip install -r requirements.txt
  - python manage.py migrate
  - python manage.py runserver

3.Frontend setup:
  - cd client
  - npm install
  - npm start



### PREVIEW

<img width="941" height="467" alt="Screenshot 2025-11-17 110350" src="https://github.com/user-attachments/assets/1f1d3249-57da-467e-8f00-01cf28e9d5bb" />
<img width="941" height="467" alt="Screenshot 2025-11-17 110513" src="https://github.com/user-attachments/assets/f33857b8-4a2f-4ac4-b0d9-9e0cafba7196" />
<img width="955" height="470" alt="Screenshot 2025-11-17 110549" src="https://github.com/user-attachments/assets/5537f14c-54e3-4541-bd2a-533fb65088b5" />
<img width="957" height="471" alt="Screenshot 2025-11-17 110709" src="https://github.com/user-attachments/assets/3b76d702-56a6-4ccb-b6b5-90ff44e99141" />
<img width="941" height="468" alt="Screenshot 2025-11-17 110801" src="https://github.com/user-attachments/assets/6b368603-5364-4afb-819e-67246c6900b8" />
<img width="954" height="471" alt="Screenshot 2025-11-17 110842" src="https://github.com/user-attachments/assets/5ab3e385-ef7b-49d6-ae6c-9b9984302127" />

