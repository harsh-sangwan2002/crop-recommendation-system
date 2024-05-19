import React, { useState } from "react";
import axios from "axios";

const CropForm = () => {
  const [formData, setFormData] = useState({
    nitrogen: "",
    phosphorus: "",
    potassium: "",
    temperature: "",
    humidity: "",
    ph: "",
    rainfall: "",
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://localhost:5000/api/query", {
        formData,
      });
      setResult(response.data.result);
    } catch (error) {
      console.error("Error fetching data:", error);
      setResult("Error fetching data");
    }
  };

  return (
    <div className="main-container">
      <div className="form-container">
        <h1 className="form-title">Predict Your Crop</h1>
        <form className="crop-form" onSubmit={handleSubmit}>
          <label className="form-label">
            Nitrogen:
            <input
              type="number"
              name="nitrogen"
              value={formData.nitrogen}
              onChange={handleChange}
              className="form-input"
            />
          </label>
          <label className="form-label">
            Phosphorus:
            <input
              type="number"
              name="phosphorus"
              value={formData.phosphorus}
              onChange={handleChange}
              className="form-input"
            />
          </label>
          <label className="form-label">
            Potassium:
            <input
              type="number"
              name="potassium"
              value={formData.potassium}
              onChange={handleChange}
              className="form-input"
            />
          </label>
          <label className="form-label">
            Temperature:
            <input
              type="number"
              name="temperature"
              value={formData.temperature}
              onChange={handleChange}
              className="form-input"
            />
          </label>
          <label className="form-label">
            Humidity:
            <input
              type="number"
              name="humidity"
              value={formData.humidity}
              onChange={handleChange}
              className="form-input"
            />
          </label>
          <label className="form-label">
            PH:
            <input
              type="number"
              name="ph"
              value={formData.ph}
              onChange={handleChange}
              className="form-input"
            />
          </label>
          <label className="form-label">
            Rainfall:
            <input
              type="number"
              name="rainfall"
              value={formData.rainfall}
              onChange={handleChange}
              className="form-input"
              placeholder="Rainfall in mm"
            />
          </label>
          {!result && (
            <button type="submit" className="form-button">
              Predict your crop
            </button>
          )}
          {result && (
            <div className="result-container">
              <p className="result-text">{result}</p>
            </div>
          )}
        </form>
      </div>
    </div>
  );
};

export default CropForm;
