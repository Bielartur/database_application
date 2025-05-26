import { Link } from "react-router-dom";
import styled from "styled-components";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

const Navbar = styled.nav`
  display: flex;
  width: 80%;
  /* gap: 16px; */
  justify-content: space-evenly;
  font-size: 20px;
  padding: 10px;
`;

const Line = styled.hr`
  width: 100%;
`;

const StyledLink = styled(Link)`
  text-decoration: none;
  color: #ffbb33;

  &:hover {
    color: white;
  }
`;

export { Container, Navbar, StyledLink, Line };
