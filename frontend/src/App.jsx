// frontend/src/App.jsx
import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    const fd = new FormData();
    if (text) fd.append("text", text);
    if (file) fd.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: fd,
      });
      const data = await res.json();
      setResult(data);
      console.log(data); // Optional: debug in browser console
    } catch (err) {
      console.error("Request failed", err);
      setResult({ error: "Request failed. See console." });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">FakeyNews Detector</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste news text..."
          className="w-full border rounded p-2"
        />
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded"
          type="submit"
          disabled={loading}
        >
          {loading ? "Checking..." : "Check News"}
        </button>
      </form>

      {result && (
        <div className="mt-6 p-4 border rounded">
          {result.error ? (
            <p className="text-red-600">{result.error}</p>
          ) : (
            <>
              <p><strong>Label:</strong> {result.prediction}</p>
              <p><strong>Confidence:</strong> {result.confidence}</p>
              <p><strong>Text Extracted:</strong> <pre className="whitespace-pre-wrap">{result.text_extracted}</pre></p>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
