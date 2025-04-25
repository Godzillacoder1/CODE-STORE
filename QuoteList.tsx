import { ThumbsUp, MessageCircle, Share2 } from 'lucide-react';
import { useQuoteStore } from '../store/quoteStore';

export function QuoteList() {
  const { quotes, upvoteQuote } = useQuoteStore();

  return (
    <div className="space-y-6">
      {quotes.map((quote) => (
        <div
          key={quote.id}
          className="bg-gray-800/50 rounded-lg p-6 backdrop-blur-sm border border-gray-700"
        >
          <blockquote className="text-xl text-gray-100 mb-4">
            "{quote.quote}"
          </blockquote>
          
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-400 font-medium">{quote.author}</p>
              <p className="text-sm text-gray-400">{quote.category}</p>
            </div>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={() => upvoteQuote(quote.id)}
                className="flex items-center space-x-1 text-gray-400 hover:text-purple-400 transition-colors"
              >
                <ThumbsUp className="w-4 h-4" />
                <span>{quote.upvotes}</span>
              </button>
              
              <button className="text-gray-400 hover:text-purple-400 transition-colors">
                <MessageCircle className="w-4 h-4" />
              </button>
              
              <button className="text-gray-400 hover:text-purple-400 transition-colors">
                <Share2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}