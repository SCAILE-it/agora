/**
 * Zustand store for chat state management
 */

import { create } from "zustand";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  isStreaming?: boolean;
}

export interface Agent {
  name: string;
  description: string;
  model: string;
}

interface ChatState {
  messages: Message[];
  currentAgent: string | null;
  sessionId: string | null;
  isLoading: boolean;
  agents: Agent[];

  // Actions
  addMessage: (message: Omit<Message, "id" | "timestamp">) => void;
  updateLastMessage: (content: string) => void;
  setStreamingMessage: (content: string) => void;
  completeStreaming: () => void;
  setCurrentAgent: (agentName: string | null) => void;
  setSessionId: (id: string) => void;
  setLoading: (loading: boolean) => void;
  setAgents: (agents: Agent[]) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  currentAgent: null,
  sessionId: null,
  isLoading: false,
  agents: [],

  addMessage: (message) =>
    set((state) => ({
      messages: [
        ...state.messages,
        {
          ...message,
          id: Math.random().toString(36).slice(2),
          timestamp: new Date(),
        },
      ],
    })),

  updateLastMessage: (content) =>
    set((state) => {
      const messages = [...state.messages];
      const lastMessage = messages[messages.length - 1];
      if (lastMessage) {
        lastMessage.content = content;
      }
      return { messages };
    }),

  setStreamingMessage: (content) =>
    set((state) => {
      const messages = [...state.messages];
      let lastMessage = messages[messages.length - 1];

      if (!lastMessage || lastMessage.role !== "assistant" || !lastMessage.isStreaming) {
        // Create new streaming message
        lastMessage = {
          id: Math.random().toString(36).slice(2),
          role: "assistant",
          content,
          timestamp: new Date(),
          isStreaming: true,
        };
        messages.push(lastMessage);
      } else {
        // Append to existing streaming message
        lastMessage.content += content;
      }

      return { messages };
    }),

  completeStreaming: () =>
    set((state) => {
      const messages = [...state.messages];
      const lastMessage = messages[messages.length - 1];
      if (lastMessage?.isStreaming) {
        lastMessage.isStreaming = false;
      }
      return { messages };
    }),

  setCurrentAgent: (agentName) => set({ currentAgent: agentName }),

  setSessionId: (id) => set({ sessionId: id }),

  setLoading: (loading) => set({ isLoading: loading }),

  setAgents: (agents) => set({ agents }),

  clearMessages: () => set({ messages: [] }),
}));
