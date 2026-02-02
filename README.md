# 📊 knime-linkedin-pipeline

Python pipeline to extract LinkedIn Analytics demographic data using **Playwright** and export it into **KNIME** for further analysis.

---

## 🚀 What this project does

This script automates the collection of audience insights:

* **Logs into LinkedIn:** supports manual or automatic login.
* **Navigates:** goes directly to the LinkedIn Analytics demographics page.
* **Extracts percentage-based demographic data such as:**
  * Job title
  * Location
  * Industry
  * Seniority
  * Company size
  * Function
* **Outputs:** the data as a table directly into KNIME.

---

## 🧰 Tech stack

* **Python**
* **Playwright**
* **Pandas**
* **KNIME** (Python Scripting node)

---

## 📦 Installation

This project uses **uv** for dependency management.
```bash
uv add playwright pandas
uv run playwright install chromium
```

---

## ▶️ How to run

The script is intended to be executed inside a KNIME Python Script node.

1. Open KNIME
2. Add a Python Script node
3. Point the node to this project environment
4. Run `main.py`
5. Login manually to LinkedIn if required
6. Output: The data will be available as a KNIME table.

---

## 🎥 Demo

You can find a full demo and explanation in this video:

[![Watch the demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

---

## ⚠️ Disclaimer

This project is for educational and personal analytics purposes only. Use responsibly and respect LinkedIn's terms of service.
