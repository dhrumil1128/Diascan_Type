"use client";

import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const TypeClassifier = () => {
  const [formData, setFormData] = useState({
    Age: "",
    BMI: "",
    Fasting_Glucose: "",
    HbA1c: "",
    C_Peptide: "",
    Insulin_Level: "",
    Autoantibody_Presence: "",
  });
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>("");

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const validateFields = () => {
    for (const key in formData) {
      if (!formData[key as keyof typeof formData]) {
        return `Please enter a valid value for ${key.replace(/_/g, " ")}.`;
      }
    }
    return null;
  };

  const handleSubmit = async () => {
    const validationError = validateFields();
    if (validationError) {
      setError(validationError);
      setResult(null);
      return;
    }

    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          Age: parseFloat(formData.Age),
          BMI: parseFloat(formData.BMI),
          Fasting_Glucose: parseFloat(formData.Fasting_Glucose),
          HbA1c: parseFloat(formData.HbA1c),
          C_Peptide: parseFloat(formData.C_Peptide),
          Insulin_Level: parseFloat(formData.Insulin_Level),
          Autoantibody_Presence: parseInt(formData.Autoantibody_Presence),
        }),
      });

      let data;
      try {
        data = await response.json();
      } catch {
        throw new Error("Invalid response from the server.");
      }

      if (!response.ok) {
        throw new Error(data.detail || "Prediction failed.");
      }

      setResult(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    }
  };

  return (
    <div className="max-w-xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold text-center">Diabetes Type Classifier</h1>

      <div className="grid gap-4">
        {Object.entries(formData).map(([field, value]) => (
          <input
            key={field}
            className="w-full p-2 border border-gray-300 rounded"
            type="text"
            name={field}
            placeholder={field.replace(/_/g, " ")}
            value={value}
            onChange={handleInputChange}
          />
        ))}
      </div>

      <Button onClick={handleSubmit} className="w-full">Predict Diabetes Type</Button>

      {error && <p className="text-red-500 mt-2 text-center">{error}</p>}

      {result && (
        <Card className="p-4 bg-gray-50 mt-6">
          <h2 className="text-xl font-semibold mb-2">Prediction Result</h2>
          <p><strong>Diabetes Type:</strong> {result.Diabetes_Type}</p>
          <p><strong>Heart Disease:</strong> {result.Heart_Disease}</p>
          <p><strong>Kidney Issues:</strong> {result.Kidney_Issues}</p>
          <p><strong>Nerve Damage:</strong> {result.Nerve_Damage}</p>
          <p><strong>Eye Problems:</strong> {result.Eye_Problems}</p>
          <p><strong>Complications:</strong> {result.Diabetes_Complications}</p>
          <p>
            <strong>Overall Damage Probability:</strong>{" "}
            <span className="text-yellow-600">{result.Overall_Damage_Probability}</span>
          </p>
        </Card>
      )}
    </div>
  );
};

export default TypeClassifier;
