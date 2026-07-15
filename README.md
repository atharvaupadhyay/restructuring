# Atharva Upadhyay's Website

This repository contains the source code for my personal portfolio website.

It's built with Flask and serves as a place to showcase my projects, achievements, and ways to get in touch. I'm rebuilding the site from scratch, so expect things to change as I keep adding features and improving the design.

## Features

- Responsive design
- Light and dark mode
- Contact form with Discord notifications
- Sam protection and rate limiting
- Project pages (Under work)
- Achievement section

## Tech Stack

- Flask
- HTML, CSS, JavaScript
- Flask-WTF
- Flask-Limiter
- Redis (for rate limiting)
- Vercel (hosting)

## Running Locally

Clone the repository:

```bash
git clone https://github.com/atharvaupadhyay/restructuring
cd restructuring
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
SECRET_KEY=...
DISCORD_WEBHOOK_URL=...
REDIS_URL=memory://
```

Start the server:

```bash
python main.py
```

The site will be available at `http://localhost:5000`.

## Project Structure

```
api/            Flask routes
templates/      HTML templates
public/         CSS, JS, fonts, images
main.py         main entry
requirements.txt
```

## Notes

This project is still a work in progress. Some pages are unfinished and will be updated over time as I continue rebuilding the website and adding my projects detailed into it :)

If you find a bug or have suggestions, feel free to open an issue.
