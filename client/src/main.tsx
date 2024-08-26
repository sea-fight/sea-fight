import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import Modal from "react-modal";
import "./main.css";
import App from "./app";

Modal.setAppElement("#root");

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
