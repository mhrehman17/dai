# Contribution Guidelines

Thank you for considering contributing to the Decentralized AI System! We welcome contributions from the community to help make this system more robust, efficient, and feature-rich. Please follow the guidelines outlined below to contribute effectively.

## Getting Started

### 1. Fork the Repository
Start by forking the project repository to your GitHub account. You can do this by clicking the "Fork" button at the top of the repository page.

### 2. Clone Your Fork
Clone the repository locally so you can start working on it:
```bash
git clone https://github.com/<your-username>/dai_project.git
```
Replace `<your-username>` with your GitHub handle.

### 3. Create a Branch
Create a branch to work on a new feature, bug fix, or enhancement:
```bash
git checkout -b feature/your-feature-name
```
Give your branch a meaningful name that reflects the purpose of your work.

## Setting Up the Development Environment

### 1. Install Dependencies
Ensure you have all the necessary dependencies by installing the Python packages listed in `requirements_dev.txt`:
```bash
pip install -r requirements_dev.txt
```

### 2. Set Up Environment Variables
Create an `.env` file in the root of the project with the necessary environment variables:
```env
DB_CONNECTION_STRING=<your_database_connection_string>
SECRET_KEY=<your_secret_key>
```

### 3. Run the Application
To run the backend application locally for development, execute the following:
```bash
cd frontend
./run_frontend.sh
```
This will start the FastAPI server and expose the API endpoints.

## Contribution Workflow

### 1. Open an Issue
Before you begin working, it is a good practice to check if an issue already exists. If not, create a new issue describing your feature or bug fix.

### 2. Pull Request Guidelines
Once your feature is ready, push your branch to GitHub and open a Pull Request (PR).
- **Title**: Provide a concise and informative title for your PR.
- **Description**: Include a detailed description of what you changed and why.
- **Linked Issues**: If your PR addresses an issue, mention it in the description (e.g., "Fixes #15").
- **Testing**: Ensure your code is thoroughly tested. Include new unit tests or update existing ones to reflect your changes.

### 3. Review Process
- Your PR will be reviewed by maintainers. Please be prepared to make changes if requested.
- Once your PR is approved, it will be merged into the main branch.

## Code Style
- Follow **PEP8** for Python code style.
- Use descriptive variable and function names.
- Document functions using docstrings, including explanations of parameters and return values.

## Writing Tests
Tests are essential for maintaining a high-quality codebase. The project uses **pytest** for unit testing.
- Place your unit tests in the `core/tests/unit_tests/` directory.
- Make sure that your new feature or bug fix is covered by appropriate tests.
- To run all tests:
  ```bash
  pytest core/tests/
  ```

## Contributing to Documentation
Documentation contributions are highly appreciated. You can improve the documentation by editing files in the `documentation/` directory.
- Update **usage.md** or **api_reference.md** if you make any changes to the API or how users interact with the system.
- Contributions to **architecture.md** or **installation.md** are also welcome for better clarity.

## Security Issues
If you discover a security vulnerability, please do not submit it as an issue. Instead, email the maintainers directly at `security@dai_project.com`.

## Code of Conduct
By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to providing a friendly, safe, and welcoming environment for all.

## Getting Help
If you need help while working on your contribution:
- Check the **troubleshooting.md** file for common problems.
- Join the community discussions on our Slack channel.
- Open a **Discussion** on GitHub to seek assistance from the maintainers and community.

## Acknowledgements
Thank you for helping to make the Decentralized AI System better. Your contributions are what make this project thrive!

---

We look forward to your contributions. Happy coding!

