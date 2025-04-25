import { Tag } from 'lucide-react';
import { useQuoteStore } from '../store/quoteStore';

const categories = [
  { id: 'all', name: 'All Categories' },
  { id: 'ethics', name: 'Ethics' },
  { id: 'metaphysics', name: 'Metaphysics' },
  { id: 'epistemology', name: 'Epistemology' },
  { id: 'existentialism', name: 'Existentialism' },
  { id: 'political', name: 'Political Philosophy' },
  { id: 'aesthetics', name: 'Aesthetics' },
  { id: 'general', name: 'General' },
];

export function CategoryFilter() {
  const { selectedCategory, setSelectedCategory } = useQuoteStore();

  return (
    <div className="bg-gray-800/50 rounded-lg p-6 backdrop-blur-sm border border-gray-700">
      <div className="flex items-center space-x-3 mb-6">
        <Tag className="w-5 h-5 text-purple-400" />
        <h2 className="text-lg font-semibold">Categories</h2>
      </div>

      <div className="space-y-2">
        {categories.map((category) => (
          <button
            key={category.id}
            onClick={() => setSelectedCategory(category.id)}
            className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
              selectedCategory === category.id
                ? 'bg-purple-600 text-white'
                : 'text-gray-300 hover:bg-gray-700'
            }`}
          >
            {category.name}
          </button>
        ))}
      </div>
    </div>
  );
}