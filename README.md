# 🎬 Movie Watchlist App

A responsive, full-stack Flask web application that enables users to **discover movies**, **add them to a watchlist**, and **rate movies** they've seen. Built with a PostgreSQL backend, the app features both guest and authenticated experiences, light/dark mode themes, and is deployed on **Google Cloud Run** with a PostgreSQL database hosted on **Azure**.

---

##  Live Demo

[Visit the Live App](https://movie-watchlist-976221425311.us-west2.run.app/)

- **Demo Credentials:**
  - **Username:** `guest`
  - **Password:** `Guest@123`

---

##  Tech Stack

- **Backend:** Python, Flask, Psycopg3
- **Database:** PostgreSQL (hosted on Azure)
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Google Cloud Run (serverless hosting)
- **Others:** Responsive design, light/dark mode support

---

##  Features

- **Flexible User Modes**: Browse as a guest or register to save personal movie ratings and watchlists visible to others.
- **Movie Actions**: Search for movies, bookmark titles to watch later, and rate titles you've seen.
- **User Profiles**: Public and private profiles feature personalized lists and ratings.
- **Responsive UI**: Mobile-friendly layout with toggle for light and dark themes.
- **Secure Backend**: Flask session-based authentication, backend validation, and error handling.

---

##  Local Setup

To run the app locally, follow these steps:

```bash
# 1. Clone the repo
git clone https://github.com/aoseni-tech/movie-watchlist-app.git
cd movie-watchlist-app

# 2. Set up a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables

# 5. Run the development server
flask run
