import { ToastContainer } from "react-toastify";
import bg from "./sitebg.png";
import { RouterProvider } from "react-router-dom";
import router from "./router";

const App = () => (
  <>
    <ToastContainer newestOnTop hideProgressBar />
    <img className="object-cover h-screen w-screen -z-10 fixed" src={bg} />
    <RouterProvider router={router} />
  </>
);

export default App;
