# Ethos Server-Side Repository

## Overview

**Ethos** is an application designed to track and evaluate experiences and opinions related to corporations, politicians, contractors, individuals, and more. It provides users with a versatile platform to manage and share feedback, aiding in informed decision-making and transparency.


## Features

- **Profile Management**: Create and manage profiles for entities such as contractors, corporations, and individuals.
  
- **Ethos Score**: Each profile includes an Ethos Score updated based on user feedback.

- **Experience Logging**: Document experiences with profiles, including descriptions, dates, and score impacts.

- **Circles**: Organize profiles into 'circles,' allowing shared access and collaboration on profiles and logs.


## User Description
- Use Case: Corporate users leverage Ethos to track and evaluate their experiences with contractors and service providers. By documenting and reviewing feedback, they can make informed decisions on whether to continue working with these entities or select new ones.
- Use Case: Individual users utilize Ethos to monitor and assess the actions and policies of corporations and politicians. By keeping detailed records of their experiences and observations, they can better decide which organizations and leaders align with their values and which ones to avoid. This empowers them to support ethical and responsible entities, contributing to more informed civic and consumer choices.


## Links and Resources
- project board: https://github.com/users/tatianabarga/projects/5/views/1?pane=issue&itemId=70796528
- postman documentation: https://documenter.getpostman.com/view/30237001/2sAXjJ4s76
- ERD: https://drawsql.app/teams/tatiana-bargas-team/diagrams/ethos


## Tech Stack
- Python
- DRF


## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/ethos-server.git
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configuration**:
   Create a `.env` file in the root directory and configure the necessary environment variables. Refer to `.env.example` for a sample configuration.

6. **Run the Server**:
   ```bash
   python app.py
   ```

7. **Database Migration**:
   Set up the database by running the migration scripts:
   ```bash
   python manage.py migrate
   ```


