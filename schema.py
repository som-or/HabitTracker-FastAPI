from pydantic import BaseModel, Field, computed_field, field_validator, model_validator
from typing import Annotated, Optional,List
from datetime import date, time

#example
# "H001": {
    # "habit": "Morning Walk",
    # "description": "Walk for at least 20 minutes every morning.",
    # "frequency": "Daily",
    # "start_date": "2023-01-01",
    # "end_date": "2023-01-07",
    # "reminder_time": "06:30",
    # "logs": [
    #   "2023-01-01",
    #   "2023-01-02",
    #   "2023-01-03",
    #   "2023-01-04",
    #   "2023-01-05",
    #   "2023-01-06",
    #   "2023-01-07"
    # ],
    # "latest_streak": 7,
    # "longest_streak": 7

class Habit(BaseModel):
    
    id : Annotated[str, Field(..., description="Unique identifier for each habit", examples=['H001'])]
    habit :Annotated[str, Field(..., description="Name of the habit")]
    description :Annotated[str, Field(..., description="Description of the habit")]
    frequency :Annotated[str, Field(..., description="Daily or day-of-week (Mon..Sun)", examples=['Daily', 'Mon'])]
    start_date :Annotated[Optional[date], Field(default=None, description="Date you started the habit")]
    reminder_time :Annotated[str, Field(..., description="Reminder time")]
    logs : Annotated[Optional[List[date]], Field(default=[], description="logs of dates the habit is done")]
    latest_streak : Annotated[int, Field(default=0, description="Latest streak")]
    longest_streak : Annotated[int, Field(default=0, description="Longest streak")]
    
    @field_validator('frequency', mode='after')
    @classmethod
    def frequencyVal(cls, value):
        valid_freq=['Daily', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        if value not in valid_freq:
            raise ValueError('not valid frequency')
        return value 
    
    @field_validator('logs',mode='after')
    @classmethod
    def logsVal(cls, value):
        value.sort(reverse=True)
        return value
    
    @model_validator(mode='after')
    def startdateVal(self):
        if self.logs:
            self.start_date=self.logs[-1]
        else:
            self.start_date=None
        return self

class CreateHabit(BaseModel):
    
    id : Annotated[str, Field(..., description="Unique identifier for each habit", examples=['H001'])]
    habit :Annotated[str, Field(..., description="Name of the habit")]
    description :Annotated[str, Field(..., description="Description of the habit")]
    frequency :Annotated[str, Field(..., description="Daily or day-of-week (Mon..Sun)", examples=['Daily', 'Mon'])]
    reminder_time :Annotated[str, Field(..., description="Reminder time")]

class EditHabit(BaseModel):
    habit :Annotated[Optional[str], Field(default=None, description="Name of the habit")]
    description :Annotated[Optional[str], Field(default=None, description="Description of the habit")]
    frequency :Annotated[Optional[str], Field(default=None, description="Daily or day-of-week (Mon..Sun)", examples=['Daily', 'Mon'])]
    reminder_time :Annotated[Optional[str], Field(default=None, description="Reminder time")]


class TrackHabit(BaseModel):
    habit : Annotated[Habit, Field(..., description="habit")]
    track_date: Annotated[date, Field(default_factory=date.today())]

    @model_validator(mode='after')
    def trackdateVal(self):
        if self.habit.start_date is not None and self.track_date<self.habit.start_date:
            raise ValueError('date before start date not allowed')
        
        elif self.track_date>date.today():
            raise ValueError('cannot track future date')

        return self
    
    @model_validator(mode='after')
    def freqDateMatch(self):
        freq=self.habit.frequency
        if freq!='Daily':
            if self.track_date.strftime("%a")!=self.habit.frequency:
                raise ValueError("habit not set for this day of the week")
        
        return self
    



# class Habit(BaseModel):
#     id : Annotated[str, Field(..., description="Unique identifier for each habit", examples=['H001'])]
#     habit :Annotated[str, Field(..., description="Name of the habit")]
#     description :Annotated[str, Field(..., description="Description of the habit")]
#     frequency :Annotated[str, Field(..., description="Daily or day-of-week (Mon..Sun)", examples=['Daily', 'Mon'])]
#     start_date :Annotated[Optional[date], Field(default=None, description="Date you started the habit")]
#     reminder_time :Annotated[str, Field(..., description="Reminder time")]
#     logs : Annotated[Optional[List[date]], Field(default=[], description="logs of dates the habit is done")]

#     @computed_field
#     @property
#     def latest_streak(self)-> int:
#         f=1 if self.frequency=="Daily" else 7
#         st_c=1
#         if self.logs:
#             for l1, l2 in zip(self.logs,self.logs[1]):
#                 if l1-l2==f:
#                     st_c+=1
#                 else:
#                     break
                
#             return st_c     
#         return 0
    
#     @computed_field
#     @property
#     def longest_streak(self)-> int:
#         if self.end_date is not None and self.start_date is not None:
#             d=(self.end_date-self.start_date).days +1
#             return d
#         return 0
    
#     @model_validator(mode='after')
#     def logs_Val(self):
#         if self.start_date is not None:
#             if self.end_date is not None and self.end_date<self.start_date:
#                 raise ValueError('last date cannot be before start date')
#             if self.end_date is None:
#                 self.end_date=self.start_date
#         if self.start_date is None:
#             self.end_date=None

#         return self
    
    
#     @field_validator('frequency', mode='after')
#     @classmethod
#     def frequencyVal(cls, value):
#         valid_freq=['Daily', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

#         if value not in valid_freq:
#             raise ValueError('not valid frequency')
        
#         return value 

# class UpdateHabit(BaseModel):
#     habit :Annotated[str, Field(default=None, description="Name of the habit")]
#     description :Annotated[str, Field(default=None, description="Description of the habit")]
#     frequency :Annotated[str, Field(default=None, description="Daily or day-of-week (Mon..Sun)", examples=['Daily', 'Mon'])]
#     start_date :Annotated[Optional[date], Field(default=None, description="Date you started the habit")]
#     reminder_time :Annotated[str, Field(default=None, description="Reminder time")]

   