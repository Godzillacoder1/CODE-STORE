import { create } from 'zustand';

export interface Message {
  type: 'user' | 'assistant';
  content: string;
}

interface AIState {
  messages: Message[];
  isProcessing: boolean;
  addMessage: (type: Message['type'], content: string) => void;
  setProcessing: (processing: boolean) => void;
  processMessage: (content: string) => Promise<void>;
}

// Simple response generator
const generateResponse = (message: string): string => {
  const normalizedMessage = message.toLowerCase().trim();
  
  // Time-related queries
  if (normalizedMessage.includes('time')) {
    return `The current time is ${new Date().toLocaleTimeString()}.`;
  }
  
  // Weather-related queries (mock response)
  if (normalizedMessage.includes('weather')) {
    return "I'm a local AI, so I can't check the actual weather. For real weather data, you would need to connect to a weather API.";
  }
  
  // Reminder-related queries
  if (normalizedMessage.includes('reminder')) {
    return "I can simulate setting a reminder, but as a local AI, I can't actually create persistent reminders.";
  }
  
  // Calendar-related queries
  if (normalizedMessage.includes('calendar')) {
    return "I understand you want to access the calendar, but as a local AI, I can't access your actual calendar system.";
  }
  
  // Message-related queries
  if (normalizedMessage.includes('message')) {
    return "I can simulate message handling, but as a local AI, I can't actually send messages.";
  }

  // Game-related commands
  if (normalizedMessage.includes('game')) {
    if (normalizedMessage.includes('start') || normalizedMessage.includes('play')) {
      return "Starting the game! Use WASD to move, SPACE to jump, and mouse to aim and shoot.";
    }
    if (normalizedMessage.includes('stop') || normalizedMessage.includes('end')) {
      return "Game paused. You can resume anytime.";
    }
    return "I can help you with the game! Try saying 'start game' or 'end game'.";
  }

  // Help command
  if (normalizedMessage.includes('help')) {
    return "I can help you with: checking time, weather updates (simulated), setting reminders (simulated), calendar access (simulated), and sending messages (simulated). I can also help you control the game!";
  }

  // Default response
  return "I understand you're trying to communicate with me, but I'm a simple local AI. I can help with basic queries about time, or simulate responses about weather, reminders, calendar, and messages. Try saying 'help' for more information.";
};

export const useAIStore = create<AIState>((set, get) => ({
  messages: [],
  isProcessing: false,
  addMessage: (type, content) => 
    set((state) => ({
      messages: [...state.messages, { type, content }],
    })),
  setProcessing: (processing) => 
    set({ isProcessing: processing }),
  processMessage: async (content: string) => {
    try {
      set({ isProcessing: true });
      get().addMessage('user', content);

      // Simulate processing delay
      await new Promise(resolve => setTimeout(resolve, 500));

      const response = generateResponse(content);
      get().addMessage('assistant', response);
    } catch (error) {
      console.error('Error processing message:', error);
      get().addMessage('assistant', "I apologize, but I'm having trouble processing your request at the moment.");
    } finally {
      set({ isProcessing: false });
    }
  },
}));