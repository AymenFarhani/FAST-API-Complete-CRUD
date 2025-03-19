from io import BytesIO

import pandas
from sqlalchemy.orm import Session
import pandas as panda
import models

def export_projects_to_excel(db: Session):
    # Fetch all projects
    projects = db.query(models.Project).all()

    # Convert data into a list of dictionaries
    data = [
        {
            "ID": project.id,
            "Title": project.title,
            "Description": project.description,
            "Start Date": project.start_date,
            "Status": project.status
        }
        for project in projects
    ]

    # Convert to DataFrame
    df = panda.DataFrame(data)

    # Create an in-memory Excel file
    output = BytesIO()
    with panda.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Projects")

    output.seek(0)  # Move pointer to the start of the file
    return output
