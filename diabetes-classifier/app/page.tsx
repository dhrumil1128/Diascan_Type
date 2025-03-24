import React from "react";
import TypeClassifier from "@/components/Services/TypeClassifier";



export default function Home() {
  return (
    <main className="min-h-screen p-6 bg-gray-50">
      <h1 className="text-3xl font-bold text-center mb-8 text-blue-600">
        Type 1 vs Type 2 Diabetes Classifier
      </h1>
      <TypeClassifier />
    </main>
  );
}
