from typing import List, Union
from datetime import datetime
import dateparser


class Job:
    def __init__(self, role: str, company: str, location: str, application: str):
        self.role = role
        self.company = company
        self.location = location
        self.application = application

        self.date_posted: Union[datetime, None] = None
        self.compensation: Union[str, None] = None
        self.description: Union[str, None] = None

    def __str__(self):
        return f"""
        Role: {self.role}
        Application: {self.application}

        Company: {self.company}
        Location: {self.location}
        Date Posted: {self.date_posted}
        Description: {self.description}
        Compensation: {self.compensation}
        """

    def identifier(self):
        return f"{self.role} @ {self.company}: {self.application}"

    def set_date_posted(self, date: datetime):
        """
        Convert a string to a datetime object
        """
        self.date_posted = dateparser.parse(date)

    def set_description(self, description: str):
        self.description = description

    def set_compensation(self, compensation: str):
        self.compensation = compensation

    def set_application(self, application: str):
        self.application = application
