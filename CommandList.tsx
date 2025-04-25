import { Circle } from 'lucide-react';

const AVAILABLE_COMMANDS = [
  'What time is it?',
  'Start game',
  'End game',
  'Help',
  'Tell me the weather',
  'Set a reminder',
  'Open calendar',
  'Send a message',
];

export function CommandList() {
  return (
    <div className="bg-blue-900/20 p-6 rounded-lg backdrop-blur-sm border border-blue-500/20">
      <h2 className="text-lg mb-4 font-light">Available Commands</h2>
      <ul className="space-y-2">
        {AVAILABLE_COMMANDS.map((command, index) => (
          <li key={index} className="flex items-center gap-2 text-sm">
            <Circle className="w-2 h-2 text-blue-400" />
            <span>{command}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}