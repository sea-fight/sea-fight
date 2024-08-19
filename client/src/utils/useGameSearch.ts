import { useRef, useState } from "react";
import { toast } from "react-toastify";
import isValidGameQueueKey from "./isValidGameQueueKey";

type State = "idle" | "searching";
type WSState = "init" | "seen-ok" | "seen-gameKey";

export default function useGameSearch(onGameKey: (value: string) => void) {
  const [state, setState] = useState<State>("idle");
  const ws = useRef<WebSocket>();
  const wsState = useRef<WSState>("init");
  const wsKey = useRef<string>();

  function triggerSearch() {
    switch (state) {
      case "idle":
        ws.current = new WebSocket("/gameQueue");
        ws.current.onopen = function () {
          this.send("access_token");
        };
        ws.current.onclose = function () {
          if (wsState.current === "seen-gameKey") {
            // Connect to game
          } else {
            toast("Соединение неожиданно закрылось", { type: "error" });
            setState("idle");
          }
        };
        ws.current.onmessage = function ({ data }) {
          let isErr = false;
          switch (wsState.current) {
            case "init":
              if (data === "ok") {
                wsState.current = "seen-ok";
              } else {
                isErr = true;
              }
              break;

            case "seen-ok":
              if (isValidGameQueueKey(data)) {
                wsKey.current = data;
                wsState.current = "seen-gameKey";
                ws.current?.close();
              } else {
                isErr = true;
              }
              break;
          }
          if (isErr) {
            toast("Невалидный ответ от сервера");
            ws.current?.close();
            setState("idle");
          }
        };
        setState("searching");
        break;

      case "searching":
        ws.current?.close();
        setState("idle");
        break;
    }
  }

  return {
    state,
    triggerSearch,
  };
}
