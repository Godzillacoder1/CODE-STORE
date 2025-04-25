import { create } from 'zustand';
import toast from 'react-hot-toast';
import { supabase } from '../lib/supabase';

interface Quote {
  id: string;
  quote: string;
  author: string;
  category: string;
  upvotes: number;
  created_at: string;
}

interface QuoteStore {
  quotes: Quote[];
  selectedCategory: string;
  setSelectedCategory: (category: string) => void;
  fetchQuotes: () => Promise<void>;
  addQuote: (quote: Omit<Quote, 'id' | 'upvotes' | 'created_at'>) => Promise<void>;
  upvoteQuote: (id: string) => Promise<void>;
  subscribeToQuotes: () => void;
}

export const useQuoteStore = create<QuoteStore>((set, get) => ({
  quotes: [],
  selectedCategory: 'all',
  
  setSelectedCategory: (category) => {
    set({ selectedCategory: category });
    get().fetchQuotes();
  },

  fetchQuotes: async () => {
    try {
      const { selectedCategory } = get();
      let query = supabase.from('quotes').select('*').order('created_at', { ascending: false });
      
      if (selectedCategory !== 'all') {
        query = query.eq('category', selectedCategory);
      }
      
      const { data, error } = await query;
      
      if (error) throw error;
      set({ quotes: data || [] });
    } catch (error) {
      console.error('Error fetching quotes:', error);
      toast.error('Failed to fetch quotes');
    }
  },

  addQuote: async (quoteData) => {
    try {
      const { data, error } = await supabase
        .from('quotes')
        .insert([quoteData])
        .select()
        .single();

      if (error) throw error;
      
      set((state) => ({
        quotes: [data, ...state.quotes]
      }));

      toast.success('Quote added successfully!');
    } catch (error) {
      console.error('Error adding quote:', error);
      toast.error('Failed to add quote');
    }
  },

  upvoteQuote: async (id) => {
    try {
      const { data, error } = await supabase.rpc('increment_upvotes', { quote_id: id });
      
      if (error) throw error;
      
      set((state) => ({
        quotes: state.quotes.map((quote) =>
          quote.id === id ? { ...quote, upvotes: data } : quote
        )
      }));
    } catch (error) {
      console.error('Error upvoting quote:', error);
      toast.error('Failed to upvote');
    }
  },

  subscribeToQuotes: () => {
    const subscription = supabase
      .channel('quotes_channel')
      .on('postgres_changes', { 
        event: '*', 
        schema: 'public', 
        table: 'quotes' 
      }, () => {
        get().fetchQuotes();
      })
      .subscribe();

    return () => {
      subscription.unsubscribe();
    };
  },
}));