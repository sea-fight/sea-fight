import { useState } from "react";
import { toast } from "react-toastify";

type State = "idle" | "searching" | "failed";

export default function useGameSearch() {
  const [state, setState] = useState<State>("idle");

  function triggerSearch() {
    switch (state) {
      case "idle":
        toast('Ищем игру...')
        setState("searching");
        break;

      case "searching":
        setState("idle");
        break;
    }
  }

  return {
    state,
    triggerSearch,
  };
}
