import { useState } from "react";

function App() {
  const [brandName, setBrandName] = useState("");
  const [product, setProduct] = useState("");
  const [targetAudience, setTargetAudience] = useState("");
  const [tone, setTone] = useState("premium");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeBrand = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze-brand", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          brand_name: brandName,
          product: product,
          target_audience: targetAudience,
          tone: tone,
        }),
      });

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Backend not reachable");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>CreativePilot – Brand Analyzer</h1>

      <input
        placeholder="Brand Name"
        value={brandName}
        onChange={(e) => setBrandName(e.target.value)}
      />
      <br /><br />

      <input
        placeholder="Product"
        value={product}
        onChange={(e) => setProduct(e.target.value)}
      />
      <br /><br />

      <input
        placeholder="Target Audience"
        value={targetAudience}
        onChange={(e) => setTargetAudience(e.target.value)}
      />
      <br /><br />

      <select value={tone} onChange={(e) => setTone(e.target.value)}>
        <option value="premium">Premium</option>
        <option value="professional">Professional</option>
        <option value="casual">Casual</option>
      </select>
      <br /><br />

      <button onClick={analyzeBrand}>
        {loading ? "Analyzing..." : "Analyze Brand"}
      </button>

      <br /><br />

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
  <pre
    style={{
      backgroundColor: "#1e1e1e",
      color: "#00ffcc",
      padding: "20px",
      borderRadius: "8px",
      maxWidth: "800px",
      overflowX: "auto"
    }}
  >
    {JSON.stringify(result, null, 2)}
  </pre>
)}



    </div>
  );
}

export default App;

