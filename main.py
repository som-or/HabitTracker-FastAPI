from fastapi import FastAPI, Path ,HTTPException, Query 
import json
from pydantic import BaseModel, Field, computed_field, field_validator, model_validator
from typing import Annotated, Optional,List
from datetime import date, datetime, time, timedelta
from utils import load_data, save_data, habit2dict, streak_calculation
from schema import Habit, EditHabit, CreateHabit, TrackHabit

app=FastAPI()

#welcome page
@app.get("/")
def Welcome():
    return {"message": "Track your habits!"}

#Retreive all habits
@app.get("/myhabits")
def ViewAllHabits():
    habits=load_data()

    return habits

#Retreive habit by its Id
@app.get("/myhabits/{habit_id}")
def ViewHabit(habit_id:str=Path(..., description="Retreive habit by its Id", examples=["H001"])):

    data=load_data()
    if habit_id in data:
        return data[habit_id]

    raise HTTPException(status_code=404, detail="habit not found")

#create new habit 
@app.post("/newhabit")
def CreateHabit(habit: CreateHabit):
    data=load_data()

    if habit.id in data:
        raise HTTPException(status_code=409, detail="habit id already present")
    
    habit_dump=habit.model_dump()
    verified_habit=Habit(**habit_dump)
    
    data[habit.id]=habit2dict(verified_habit,exclude={'id'})

    save_data(data)

    return f"New Habit with id:{habit.id} saved successfully"

#edit habit details
@app.put("/edithabit/{habit_id}")
def EditHabit(habit: EditHabit, habit_id: str=Path(..., description="habit id that needs to be edited")):
    data=load_data()
    edit_habit=habit.model_dump(exclude_unset=True)
    
    if habit_id not in data:
        raise HTTPException(status_code=404, detail="habit id not present")
    if not edit_habit:
        raise HTTPException(status_code=400, detail="nothing to update")
    
    change_habit=data[habit_id].copy()

    for k, v in edit_habit.items():
        change_habit[k]=v
    
    change_habit['id']=habit_id
    verify_updates=Habit(**change_habit)

    updated_habits=habit2dict(verify_updates,exclude={'id'})
    data[habit_id]=updated_habits
    
    save_data(data)
    return f"Habit Id:{habit_id} successfully edited"

#delete a habit 
@app.delete("/delete/{habit_id}")
def DeleteHabit(habit_id: str=Path(..., description="delete the Habit of the given id")):
    data=load_data()

    if habit_id not in data:
        raise HTTPException(status_code=404, detail="habit id not found")
    
    del data[habit_id]

    save_data(data)
    return f"Habit with Id:{habit_id} deleted successfully"

#track the habit streak
@app.put("/track/{habit_id}")
def Track(check: bool=Query(default=True, description="mark done/undone"), habit_id: str=Path(...,description="Habit ID to track"), date2track: Optional[date]=Query(default=None, description="Date to track (YYYY-MM-DD). Defaults to today.")):
    data=load_data()

    track_date=date2track or date.today()

    if habit_id not in data:
        raise HTTPException(status_code=404, detail="habit id not found")

    track_habit=data[habit_id].copy()
    track_habit['id']=habit_id

    valid_input=TrackHabit(habit=track_habit, track_date=track_date)

    logs=list(valid_input.habit.logs)
    freq=valid_input.habit.frequency

    if check and track_date in logs:
        raise HTTPException(status_code=409, detail='already tracked for this date')
    if not check and track_date not in logs:
        raise HTTPException(status_code=409, detail='no log to uncheck for this date')
    
    if valid_input.habit.start_date is None:
        track_habit['start_date']=track_date

    if check:
        logs.append(track_date)
    else:
        logs.remove(track_date)
 
    logs.sort(reverse=True)

    lo=valid_input.habit.longest_streak
    la=valid_input.habit.latest_streak
    longest_streak, latest_streak=streak_calculation(logs, track_date, freq, check, lo, la)

    track_habit['logs']=logs
    track_habit['longest_streak']=longest_streak
    track_habit['latest_streak']=latest_streak

    track_habit_validate = Habit(**track_habit)

    track_habit_dump=habit2dict(track_habit_validate,exclude={'id'})
    
    data[habit_id]=track_habit_dump
    save_data(data)
    
    return f"Updated the streak count for habit id:{habit_id}"


                



            


    

