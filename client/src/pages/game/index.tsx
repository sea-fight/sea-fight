import { useEffect, useState } from "react";
import { ThreeDots } from "react-loader-spinner";
import { useParams } from "react-router-dom";

const GamePage = () => {
  const { gameId } = useParams();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    
  }, []);

  if (loading) {
    return (
      <div className="h-screen grid place-items-center">
        <ThreeDots width={200} />
      </div>
    );
  }
};

export default GamePage;
