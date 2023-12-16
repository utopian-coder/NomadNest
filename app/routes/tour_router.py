from bson import ObjectId
from fastapi import APIRouter, HTTPException
import json
from ..models.tour_model import Tour

router = APIRouter()

#Create tour
@router.post("/", status_code=201)
def create_tour(name: str, difficulty: str):
    try:
        new_tour = Tour(name=name, difficulty=difficulty)
        new_tour.save()
        return {"status": "success", "tour": new_tour}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#Get all the tours
@router.get("/", status_code=200)
def get_all_tours():
    try:
        tours = json.loads(Tour.objects().to_json())
        return {"status": "success", "tours": tours}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Not Found!")

#Get a tour
@router.get("/{tour_id}", status_code=200)
def get_tour(tour_id):
    try:
        tour = json.loads(Tour.objects.get(id = ObjectId(tour_id)).to_json())
        return {"status": "success", "tour": tour}
    except:
        raise HTTPException(status_code=404, detail="Not Found!")

#update a tour 
@router.patch("/{tour_id}", status_code=200)
def update_tour(tour_id: str, tour: dict):
    name, difficulty = tour.values()
    Tour.objects(id = ObjectId(tour_id)).update(name = name, difficulty = difficulty)
    return {"status": "success", "updated_tour_id": "succesfully updated the tour"}

#Delete a tour
@router.delete("/{tour_id}", status_code=204)
def delete_a_tour(tour_id: str):
    try:
        Tour.objects(id = ObjectId(tour_id)).delete()
        return {"status": "success", "message": "successfully deleted!"}
    except:
        raise HTTPException(status_code=404, detail="Something went wrong, try again!")

#For cleanup after testing
@router.delete("/", status_code=204)
def delete_all_tours():
    Tour.objects().delete()
    return {"status": "success", "message": "successfully deleted all tours!"}