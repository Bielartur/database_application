import { useState } from "react";
import {
  Container,
  Button,
  Form,
  Input,
  Label,
  Title,
  TitleContainer,
  ButtonContainer,
} from "./styled";
import { toast, ToastContainer } from "react-toastify";
import axios from "axios";

export function GameForm() {
  const [formData, setFormData] = useState({
    id: "",
    titulo: "",
    descricao: "",
    ano: "",
    categoria: "",
    duracao: "",
    preco: "",
  });

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      console.log("Criando o jogo...");
      //Aqui vai ficar a parte da integração
      // await axios.post("http://localhost:5173", {
      //   id: formData.id,
      //   titulo: formData.titulo,
      //   descricao: formData.descricao,
      //   ano: formData.ano,
      //   categoria: formData.categoria,
      //   duracao: formData.duracao,
      //   preco: formData.preco,
      // });
      setFormData({
        id: "",
        ano: "",
        categoria: "",
        descricao: "",
        duracao: "",
        preco: "",
        titulo: "",
      });

      toast.success("Jogo criado com sucesso!");
    } catch (err) {
      console.log("Ocorreu um erro ", err);
      toast.error("Ocorreu um erro, tente novamente!");
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  console.log(formData);

  return (
    <Container>
      <Form onSubmit={handleSubmit}>
        <TitleContainer>
          <Title>Criar Jogo</Title>
        </TitleContainer>

        <Label>ID:</Label>
        <Input
          name="id"
          placeholder="ID"
          value={formData.id}
          onChange={handleChange}
        />

        <Label>Título:</Label>
        <Input
          name="titulo"
          placeholder="Título"
          value={formData.titulo}
          onChange={handleChange}
        />

        <Label>Descrição:</Label>
        <Input
          name="descricao"
          placeholder="Descrição"
          value={formData.descricao}
          onChange={handleChange}
        />

        <Label>Ano de Lançamento:</Label>
        <Input
          name="ano"
          placeholder="Ano de Lançamento"
          value={formData.ano}
          onChange={handleChange}
        />

        <Label>Categoria:</Label>
        <Input
          name="categoria"
          placeholder="Categoria"
          value={formData.categoria}
          onChange={handleChange}
        />

        <Label>Duração (min):</Label>
        <Input
          name="duracao"
          placeholder="Duração (min)"
          value={formData.duracao}
          onChange={handleChange}
        />

        <Label>Preço:</Label>
        <Input
          name="preco"
          placeholder="Preço"
          value={formData.preco}
          onChange={handleChange}
        />

        <ButtonContainer>
          <Button type="submit">Criar Jogo</Button>
        </ButtonContainer>
      </Form>

      <ToastContainer position="top-center" autoClose={2000} />
    </Container>
  );
}
