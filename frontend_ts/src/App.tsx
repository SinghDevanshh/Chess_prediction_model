import React, { useState } from 'react';
import './style.css';
import rocCurve from './roc_curve.png';
import ShineBorder from "./components/shine-border";
import SparklesText from "./components/Sparkle-text";
import ShimmerButton from "./components/Shimer-button";



interface Result {
  Accuracy: string | number;
  Precision: string | number;
  Predictions: number[];
  message?: string;
}

const PredictionForm: React.FC = () => {
  const players = ['Magnus', 'Hikaru', 'Anish', 'Alireza', 'Ian', 'Fabi', 'Ding', 'Nodirbek'];
  const players2 = ['All (Default Single player mode)', 'Magnus', 'Hikaru', 'Anish', 'Alireza', 'Ian', 'Fabi', 'Ding', 'Nodirbek'];
  const models = ['RandomForest (Recommended)', 'LogisticRegression', 'GradientBoosting', 'SupportVectorMachine'];

  const [player1, setPlayer1] = useState<string>(players[0]);
  const [player2, setPlayer2] = useState<string>(players2[0]);
  const [model, setModel] = useState<string>(models[0]);
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState<boolean>(false);


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // http://127.0.0.1:5000/predict_route
    // https://chess-prediction-model-backend.onrender.com/predict_route
    
    const response = await fetch('https://chess-prediction-model-backend.onrender.com/predict_route', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ player1, player2, model }),
    });

    const data = await response.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="container">
      <div className="form-section">
        <form className="form" onSubmit={handleSubmit}>
          <select value={player1} onChange={(e) => setPlayer1(e.target.value)}>
            {players.map((player, index) => (
              <option key={index} value={player}>{player}</option>
            ))}
          </select>
          <select value={player2} onChange={(e) => setPlayer2(e.target.value)}>
            {players2.map((player, index) => (
              <option key={index} value={player}>{player}</option>
            ))}
          </select>
          <select value={model} onChange={(e) => setModel(e.target.value)}>
            {models.map((model, index) => (
              <option key={index} value={model}>{model}</option>
            ))}
          </select>
            <ShimmerButton className="shadow-2xl">
              <span className="whitespace-pre-wrap text-center text-sm font-medium leading-none tracking-tight text-white dark:from-white dark:to-slate-900/10 lg:text-lg">
                <button type="submit"> 
                  Submit 
                </button>
              </span>
            </ShimmerButton>
        </form>
      </div>
      {loading ? (
        <div className="loading-section">
          <p><SparklesText text="Loading, please wait..." /></p>
        </div>
      ) : (
        result && (
          <div className="result-section">
            {result.message ? (
              <div>
                <h3><SparklesText text="Nice Try" /></h3>
                <p>{result.message}</p>
              </div>
            ) : (
              <div>
                <h3><SparklesText text="Results" /></h3>
                <p>Accuracy: {result.Accuracy}</p>
                <p>Precision: {result.Precision}</p>
                <p>Predictions: {result.Predictions instanceof Array ? result.Predictions.join(', ') : result.Predictions}</p>
                <ShineBorder
                  className="relative flex items-center justify-center overflow-hidden rounded-lg border bg-background md:shadow-xl" 
                  color={["#A07CFE", "#FE8FB5", "#FFBE7B"]}
                >
                  <span className="pointer-events-none whitespace-pre-wrap bg-gradient-to-b from-black to-gray-300/80 bg-clip-text text-center text-8xl font-semibold leading-none text-transparent dark:from-white dark:to-slate-900/10">
                    <img src={rocCurve} style={{margin: "0px"}} alt="ROC Curve" />
                  </span>
                </ShineBorder>
              </div>
            )}
          </div>
        )
      )}
    </div>
  );
}

export default PredictionForm;
