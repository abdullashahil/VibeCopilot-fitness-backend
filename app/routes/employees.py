from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List
from app.models.appointment import Appointment, AppointmentUpdate
from app.db.mongodb import get_db

router = APIRouter()

@router.post("/appointments", response_model=Appointment)
async def create_appointment(appointment: Appointment):
    appointment_dict = appointment.model_dump()
    db = get_db()
    result = await db.appointments.insert_one(appointment_dict)
    appointment_dict["_id"] = str(result.inserted_id)
    return appointment_dict


@router.get("/appointments", response_model=List[Appointment])
async def get_all_appointments():
    db = get_db()
    appointments = []
    async for appt in db.appointments.find():
        appt["_id"] = str(appt["_id"])
        appointments.append(Appointment(**appt).model_dump(by_alias=True))
    return appointments

@router.get("/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str):
    db = get_db()
    appt = await db.appointments.find_one({"_id": ObjectId(appointment_id)})
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appt["_id"] = str(appt["_id"])
    return appt

@router.put("/appointments/{appointment_id}", response_model=Appointment)
async def update_appointment(appointment_id: str, appointment: AppointmentUpdate):
    db = get_db()
    update_data = appointment.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")
    
    result = await db.appointments.update_one(
        {"_id": ObjectId(appointment_id)},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    updated_appt = await db.appointments.find_one({"_id": ObjectId(appointment_id)})
    updated_appt["_id"] = str(updated_appt["_id"])
    return updated_appt

@router.delete("/appointments/{appointment_id}")
async def delete_appointment(appointment_id: str):
    db = get_db()
    result = await db.appointments.delete_one({"_id": ObjectId(appointment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment deleted"}