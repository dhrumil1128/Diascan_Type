from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import joblib
import traceback

app = FastAPI()

# CORS to allow frontend access (localhost dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------- MODELS TO LOAD ---------------------

# Load diabetes type classifier
type_model = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\type_model.pkl")
le_type = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\le_type.pkl")  # Label encoder for diabetes type

# Label encoders
le_heart = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\le_heart.pkl")
le_kidney = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\le_kidney.pkl")
le_nerve = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\le_nerve.pkl")
le_eye = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\le_eye.pkl")
le_complication = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\le_complication.pkl")

# Complication Models
# ------------------- TYPE 1 MODELS -------------------
model_t1_heart = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\Type 1 Diabetes_Heart_Disease_model.pkl")
model_t1_kidney = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\Type 1 Diabetes_Kidney_Issues_model.pkl")
model_t1_nerve = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\Type 1 Diabetes_Nerve_Damage_model.pkl")
model_t1_eye = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\Type 1 Diabetes_Eye_Problems_model.pkl")
model_t1_complication = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\Type 1 Diabetes_complication_model.pkl")

# ------------------- TYPE 2 MODELS -------------------
model_t2_heart = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\Type 2 Diabetes_Heart_Disease_model.pkl")
model_t2_kidney = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\Type 2 Diabetes_Kidney_Issues_model.pkl")
model_t2_nerve = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\Type 2 Diabetes_Nerve_Damage_model.pkl")
model_t2_eye = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\Type 2 Diabetes_Eye_Problems_model.pkl")
model_t2_complication = joblib.load(r"C:\Users\Dhrumil\Desktop\diabetes-classifier\Backend\saved_models\Type 2 Diabetes_complication_model.pkl")

# --------------------- INPUT MODEL ---------------------

class InputData(BaseModel):
    Age: float
    BMI: float
    Fasting_Glucose: float
    HbA1c: float
    C_Peptide: float
    Insulin_Level: float
    Autoantibody_Presence: int


@app.post("/predict")
def predict(input: InputData):
    try:
        # Create input array
        features = np.array([
            input.Age,
            input.BMI,
            input.Fasting_Glucose,
            input.HbA1c,
            input.C_Peptide,
            input.Insulin_Level,
            input.Autoantibody_Presence
        ]).reshape(1, -1)

        # Predict Diabetes Type
        type_pred = type_model.predict(features)
        diabetes_type = le_type.inverse_transform(type_pred)[0]

        # Select model set based on diabetes type
        if diabetes_type == "Type 1 Diabetes":
            heart_pred = le_heart.inverse_transform(model_t1_heart.predict(features))[0]
            kidney_pred = le_kidney.inverse_transform(model_t1_kidney.predict(features))[0]
            nerve_pred = le_nerve.inverse_transform(model_t1_nerve.predict(features))[0]
            eye_pred = le_eye.inverse_transform(model_t1_eye.predict(features))[0]
            complication_pred = le_complication.inverse_transform(model_t1_complication.predict(features))[0]
        else:  # Type 2 Diabetes
            heart_pred = le_heart.inverse_transform(model_t2_heart.predict(features))[0]
            kidney_pred = le_kidney.inverse_transform(model_t2_kidney.predict(features))[0]
            nerve_pred = le_nerve.inverse_transform(model_t2_nerve.predict(features))[0]
            eye_pred = le_eye.inverse_transform(model_t2_eye.predict(features))[0]
            complication_pred = le_complication.inverse_transform(model_t2_complication.predict(features))[0]

        # Dummy Probability - you can replace with actual if models support it
        overall_probability = 66.0  # for now, static or set from model output if supported

        return {
            "Diabetes_Type": diabetes_type,
            "Heart_Disease": heart_pred,
            "Kidney_Issues": kidney_pred,
            "Nerve_Damage": nerve_pred,
            "Eye_Problems": eye_pred,
            "Diabetes_Complications": complication_pred,
            "Overall_Damage_Probability": f"{overall_probability:.1f}%"
        }

    except Exception as e:
        traceback.print_exc()  # Logs error to console
        raise HTTPException(status_code=500, detail=str(e))


# 👇 This runs the FastAPI server when executing `python app.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
