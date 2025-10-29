/**
 * Main chat window component with message display
 */

"use client";

import { useEffect, useRef } from "react";
import { useChatStore } from "@/hooks/useChat";
import { MessageBubble } from "./MessageBubble";
import { Bot } from "lucide-react";

export function ChatWindow() {
  const { messages } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 rounded-full bg-secondary flex items-center justify-center mx-auto mb-4">
            <Bot size={32} className="text-secondary-foreground" />
          </div>
          <h2 className="text-xl font-semibold mb-2">Welcome to Agora</h2>
          <p className="text-muted-foreground max-w-md">
            Start a conversation with our AI agents. They&apos;ll help you with
            academic writing, shopping recommendations, and more.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div
      ref={scrollContainerRef}
      className="flex-1 overflow-y-auto chat-scrollbar px-4 py-6"
    >
      <div className="max-w-4xl mx-auto">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}
