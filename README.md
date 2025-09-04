# Diet Tracker

This is a personal diet tracking application built in Python. It logs weekly metrics, meals, activity data, and emotional reflections to support metabolic discipline and long-term health transformation.

## Features

- Add weekly entries with weight, body fat %, BMI, BMR, visceral fat, muscle mass, bone mass, protein %, water %, and skeletal muscle.
- Log meals with macro breakdowns (calories, protein)
- Track physical activity (miles walked, length of time walked, calories burned, average heart rate, and steps)
- Record emotional reflections for each day
- Future plans: CSV export, average rate calculations, and real-time summaries

### 📦 Weight Tracking Summary Tool

This module was added as a personal enhancement. It wasn’t part of the original roadmap, but I was manually reviewing weekly weight logs and behavioral trends, so I decided to formalize the process.

The tool includes:

- Metric-by-metric summaries (weight, fat %, muscle, hydration, etc.)
- Weekly and daily weight change calculations
- Rolling 7-day deltas
- Milestone detection (every 10 lbs from 260 down)
- Visual dashboard using `matplotlib`
- CSV export for spreadsheet analysis

> **Note:** This module was co-developed with the help of AI (Microsoft Copilot). It accelerated the buildout and helped modularize logic I was already applying manually. While designed for personal use, others may find it useful for tracking progress or visualizing health metrics.

## Why I Built This

This project reflects my own journey through VLCD compliance, metabolic recovery, and emotional clarity. It’s not just code—it’s a living artifact of discipline, frustration, and growth. I built it from scratch to learn how to structure Python programs and apply them to real-world routines.

## Status

Currently in development. Core data entry functions are being scaffolded. Future features will include summary analytics and file output.

## Data Sources

All metrics and activity data are recorded using real-world tools:

- **BeWell Scale**: Used for weekly body composition metrics including weight, body fat %, visceral fat, muscle mass, bone mass, and more.
- **Samsung Galaxy Watch6**: Used to track daily walks, including distance, duration, average heart rate, calories burned, and step count.

These devices provide consistent, structured data that feeds into the tracker. The program is designed to be flexible—users can adapt it to their own gear and measurement routines.

## How to Use

Run the program in terminal and follow the prompts to enter daily data. All entries are stored in memory or written to file (depending on version).

## Quick Start

To begin tracking:

1. Clone the repository
2. Run `main.py` in your terminal
3. Follow the prompts to log metrics, meals, and activity

## Design Philosophy

This project follows a modular design approach. Each core function—such as metric parsing, food logging, activity tracking, and timestamp handling—is separated into its own file. This simplifies debugging, keeps each module focused, and makes future upgrades easier to manage.

### Module Overview

- `parse_metrics.py` — handles unit tagging and timestamp integration
- `log_metrics.py` — handles user input for scale data
- `timestamp.py` — provides reusable date/time logic
- `food.py` — logs meals with macro breakdowns and satiety tagging
- `activity.py` — tracks physical movement, heart rate, and emotional reflections

## License

This project is for personal use and educational exploration.  
Feel free to fork, adapt, or build your own version.

## Contributions

Built solo as a learning artifact.  
No external contributions planned at this time.

---

Built with sweat, discipline, and a few broken egg yolks.
