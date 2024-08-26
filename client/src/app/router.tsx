import { createBrowserRouter } from "react-router-dom";
import IndexPage from "../pages/main";
import GamePage from "../pages/game";

const router = createBrowserRouter([
  {
    path: "/",
    element: <IndexPage />,
  },
  {
    path: "/:gameId",
    element: <GamePage />,
  },
]);

export default router;
