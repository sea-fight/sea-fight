import { useRef, useState } from "react";
import { toast } from "react-toastify";
import isValidGameQueueKey from "./isValidGameQueueKey";

type State = "idle" | "searching";
type WSState = "init" | "seen-ok" | "seen-gameKey";

export default function useGameSearch(onKey: (value: string) => void) {
  const [state, setState] = useState<State>("idle");
  const ws = useRef<WebSocket>();
  const wsState = useRef<WSState>("init");
  const wsForceClosed = useRef(false);

  function triggerSearch() {
    switch (state) {
      case "idle":
        ws.current = new WebSocket(
          process.env.NEXT_PUBLIC_API_URL + "/gameQueue"
        );
        ws.current.onopen = function () {
          this.send("<anonymous>");
        };
        ws.current.onclose = function () {
          if (wsState.current !== "seen-gameKey" && !wsForceClosed.current) {
            toast("Соединение неожиданно закрылось", { type: "error" });
            setState("idle");
          }
          wsForceClosed.current = false;
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
                wsState.current = "seen-gameKey";
                ws.current?.close();
                onKey(data);
              } else {
                isErr = true;
              }
              break;
          }
          if (isErr) {
            toast("Невалидный ответ от сервера", { type: "error" });
            ws.current?.close();
          }
        };
        setState("searching");
        break;

      case "searching":
        wsForceClosed.current = true;
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
