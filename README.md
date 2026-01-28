# Habit Tracker API

A FastAPI-based REST API for tracking daily habits, managing streaks, and building better routines. Build, track, and maintain your habits with ease.

## Features

- **Create Habits**: Define new habits with custom frequencies and reminders
- **Track Progress**: Log daily completions and maintain habit streaks
- **Streak Management**: Automatically calculate latest and longest streaks
- **Flexible Scheduling**: Support for daily habits or specific days of the week
- **Update Habits**: Modify habit details anytime
- **Delete Habits**: Remove habits you no longer need
- **Persistent Storage**: All data saved to JSON for reliable persistence

## Getting Started

### Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic

### Installation

```bash
pip install fastapi uvicorn pydantic
```

### Running the Server

```bash
python -m uvicorn main:app --reload --port 8080
```

The API will be available at `http://localhost:8080`

**Interactive API Documentation**: Visit `http://localhost:8080/docs` for Swagger UI

## Data Schema

### Habit Model

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier (e.g., "H001") |
| habit | string | Habit name |
| description | string | Habit description |
| frequency | string | "Daily" or day name (Mon-Sun) |
| start_date | date | First completion date |
| reminder_time | string | Reminder time in HH:MM format |
| logs | list[date] | List of completion dates |
| latest_streak | int | Current consecutive completions |
| longest_streak | int | Best consecutive completions |

## Usage Examples

### Create a New Habit
```bash
curl -X POST "http://localhost:8080/newhabit" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "H001",
    "habit": "Morning Walk",
    "description": "Walk for at least 20 minutes",
    "frequency": "Daily",
    "reminder_time": "06:30"
  }'
```

### Track a Habit
```bash
curl -X PUT "http://localhost:8080/track/H001?check=true"
```

### View All Habits
```bash
curl "http://localhost:8080/myhabits"
```

## Project Structure

```
FastAPI/
├── main.py           # FastAPI application with all endpoints
├── schema.py         # Pydantic models for validation
├── utils.py          # Utility functions (file I/O, calculations)
├── tracker.json      # Persistent data storage
└── README.md         # This file
```

## Technical Details

### Validation
- Habits must have unique IDs
- Valid frequencies: Daily, Mon, Tue, Wed, Thu, Fri, Sat, Sun
- Tracking dates cannot be before habit start date or in the future
- Cannot track the same date twice
- Weekly habits can only be tracked on specified days

### Streak Calculation
- **Latest Streak**: Current consecutive completions
- **Longest Streak**: Best consecutive completions ever achieved
- Streaks automatically reset when a day is missed
- Considers frequency when calculating consecutive dates
