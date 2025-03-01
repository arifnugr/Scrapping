# Garuda Journal Scraper

This repository contains a Python project that scrapes journal data from the **Garuda Kemdikbud** website. The goal of this scraper is to automate the extraction of journal titles from the site and store them in a CSV file for further analysis.

## Table of Contents

1. [Overview](#overview)
2. [Dependencies](#dependencies)
3. [File Structure](#file-structure)
4. [Setup Instructions](#setup-instructions)
5. [Usage](#usage)
6. [How the Scraper Works](#how-the-scraper-works)

## Overview

This project uses **Python** and libraries like **BeautifulSoup** and **requests** to scrape journal data from the **Garuda Kemdikbud** platform. The scraper is designed to automatically:

- Extract journal titles from multiple pages.
- Save them into a CSV file (`raw_data.csv`).
- Dynamically detect the number of pages to scrape, ensuring future scalability for new journal entries.

This project serves as a useful tool to collect and store journal data for further research or analysis.

## Dependencies

In this section, you will find all the external libraries or dependencies required to run the project. Before starting the scraper, you need to install them. Here's what you need:

1. **Python 3.x**: Make sure you have Python installed on your machine.
2. **Required Libraries**: The project relies on the following libraries:
   - `requests`: To send HTTP requests to the Garuda website and retrieve the HTML content.
   - `beautifulsoup4`: To parse and extract journal titles from the HTML content.
   - `csv`: To save the scraped data into a CSV file.
   - `concurrent.futures`: To perform parallel scraping and speed up the process.

To install all dependencies, follow these steps:

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
2. **Install the necessary libraries:
   ```bash
   pip install -r requirements.txt
   
