import { BrowserRouter, Route, Router, Routes } from "react-router-dom";
import { Login } from "../pages/login";
import { MainLayout } from "../components/layout";
import { GameForm } from "../pages/gameForm";
import { GameList } from "../pages/gameList";

export function AllRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" index element={<Login />} />

        <Route path="/home" element={<MainLayout />}>
          <Route path="gameform" element={<GameForm />} />
          <Route path="gamelist" element={<GameList />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
