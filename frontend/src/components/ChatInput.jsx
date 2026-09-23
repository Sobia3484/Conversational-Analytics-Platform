import { useState } from "react";

/**
 * Phase 15 — Chat UI
 * Text input + send button for asking a question. Submits on Enter
 * (Shift+Enter for a newline) or the Send button. Disabled while a
 * request is in flight (wired up properly in Phase 16).
 */
export default function ChatInput({ onSend, disabled }) {
  const [value, setValue] = useState("");

  const submit = () => {
    const question = value.trim();
    if (!question || disabled) return;
    onSend(question);
    setValue("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  return (
    <div className="chat-input">
      <textarea
        className="chat-input__field"
        placeholder="Ask about your sales data — e.g. “Show top 5 products by sales”"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        rows={1}
      />
      <button
        className="chat-input__send"
        onClick={submit}
        disabled={disabled || !value.trim()}
        aria-label="Send question"
      >
        Ask
      </button>
    </div>
  );
}
