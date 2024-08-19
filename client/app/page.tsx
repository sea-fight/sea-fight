"use client";

import Button from "@/src/ui/Button";
import useGameSearch from "@/src/utils/useGameSearch";

export default function Home() {
  const gameSearch = useGameSearch();

  return (
    <div className="flex h-screen justify-center items-center">
      <Button
        loading={gameSearch.state === "searching"}
        onClick={() => gameSearch.triggerSearch()}
      >
        {gameSearch.state === 'idle' ? 'Начать игру' : 'Прервать поиск'}
      </Button>
    </div>
  );
}
