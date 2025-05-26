import styled from "styled-components";

const Container = styled.div`
  display: flex;
  gap: 40px;
`;

const GameCard = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 300px;
  background-color: #ffbb33;
  border-radius: 8px;
  padding: 10px;
`;

const Title = styled.text`
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
`;

const Label = styled.text`
  font-size: 16px;
  font-weight: bold;
  text-decoration: underline;
`;

const Text = styled.text`
  font-size: 16px;
`;

const TitleContainer = styled.div``;

export { Container, GameCard, Label, Text, Title, TitleContainer };
