import { useState } from "react";
import { State } from "../useGameSearch";

export default function useGameSearchMock(onKey: (value: string) => void) {
  const [state, setState] = useState<State>("idle");

  function triggerSearch() {
    setState("searching");
    setTimeout(() => onKey('abcd'), 3000)
  }

  return {
    state,
    triggerSearch,
  };
}
