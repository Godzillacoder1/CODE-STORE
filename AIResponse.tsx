import { Message } from '../store/aiStore';

interface AIResponseProps {
  message: Message;
}

export function AIResponse({ message }: AIResponseProps) {
  return (
    <div className={`flex items-start gap-4 ${message.type === 'assistant' ? 'flex-row' : 'flex-row-reverse'}`}>
      <div className={`
        px-4 py-2 rounded-lg max-w-[80%]
        ${message.type === 'assistant' 
          ? 'bg-blue-500/20 text-blue-300' 
          : 'bg-blue-900/40 text-blue-200'
        }
      `}>
        <p className="text-sm">{message.content}</p>
      </div>
    </div>
  );
}