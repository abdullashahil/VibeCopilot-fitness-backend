from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List
from app.models.appointment import Status, Appointment, StatusUpdate
from app.db.mongodb import get_db
from fastapi import Body
from datetime import datetime

router = APIRouter()

@router.get("/appointments", response_model=List[Appointment])
async def get_all_appointments():
    db = get_db()
    appointments = []
    async for appt in db.appointments.find():
        appt["_id"] = str(appt["_id"])
        appointments.append(appt)
    return appointments


@router.patch("/appointments/{appointment_id}/status", response_model=Appointment)
async def update_status(
    appointment_id: str, 
    update_data: StatusUpdate = Body(...)
):
    db = get_db()
    
    existing_appt = await db.appointments.find_one({"_id": ObjectId(appointment_id)})
    if not existing_appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    update_values = {"status": update_data.status}

    if update_data.status == Status.APPROVED:
        if not update_data.time:
            raise HTTPException(
                status_code=400,
                detail="Time is required when approving appointments"
            )
        
        try:
            # Parse and combine date/time
            original_date = existing_appt["date"]
            hours, minutes = map(int, update_data.time.split(':'))
            new_datetime = datetime.combine(
                original_date.date(),
                datetime.min.time().replace(hour=hours, minute=minutes)
            )
            update_values["date"] = new_datetime
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid time format. Use HH:MM"
            )

    result = await db.appointments.update_one(
        {"_id": ObjectId(appointment_id)},
        {"$set": update_values}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")

    updated_appt = await db.appointments.find_one({"_id": ObjectId(appointment_id)})
    return Appointment(**updated_appt)