import { useState, useRef, useEffect } from "react";
import ChatInput from "./components/ChatInput.jsx";

/**
 * Phase 15 — Chat UI (shell only)
 *
 * This phase builds the conversational shell: a scrolling thread of
 * questions and answers, plus the input at the bottom. Answers are still
 * a placeholder here — Phase 16 wires this up to the real /query API,
 * and Phase 17 replaces the placeholder with real KPI/chart/table
 * rendering based on response_type.
 */
export default function App() {
  const [messages, setMessages] = useState([]);
  const threadEndRef = useRef(null);

  useEffect(() => {
    threadEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = (question) => {
    const userMessage = { id: crypto.randomUUID(), role: "user", text: question };
    // Placeholder answer — Phase 16 replaces this with the real API call.
    const placeholderAnswer = {
      id: crypto.randomUUID(),
      role: "assistant",
      text: "…", // shown until Phase 16 connects this to the backend
    };
    setMessages((prev) => [...prev, userMessage, placeholderAnswer]);
  };

  return (
    <div className="app">
      <header className="app__header">
        <span className="app__mark">Ledger</span>
        <span className="app__subtitle">Conversational Analytics</span>
      </header>

      <main className="thread">
        {messages.length === 0 && (
          <div className="thread__empty">
            <p>Ask a question about your sales data to get started.</p>
            <ul className="thread__examples">
              <li>What are the total sales?</li>
              <li>Show top 5 products by sales</li>
              <li>Compare sales between Furniture and Technology</li>
            </ul>
          </div>
        )}

        {messages.map((m) => (
          <div key={m.id} className={`bubble bubble--${m.role}`}>
            <span className="bubble__label">{m.role === "user" ? "You" : "Ledger"}</span>
            <p className="bubble__text">{m.text}</p>
          </div>
        ))}
        <div ref={threadEndRef} />
      </main>

      <footer className="app__footer">
        <ChatInput onSend={handleSend} disabled={false} />
      </footer>
    </div>
  );
}
