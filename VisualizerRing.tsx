interface VisualizerRingProps {
  isActive: boolean;
}

export function VisualizerRing({ isActive }: VisualizerRingProps) {
  return (
    <div className="flex items-center justify-center">
      <div className={`
        relative w-32 h-32 rounded-full border-2 border-blue-500/30
        ${isActive ? 'animate-pulse' : ''}
      `}>
        <div className={`
          absolute inset-1 rounded-full border-2 border-blue-400/30
          ${isActive ? 'animate-ping' : ''}
        `} />
        <div className={`
          absolute inset-2 rounded-full border-2 border-blue-300/30
          ${isActive ? 'animate-pulse delay-75' : ''}
        `} />
        <div className={`
          absolute inset-3 rounded-full border-2 border-blue-200/30
          ${isActive ? 'animate-pulse delay-150' : ''}
        `} />
      </div>
    </div>
  );
}