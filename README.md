# Garuda Journal Scraper

This repository contains a Python project that scrapes journal data from the **Garuda Kemdikbud** website. The goal of this scraper is to automate the extraction of journal titles from the site and store them in a CSV file for further analysis. This README provides detailed instructions on how to set up and run the scraper, as well as an overview of the entire process.

## Table of Contents

1. [Overview](#overview)
2. [Dependencies](#dependencies)
3. [File Structure](#file-structure)
4. [Setup Instructions](#setup-instructions)
5. [Usage](#usage)
6. [How the Scraper Works](#how-the-scraper-works)
7. [Error Handling](#error-handling)
8. [Contributing](#contributing)
9. [License](#license)

## Overview

This project uses **Python** and libraries like **BeautifulSoup** and **requests** to scrape journal data from the **Garuda Kemdikbud** platform. The scraper is designed to extract the journal titles from multiple pages on the website and save them into a CSV file (`raw_data.csv`). The scraper dynamically detects the total number of pages to scrape, so it's ready for future updates when new journals are added.

## Dependencies

Before running the scraper, you'll need to install the required dependencies. This can be done by setting up a virtual environment and installing the necessary packages via **pip**.

1. Install **Python 3.x** if you haven't already.
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
