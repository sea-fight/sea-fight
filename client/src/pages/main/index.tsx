import { useNavigate } from "react-router-dom";
import Button from "../../shared/ui/button";
import generateGameLink from "../../shared/api/endpoints/gameLink";

const IndexPage = () => {
  const nav = useNavigate();

  return (
    <div className="flex h-screen justify-center items-center flex-col gap-10">
      <Button size="big" onClick={() => generateGameLink().then(nav)}>
        Создать игру по ссылке
      </Button>
      <Button size="big" className="relative" disabled>
        Найти игру
        <p className="absolute text-xs left-9">в разработке</p>
      </Button>
    </div>
  );
};

export default IndexPage;
