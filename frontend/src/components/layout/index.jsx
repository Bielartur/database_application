import { Outlet } from "react-router-dom";
import { Container, Line, Navbar, StyledLink } from "./styled";

export function MainLayout() {
  return (
    <Container>
      <Navbar>
        <StyledLink to={"gameform"}>Criar</StyledLink>
        <StyledLink to={"gamelist"}>Procurar Jogo </StyledLink>
        <StyledLink to={"gamelist"}>Lista de Jogos</StyledLink>
      </Navbar>
      <Line />
      <Outlet />
    </Container>
  );
}
