# Bibliotech. Online Library Management
***vgupe2024_team2***
[Overleaf LaTeX report](https://www.overleaf.com/read/vnwzxfkpcztz#cff629)

## Table of Contents
1. [Table of Contents](#table-of-contents)
2. [Team members](#team-members)
3. [How to Install and Run the Package](#how-to-install-and-run-the-package)
4. [File Structure](#file-structure)
5. [System Design](#system-design)
6. [UI Display](#ui-display)
8. [License](#license)

## Team members
| Full Name    | Student's ID  |
| ------------ | ------------- |
| [Huỳnh Lê An Phú](https://github.com/TheFabulousP) | 10421100 |
| [Đỗ Minh Quang](https://github.com/minWang916) | 10421051 |
| [Lê Công Nguyên](https://github.com/lcnguyencs) | 10421043 |
| [Dương Thiên Hương](https://github.com/dxd1019) | 10421019 |
| [Phan Tâm Như](https://github.com/nhuhuynh1508) | 10421122 |
| [Nguyễn Minh Anh](https://github.com/sumirez) | 10421068 |

## Project Description
### Overview
The Online Library Management Application is a comprehensive system designed to facilitate the rental, review, and management of books through a user-friendly interface. The application supports three primary roles: Users, Moderators, and Admins.

### Features
- **User Interface**:
    - **Browse and Filter**: Users can browse books, filter them by categories, authors, publications, etc.
    - **Rent Books**: Users can rent books for a specified duration.
    - **Review and Like**: Users can like and review books.
    - **Moderator Application**: Users can apply to become moderators.

- **Moderator Interface**:
    - **Book Management**: Moderators can list and manage books, track their availability, and send notifications when leases expire.
    - **Approval Process**: Moderators submit books for admin approval before they become available to users.

- **Admin Role**:
    - **Approval**: Admins approve books submitted by moderators, ensuring quality and compliance.

### Technologies Used
- **Backend**:
    - **Django and Python**: Chosen for their robustness, scalability, and the extensive online resources available for development support. Django's built-in admin interface simplifies administrative tasks, making it an ideal choice for managing complex database operations and user roles.
- **Frontend**:
    - **Webflow**: Utilized to streamline the design-to-production process, allowing for rapid prototyping and a polished user interface. Webflow's visual editor makes it easy to create responsive designs without extensive front-end coding.

### Deployment page
You can find our deployment using Railway Production [here](https://vgupe2024team2clone-production.up.railway.app/).

### Project Timeline
Our timeline for the project has been described in the report. However, this is the actual link where we detail the goals and achievements for each week. See Notion link [here](https://lcnguyencs.notion.site/Schedule-96c5328274bc4e1b817b2768dd6da224)

### Project Report
[Overleaf LaTeX report](https://www.overleaf.com/read/vnwzxfkpcztz#cff629)

We also include a pdf version on our GitHub repo [here](.document/report/Bibliotech_report.pdf).

## How to install and run the package
### Prequisites
- **Python 3.9 or higher:** Ensure Python is installed on your system. Our team use Python 3.9 to implement this project.
- **sqlite3:** Required for database view and management (optional).
- **docker:** For containerssation and deployment

### Installation Steps
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/galvdat-hthieu/vgupe2024_team2.git
   cd vgupe2024_team2
   ```

2. **Install Required Packages:**
   Our team has already included a file named 'requirements.txt' that contained all packages needed to run this project smoothly. To install
the file, execute the following command in the terminal:
   ```sh
   pip install -r requirements.txt

### Running the Project
To run the project, execute the following command in the terminal:
```sh
python manage.py runserver
```
Or using Docker command:
```sh
docker-compose up
```

## File Structure
The following outlines is the hierarchical structure of our project, generalizing the organization of directories and files. This structure is designed to facilitate ease of development, maintenance, and deployment.
<details>
<summary>📦 vgupe2024_team2</summary>

```
├─ .document
│  └─ diagrams: Contains diagrams related to the project.
├─ Bibliotech
├─ control: contains configurations, views, URL mappings, models, and migration files essential for these operations.
├─ front-end template
|  └─ images: Contains image assets used in the front-end of the project.
├─ home: This directory represents the landing page or main interface components of the application.
├─ media: Media files related to books and users
├─ moderator: manage moderator functionalities, including handling forms, URL routing, views, and administrative tasks related to user and book moderation
├─ old database: older version of database that contains book records and accounts
├─ social platform: integrating and managing social account functionalities, including URL routing, views, and model definitions for user interactions on social platforms
├─ static: organizes and stores all static assets like CSS, JavaScript, and images, categorized into subdirectories for different parts of the web application
├─ templates: contains HTML templates organized into subdirectories for different parts of the web application, ensuring a clean structure for rendering dynamic content across various views
├─ user:  managing user-related functionalities, including user registration, authentication, form handling, URL routing, and administrative tasks. 
├─ Dockerfile and docker-compose.yaml: Configuration file for building a Docker image of the project, for defining and running multi-container Docker applications.
├─ manage.py: Django’s command-line utility for administrative tasks.
├─ requirements.txt: List of Python dependencies required for the project.
├─ db.sqlite3: SQLite database file.
└─ README.md: Markdown file providing an overview and documentation of the project.
```
</details>

## System Design
### System Requirement
Our project will focus on the following set of requirements while designing the Online Library Management:

1. Any library user should be able to search books by their title, author, subject category as well by the publication date.
2. Each book will have a unique identification number and other details which will help to physically locate the book.
3. There could be more than one copy of a book, and library users should be able to check-out and reserve any copy.
4. The admin should be able to retrieve information like who took a particular book or what are the books checked-out by a specific library user.
5. There should be a maximum limit (14) on how many days a user can keep a book.
6. The user will receive an email informing them when a book has been approved by the admin to be checked out.

### Use Case Diagrams
Our team have four actors in our system:
- Administrator (Admin): The admin is in charge of adding and modifying books, book items, and users. 
- User: The user can search the catalog, as well as checkout, reserve, renew, return a book, leave a review, etc.
- System: The system is responsible for sending notifications about the latest news onsite and update the status of the service that the users are currently using.
- Guest: The guest can access the webpage to view its content such as latest news from the library, the regulation or the FAQ. 

<a href=".document/diagrams/usecase/usecase-Guest.drawio.png">Use case diagram for guest</a>

<a href=".document/diagrams/usecase/usecase-User.drawio.png">Use case diagram for registered user</a>

<a href=".document/diagrams/usecase/usecase-Moderator.drawio.png">Use case diagram for moderator</a>

<a href=".document/diagrams/usecase/usecase-Admin.drawio.png">Use case diagram for admin</a>

### Sequence Diagram
Here are the following sequence diagrams to illustrate various functions within our project: 

<a href=".document/diagrams/sequence/sequence_guest.png">Sequence diagram for guest functions: contact, search book, view books, read FAQs</a>

<a href=".document/diagrams/sequence/sequence_register.png">Sequence diagram for "register" function</a>
<a href=".document/diagrams/sequence/sequence_login.png">Sequence diagram for "login" function</a>
<a href=".document/diagrams/sequence/sequence_addbook.png">Sequence diagram for "add book" function</a>

<a href=".document/diagrams/sequence/Review.svg">Sequence diagram for "user's book review" function</a>

### E-R Diagram
Below is the E-R diagram to demonstrate about our database throughout the project:

<a href=".document/ER-diagram.png">E-R Diagram</a>

### Deployment Diagram
Below is the deployment diagram to demonstrate about our database throughout the project:

Below is the link to the component diagram of our prroject.

<a href=".document/diagrams/deployment/usecase-Deployment.png">Deployment Diagram</a>

### Component Diagram
Below is the link to the component diagram of our prroject.

<a href=".document/diagrams/component/usecase-Component.drawio.png">Component Diagram</a>

## UI Display
Below is the link where we make a list of our UI display and to keep track of our work.

See our prototypes here on [our Notion dashboard](https://lcnguyencs.notion.site/Tasks-for-reference-cc3fbe582dcb4f9d91675ce3e0b5d486)

## License
MIT License
