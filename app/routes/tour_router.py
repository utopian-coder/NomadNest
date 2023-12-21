from bson import ObjectId
from fastapi import APIRouter, HTTPException
import json
from ..models.tour_model import Tour
from pydantic import BaseModel

router = APIRouter()

class TourFields(BaseModel):
    name: str
    description: str
    duration: int
    price: float
    difficulty: str
    ratings_quantity: int
    ratings_average: float

#Create tour
@router.post("/", status_code=201)
def create_tour(request: TourFields):
    name, description, duration, price, difficulty, ratings_quantity, ratings_average = list(request.model_dump().values())
    try:
        new_tour = Tour(
            name=name,
            description=description,
            duration=duration,
            difficulty=difficulty,
            price=price,
            ratings_quantity=ratings_quantity,
            ratings_average=ratings_average
        )
        
        new_tour.save()
        
        return {"status": "success", "tour": new_tour}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#Get all the tours
@router.get("/", status_code=200)
def get_all_tours():
    try:
        tours = json.loads(Tour.objects().to_json())
        return {"status": "success", "numeber_of_tours": len(tours), "tours": tours }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Not Found!")


#get tour stats based on difficulty
@router.get("/stats", status_code=200)
def get_tour_stats_by_difficulty():
    pipeline = [
        {
            "$group": {
                "_id": "$difficulty",
                "number_of_tours": {"$sum": 1},
                "number_of_ratings": {"$sum": "$ratings_quantity"},
                "average_rating": {"$avg": "$ratings_average"},
                "minimum_price": {"$min": "$price"},
                "maximum_price": {"$max": "$price"},
                "average_price": {"$avg": "$price"},
            }
        }
    ]

    tour_stats = Tour.objects().aggregate(pipeline) #returns <class 'pymongo.command_cursor.CommandCursor'>
    tour_stats_list = list(tour_stats)

    return {"status": "success", "stats": tour_stats_list}

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
    
# #For inserting test data into db
@router.post("/create-multiple-tour", status_code=201)
def create_tour(request: list[TourFields]):
    try:
        # If only one item is provided, convert it to a list for consistency
        if not isinstance(request, list):
            request = [request]

        new_tours = []

        for tour_data in request:
            name, description, duration, price, difficulty, ratings_quantity, ratings_average = list(tour_data.model_dump().values())

            new_tour = Tour(
                name=name,
                description=description,
                duration=duration,
                difficulty=difficulty,
                price=price,
                ratings_quantity=ratings_quantity,
                ratings_average=ratings_average
            )

            new_tour.save()
            new_tours.append(new_tour)

        return {"status": "success", "tours": new_tours}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#For cleanup after testing
@router.delete("/", status_code=204)
def delete_all_tours():
    Tour.objects().delete()
    return {"status": "success", "message": "successfully deleted all tours!"}

# class APIFeatures {
#   constructor(query, queryString) {
#     this.query = query;
#     this.queryString = queryString;
#   }

#   filter() {
#     let queryObject = { ...this.queryString };

#     const excludeFields = ["sort", "page", "limit", "fields"];
#     excludeFields.forEach((curr) => delete queryObject[curr]);

#     const queryString = JSON.stringify(queryObject);

#     queryObject = JSON.parse(
#       queryString.replace(/\b(gt|gte|lt|lte)\b/g, (match) => `$${match}`) //\b\b for this to run when matches exactly, and g for replacing all
#     );

#     this.query = this.query.find(queryObject);

#     return this;
#   }

#   sort() {
#     if (this.queryString.sort) {
#       const sortBy = this.queryString.sort.split(",").join(" ");
#       this.query = this.query.sort(sortBy);
#     } else {
#       this.query = this.query.sort("-createdAt");
#     }

#     return this;
#   }

#   limitFields() {
#     if (this.queryString.fields) {
#       const fields = this.queryString.fields.split(",").join(" ");
#       this.query = this.query.select(fields);
#     } else {
#       this.query = this.query.select("-__v");
#     }

#     return this;
#   }

#   paginate() {
#     const page = this.queryString.page * 1 || 1;
#     const limit = this.queryString.limit || 5;
#     const skip = (page - 1) * limit;

#     this.query = this.query.skip(skip).limit(limit);

#     return this;
#   }
# }

# module.exports = APIFeatures;
