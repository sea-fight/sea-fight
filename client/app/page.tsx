"use client";

import Button from "@/src/ui/Button";
import useGameSearch from "@/src/hooks/mock/useGameSearchMock";
import { useRouter } from "next/navigation";

export default function Page() {
  const router = useRouter();
  const gameSearch = useGameSearch((key) => router.push("/game?key=" + key));

  return (
    <div className="flex h-screen justify-center items-center">
      <Button
        loading={gameSearch.state === "searching"}
        onClick={() => gameSearch.triggerSearch()}
      >
        {gameSearch.state === "idle" ? "Начать игру" : "Прервать поиск"}
      </Button>
    </div>
  );
}
