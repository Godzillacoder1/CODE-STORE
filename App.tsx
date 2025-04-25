import { useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import { Quote, Brain, Search, SlidersHorizontal } from 'lucide-react';
import { useQuoteStore } from './store/quoteStore';
import { QuoteForm } from './components/QuoteForm';
import { QuoteList } from './components/QuoteList';
import { CategoryFilter } from './components/CategoryFilter';

function App() {
  const { fetchQuotes, subscribeToQuotes } = useQuoteStore();

  useEffect(() => {
    fetchQuotes();
    const unsubscribe = subscribeToQuotes();
    return () => {
      unsubscribe();
    };
  }, [fetchQuotes, subscribeToQuotes]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-gray-100">
      <Toaster position="top-center" />
      
      {/* Header */}
      <header className="border-b border-gray-700 bg-gray-900/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Brain className="w-8 h-8 text-purple-400" />
              <h1 className="text-2xl font-semibold tracking-tight">PhilosophicalMinds</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button className="p-2 hover:bg-gray-700 rounded-full transition-colors">
                <Search className="w-5 h-5" />
              </button>
              <button className="p-2 hover:bg-gray-700 rounded-full transition-colors">
                <SlidersHorizontal className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-3">
            <div className="sticky top-8">
              <CategoryFilter />
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-9 space-y-8">
            <QuoteForm />
            <QuoteList />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-700 bg-gray-900/50 backdrop-blur-sm mt-16">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Quote className="w-5 h-5 text-purple-400" />
              <span className="text-sm text-gray-400">Share wisdom, inspire minds</span>
            </div>
            <p className="text-sm text-gray-400">© 2025 PhilosophicalMinds</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App