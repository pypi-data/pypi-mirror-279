#! ./venv/bin/python3
import typer
from typing_extensions import Annotated
from rich.console import Console
from rich.table import Table

from datetime import datetime, timedelta

from common.TimeEntry import TimeEntry
from common.TimeSheet import TimeSheet

import common.prompt_checking as pc

app = typer.Typer()
console = Console()

@app.command()
def enter():

    time_entry = None

    start_date_string = pc.validated_prompter("Start Date", pc.check_date_entry)
    start_time_string = pc.validated_prompter("Start Time", pc.check_time_entry)

    time_entry = TimeEntry(start_date_string, start_time_string)

    task_end_type = pc.validated_prompter("Duration (type 'd') or DateTime (time 't')", pc.check_end_selection)

    if task_end_type == "d":
        duration_string = pc.validated_prompter("Duration", pc.check_duration)
        time_entry.set_duration(duration_string)

    elif task_end_type == "t":
        end_date = pc.validated_prompter("End Date", pc.check_date_entry)
        end_time = pc.validated_prompter("End Time", pc.check_time_entry)
        time_entry.set_end_ts(end_date, end_time)

    description = pc.validated_prompter("Description", None)
    print(description)
    client = pc.validated_prompter("Client", None)
    category = pc.validated_prompter("Category", None)

    time_entry.set_note(description)
    time_entry.set_client(client)
    time_entry.set_category(category)

    timesheet = TimeSheet()
    timesheet.insert_time_entry(time_entry)

@app.command()
def show():

    timesheet = TimeSheet()

    table = Table("start ts", "duration (hrs)", "end ts", "description", "client")
    for row in timesheet.get_time_entries():
        start_ts, duration_sec, end_ts, description, category, client = row
        duration_hrs = round(duration_sec/3600, 5)
        # 2024-05-28 12:00:00

        start_ts = datetime.strptime(start_ts, '%Y-%m-%d %H:%M:%S').strftime("%d/%m/%Y %H:%M")
        end_ts = datetime.strptime(end_ts, '%Y-%m-%d %H:%M:%S').strftime("%d/%m/%Y %H:%M")

        table.add_row(start_ts, str(duration_hrs), end_ts, description, client)
    console.print(table)

@app.command()
def version():
    print("V0.1.1")

if __name__ == "__main__":
    app()
