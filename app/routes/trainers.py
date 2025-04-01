from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List
from app.models.appointment import Status, Appointment, StatusUpdate
from app.db.mongodb import get_db
from fastapi import Body

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
    
    # Get existing appointment
    existing_appt = await db.appointments.find_one({"_id": ObjectId(appointment_id)})
    if not existing_appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    update_values = {"status": update_data.status}

    # Handle time setting for approved appointments
    if update_data.status == Status.APPROVED:
        if not update_data.time:
            raise HTTPException(
                status_code=400,
                detail="Time is required when approving appointments"
            )

        # Combine existing date with new time
        hours, minutes = map(int, update_data.time.split(':'))
        new_time = existing_appt["date"].replace(
            hour=hours,
            minute=minutes,
            second=0,
            microsecond=0
        )
        update_values["date"] = new_time

    # Update database
    result = await db.appointments.update_one(
        {"_id": ObjectId(appointment_id)},
        {"$set": update_values}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")

    updated_appt = await db.appointments.find_one({"_id": ObjectId(appointment_id)})
    return Appointment(**updated_appt)