import { useState } from "react";

export default function ChatInput({ onSend, disabled = false, compact = false }) {
  const [value, setValue] = useState("");
  const submit = () => {
    const question = value.trim();
    if (!question || disabled) return;
    onSend(question);
    setValue("");
  };
  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      submit();
    }
  };
  return (
    <div className={`chat-input ${compact ? "chat-input--compact" : ""}`}>
      <span className="chat-input__spark">⌕</span>
      <textarea rows={1} value={value} disabled={disabled} onChange={(e) => setValue(e.target.value)} onKeyDown={handleKeyDown} placeholder="Ask a business question..." aria-label="Ask a business question" />
      <button className="send-button" onClick={submit} disabled={disabled || !value.trim()} aria-label="Send question">➤</button>
    </div>
  );
}
