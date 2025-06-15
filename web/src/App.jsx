import React, { useRef, useState } from 'react';
import { runInference } from './infer.js';

export default function App() {
  const imgRef = useRef(null);
  const canvasRef = useRef(null);
  const [result, setResult] = useState(null);

  const handleFile = e => {
    const file = e.target.files[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    imgRef.current.src = url;
  };

  const onLoad = async () => {
    const res = await runInference(imgRef.current);
    setResult(res);
    const ctx = canvasRef.current.getContext('2d');
    ctx.drawImage(imgRef.current, 0, 0);
    res.detections.forEach(d => {
      const [x1, y1, x2, y2] = d.box;
      ctx.strokeStyle = 'red';
      ctx.lineWidth = 2;
      ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
    });
    // Overlay heatmap (simple alpha composite)
    const heatmap = res.heatmap.arraySync();
    // naive overlay for demo
    // ...
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFile} />
      <canvas ref={canvasRef} width={224} height={224} />
      <img ref={imgRef} onLoad={onLoad} alt="" style={{ display: 'none' }} />
      {result && (
        <div>
          Prediction: {result.cls.label} ({(result.cls.score * 100).toFixed(1)}%)
        </div>
      )}
    </div>
  );
}
