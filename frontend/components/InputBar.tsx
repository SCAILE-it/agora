/**
 * Message input bar component
 */

"use client";

import { useState, FormEvent, KeyboardEvent } from "react";
import { Send, Loader2 } from "lucide-react";
import { useChatStore } from "@/hooks/useChat";

interface InputBarProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function InputBar({ onSend, disabled }: InputBarProps) {
  const [input, setInput] = useState("");
  const { isLoading } = useChatStore();

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading && !disabled) {
      onSend(input);
      setInput("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="border-t border-border bg-background p-4">
      <div className="flex items-end gap-2 max-w-4xl mx-auto">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message... (Shift+Enter for new line)"
          disabled={isLoading || disabled}
          className="flex-1 resize-none rounded-lg border border-input bg-background px-4 py-3 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring disabled:opacity-50 min-h-[60px] max-h-[200px]"
          rows={1}
        />
        <button
          type="submit"
          disabled={!input.trim() || isLoading || disabled}
          className="rounded-lg bg-primary text-primary-foreground p-3 hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? (
            <Loader2 size={20} className="animate-spin" />
          ) : (
            <Send size={20} />
          )}
        </button>
      </div>
      <div className="text-xs text-muted-foreground text-center mt-2">
        Use <code className="bg-muted px-1 rounded">/paper_writer</code> or{" "}
        <code className="bg-muted px-1 rounded">/shopper</code> to select an agent
      </div>
    </form>
  );
}
