import { create } from 'zustand';

interface GameState {
  score: number;
  health: number;
  materials: number;
  addScore: () => void;
  resetScore: () => void;
  takeDamage: (amount: number) => void;
  addMaterials: (amount: number) => void;
  useMaterials: (amount: number) => boolean;
}

export const useGameStore = create<GameState>((set) => ({
  score: 0,
  health: 100,
  materials: 0,
  addScore: () => set((state) => ({ score: state.score + 100 })),
  resetScore: () => set({ score: 0 }),
  takeDamage: (amount) => set((state) => ({ health: Math.max(0, state.health - amount) })),
  addMaterials: (amount) => set((state) => ({ materials: state.materials + amount })),
  useMaterials: (amount) => set((state) => {
    if (state.materials >= amount) {
      return { materials: state.materials - amount };
    }
    return state;
  }),
}));