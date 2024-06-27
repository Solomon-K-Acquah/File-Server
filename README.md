# File Server Project

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#Features)
3. [Tech Stack](#tech-stack)
4. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Application](#running-the-application)
5. [Database Schema](#database-schema)
6. [API Endpoints](#api-endpoints)
7. [Deployment](#deployment)
8. [Contributing](#contributing)
9. [License](#license)

## Project Overview
Lizzy runs a business that distributes documents in the likes of wedding cards, admission forms etc. on behalf of various businesses to different users. All have been moving well, but she desires to scale her business. 
After doing research, she finds that having a digital platform where these can be easily accessed and downloaded remotely is a good solution to the scaling challenge she currently faces. She has found you after 
your relatives in her network defended you to be the right person for the job.

This project aims to develop a digital platform for users to access and download these documents remotely.

## Features

### User Features
1. **Signup & Login**: Users can sign up and log in using email and password. Account verification and password reset features are included.
2. **Feed Page**: Displays a list of downloadable files.
3. **Search**: Users can search for specific files.
4. **Send File via Email**: Users can send files to an email address through the platform.

### Admin Features
1. **Upload Files**: Admin can upload files with a title, description, image and category.
2. **Analytics**: Admin can view the number of downloads and emails sent for each file.

## Tech Stack
- **Backend**: Django, Django Rest Framework
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: PostgreSQL (recommended for production), SQLite (for development)
- **Version Control**: Git, GitHub
- **Deployment**: Heroku/AWS/DigitalOcean
- **Email Service**: Django’s email backend, SMTP server (e.g., Gmail SMTP, SendGrid)

## Getting Started

### Prerequisites

- Python 3.x
- Django 3.x or higher
- PostgreSQL (or SQLite for development)
- Git

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/file-server.git
    cd file-server
    ```



