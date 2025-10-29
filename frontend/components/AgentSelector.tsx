/**
 * Agent selector dropdown component
 */

"use client";

import { useChatStore } from "@/hooks/useChat";
import { ChevronDown, Bot } from "lucide-react";
import { useState, useEffect } from "react";

export function AgentSelector() {
  const { agents, currentAgent, setCurrentAgent } = useChatStore();
  const [isOpen, setIsOpen] = useState(false);

  const selectedAgent = agents.find((a) => a.name === currentAgent);

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 rounded-lg bg-secondary text-secondary-foreground hover:bg-secondary/80 transition-colors"
      >
        <Bot size={16} />
        <span className="text-sm font-medium">
          {selectedAgent?.name || "Auto"}
        </span>
        <ChevronDown
          size={14}
          className={`transition-transform ${isOpen ? "rotate-180" : ""}`}
        />
      </button>

      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />

          {/* Dropdown Menu */}
          <div className="absolute top-full mt-2 left-0 min-w-[200px] bg-popover border border-border rounded-lg shadow-lg z-20 overflow-hidden">
            <div
              className="px-3 py-2 hover:bg-accent cursor-pointer transition-colors"
              onClick={() => {
                setCurrentAgent(null);
                setIsOpen(false);
              }}
            >
              <div className="font-medium text-sm">Auto</div>
              <div className="text-xs text-muted-foreground">
                Automatically select agent
              </div>
            </div>

            {agents.map((agent) => (
              <div
                key={agent.name}
                className="px-3 py-2 hover:bg-accent cursor-pointer transition-colors border-t border-border"
                onClick={() => {
                  setCurrentAgent(agent.name);
                  setIsOpen(false);
                }}
              >
                <div className="font-medium text-sm">{agent.name}</div>
                <div className="text-xs text-muted-foreground">
                  {agent.description}
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
