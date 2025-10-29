/**
 * Main chat page - orchestrates WebSocket connection and message flow
 */

"use client";

import { useEffect, useState, useCallback } from "react";
import { ChatWindow } from "@/components/ChatWindow";
import { InputBar } from "@/components/InputBar";
import { AgentSelector } from "@/components/AgentSelector";
import { useChatStore } from "@/hooks/useChat";
import { ChatSocket } from "@/lib/socket";

export default function Home() {
  const [socket, setSocket] = useState<ChatSocket | null>(null);
  const [connected, setConnected] = useState(false);

  const {
    addMessage,
    setStreamingMessage,
    completeStreaming,
    setSessionId,
    setLoading,
    setAgents,
    currentAgent,
  } = useChatStore();

  // Initialize WebSocket connection
  useEffect(() => {
    const chatSocket = new ChatSocket();

    chatSocket
      .connect()
      .then(() => {
        setConnected(true);
        setSocket(chatSocket);

        // Set up message handler
        chatSocket.onMessage((data) => {
          switch (data.type) {
            case "start":
              setSessionId(data.session_id);
              setLoading(true);
              break;

            case "token":
              setStreamingMessage(data.content);
              break;

            case "end":
              completeStreaming();
              setLoading(false);
              break;

            case "error":
              addMessage({
                role: "assistant",
                content: `Error: ${data.content}`,
              });
              setLoading(false);
              break;
          }
        });
      })
      .catch((error) => {
        console.error("Failed to connect to WebSocket:", error);
        setConnected(false);
      });

    // Fetch available agents
    fetch("http://localhost:8000/agents")
      .then((res) => res.json())
      .then((data) => {
        if (data.agents) {
          setAgents(data.agents);
        }
      })
      .catch((error) => {
        console.error("Failed to fetch agents:", error);
      });

    return () => {
      chatSocket.disconnect();
    };
  }, []);

  const handleSendMessage = useCallback(
    (message: string) => {
      if (!socket || !connected) {
        console.error("WebSocket not connected");
        return;
      }

      // Add user message to UI
      addMessage({ role: "user", content: message });

      // Send to backend
      socket.send({
        query: message,
        agent_name: currentAgent,
      });
    },
    [socket, connected, currentAgent, addMessage]
  );

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="flex items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-2xl font-bold">Agora</h1>
            <p className="text-sm text-muted-foreground">
              Modular AI Agent Platform
            </p>
          </div>

          <div className="flex items-center gap-3">
            <AgentSelector />
            <div
              className={`w-2 h-2 rounded-full ${
                connected ? "bg-green-500" : "bg-red-500"
              }`}
              title={connected ? "Connected" : "Disconnected"}
            />
          </div>
        </div>
      </header>

      {/* Chat Area */}
      <ChatWindow />

      {/* Input Bar */}
      <InputBar onSend={handleSendMessage} disabled={!connected} />
    </div>
  );
}
