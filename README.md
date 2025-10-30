# Reddit API Data Collection Assignment

This project connects to the Reddit API using **PRAW (Python Reddit API Wrapper)** to collect, process, and export Reddit posts related to finance and investing topics.  
It demonstrates how to securely access APIs, clean and structure data using **pandas**, and create a simple, reproducible data pipeline for analysis.

---

## Assignment Overview
The goal of this project is to build a Python application that interacts with the Reddit API to collect, clean, and store social media data from several subreddits.  
This assignment simulates a real-world data analytics and engineering workflow, where you design a pipeline that gathers, processes, and exports data in a structured format.

The script:
- Connects to the Reddit API using credentials securely stored in an environment file (`reddit.env`)
- Fetches “Hot” posts from multiple subreddits related to finance and investing
- Performs keyword-based searches (e.g., “index fund”) across the same subreddits
- Cleans and merges the collected data into a unified dataset
- Removes duplicates and exports the final dataset as a clean CSV file ready for analysis

---

## Learning Objectives
By completing this project, you will:
- Learn to authenticate and interact with a public REST API
- Use **environment variables** to manage credentials securely
- Apply **pandas** for data cleaning, validation, and export
- Gain experience working with **GitHub** and version-controlled workflows
- Understand how to design a simple, modular data collection pipeline

---

## How to Run

### 1. Prerequisites
- Python **3.8+**
- Internet connection
- Reddit Developer account with:
  - `client_id`
  - `client_secret`
  - `user_agent`

---

### 2. Installation
Install all dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt

