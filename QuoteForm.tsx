import { useState } from 'react';
import { Quote } from 'lucide-react';
import { useQuoteStore } from '../store/quoteStore';

export function QuoteForm() {
  const [quote, setQuote] = useState('');
  const [author, setAuthor] = useState('');
  const [category, setCategory] = useState('general');
  const { addQuote } = useQuoteStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!quote.trim() || !author.trim()) return;

    await addQuote({
      quote,
      author,
      category,
    });

    setQuote('');
    setAuthor('');
    setCategory('general');
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-800/50 rounded-lg p-6 backdrop-blur-sm border border-gray-700">
      <div className="flex items-center space-x-3 mb-6">
        <Quote className="w-5 h-5 text-purple-400" />
        <h2 className="text-lg font-semibold">Share a Quote</h2>
      </div>

      <div className="space-y-4">
        <div>
          <label htmlFor="quote" className="block text-sm font-medium text-gray-300 mb-1">
            Quote
          </label>
          <textarea
            id="quote"
            value={quote}
            onChange={(e) => setQuote(e.target.value)}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-gray-100 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            rows={3}
            placeholder="Enter a philosophical quote..."
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="author" className="block text-sm font-medium text-gray-300 mb-1">
              Author
            </label>
            <input
              type="text"
              id="author"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-gray-100 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="Who said this?"
            />
          </div>

          <div>
            <label htmlFor="category" className="block text-sm font-medium text-gray-300 mb-1">
              Category
            </label>
            <select
              id="category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-gray-100 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="general">General</option>
              <option value="ethics">Ethics</option>
              <option value="metaphysics">Metaphysics</option>
              <option value="epistemology">Epistemology</option>
              <option value="existentialism">Existentialism</option>
              <option value="political">Political Philosophy</option>
              <option value="aesthetics">Aesthetics</option>
            </select>
          </div>
        </div>

        <button
          type="submit"
          className="w-full bg-purple-600 hover:bg-purple-700 text-white font-medium py-3 px-4 rounded-lg transition-colors"
        >
          Share Quote
        </button>
      </div>
    </form>
  );
}