import {
  Container,
  GameCard,
  Label,
  Text,
  Title,
  TitleContainer,
} from "./styled";
import { useEffect, useState } from "react";
import axios from "axios";

export function GameList() {
  const [games, setGames] = useState([]);

  const jogos = [
    {
      id: 1,
      titulo: "Metal Slug",
      descricao: "Jogo de tiro iraço",
      ano: "2004",
      categoria: "Ação",
      duracao: "189",
      preco: "18.90",
    },
    {
      id: 2,
      titulo: "Path of Exile",
      descricao: "Farmar farmar e morrer pra mob normal",
      ano: "2014",
      categoria: "RPG",
      duracao: "infinito",
      preco: "79.90",
    },
    {
      id: 3,
      titulo: "Minecraft",
      descricao: "Melhor jogo do mundo",
      ano: "2008",
      categoria: "Sandbox",
      duracao: "infinito",
      preco: "109.90",
    },
  ];

  //Função para pegar a lista de Games do back
  async function renderGames() {
    try {
      console.log("Buscando a lista de games...");
      // const response = await axios.get("http://localhost:5173");
      // setGames(response.data);
    } catch (err) {
      console.log("Ocorreu um erro: ", err);
    }
  }

  // useEffect para chamar a busca no banco toda vez que a página for aberta
  useEffect(() => {
    renderGames();
  }, []);

  return (
    <Container>
      {jogos.length < 0 ? (
        <Title>Não foi encontrado nenhum jogo</Title>
      ) : (
        jogos.map((jogo) => (
          <GameCard>
            <Label>ID:</Label>
            <Text>{jogo.id}</Text>

            <Label>Titulo:</Label>
            <Text>{jogo.titulo}</Text>

            <Label>Descrição:</Label>
            <Text>{jogo.descricao}</Text>

            <Label>Ano:</Label>
            <Text>{jogo.ano}</Text>

            <Label>Categoria:</Label>
            <Text>{jogo.categoria}</Text>

            <Label>Preço::</Label>
            <Text>{jogo.preco}</Text>
          </GameCard>
        ))
      )}
    </Container>
  );
}
